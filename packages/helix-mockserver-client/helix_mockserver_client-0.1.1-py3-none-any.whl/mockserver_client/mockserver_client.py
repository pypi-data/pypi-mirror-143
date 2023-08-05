import collections
import glob
import json
import logging
import os
from logging import Logger
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import parse_qs

import dictdiffer  # type: ignore
from requests import put, Response

from mockserver_client.exceptions.mock_server_exception import (
    MockServerException,
)
from mockserver_client.exceptions.mock_server_expectation_not_found_exception import (
    MockServerExpectationNotFoundException,
)
from mockserver_client.exceptions.mock_server_json_content_mismatch_exception import (
    MockServerJsonContentMismatchException,
)
from mockserver_client.exceptions.mock_server_request_not_found_exception import (
    MockServerRequestNotFoundException,
)
from ._time import _Time
from ._timing import _Timing
from .mockserver_verify_exception import MockServerVerifyException


class Expectation:
    def __init__(
        self, request: Dict[str, Any], response: Dict[str, Any], timing: _Timing
    ) -> None:
        self.request: Dict[str, Any] = request
        self.response: Dict[str, Any] = response
        self.timing: _Timing = timing


class MockServerFriendlyClient(object):
    """
    from https://pypi.org/project/mockserver-friendly-client/
    """

    def __init__(self, base_url: str) -> None:
        self.base_url: str = base_url
        self.expectations: List[Expectation] = []
        self.logger: Logger = logging.getLogger("MockServerClient")
        self.logger.setLevel(os.environ.get("LOGLEVEL") or logging.INFO)

    def _call(self, command: str, data: Any = None) -> Response:
        return put("{}/{}".format(self.base_url, command), data=data)

    def clear(self, path: str) -> None:
        self.expectations = []
        self._call("clear", json.dumps({"path": path}))

    def reset(self) -> None:
        self.expectations = []
        self._call("reset")

    def stub(
        self,
        request1: Any,
        response1: Any,
        timing: Any = None,
        time_to_live: Any = None,
    ) -> None:
        self._call(
            "expectation",
            json.dumps(
                _non_null_options_to_dict(
                    _Option("httpRequest", request1),
                    _Option("httpResponse", response1),
                    _Option("times", (timing or _Timing()).for_expectation()),
                    _Option("timeToLive", time_to_live, formatter=_to_time_to_live),
                )
            ),
        )

    def expect(
        self,
        request1: Dict[str, Any],
        response1: Dict[str, Any],
        timing: _Timing,
        time_to_live: Any = None,
    ) -> None:
        self.stub(request1, response1, timing, time_to_live)
        self.expectations.append(
            Expectation(request=request1, response=response1, timing=timing)
        )

    def expect_files_as_requests(
        self,
        folder: Path,
        url_prefix: Optional[str],
        content_type: str = "application/fhir+json",
        add_file_name: bool = False,
    ) -> List[str]:
        """
        Expects the files as requests
        """
        file_path: str
        files: List[str] = sorted(
            glob.glob(str(folder.joinpath("**/*.json")), recursive=True)
        )
        for file_path in files:
            file_name = os.path.basename(file_path)
            with open(file_path, "r") as file:
                content = json.loads(file.read())

                try:
                    request_parameters = content["request_parameters"]
                except ValueError:
                    raise Exception(
                        "`request_parameters` key not found! It is supposed to contain parameters of the request function."
                    )

                path = f"{('/' + url_prefix) if url_prefix else ''}"
                path = (
                    f"{path}/{os.path.splitext(file_name)[0]}"
                    if add_file_name
                    else path
                )

                try:
                    request_result = content["request_result"]
                except ValueError:
                    raise Exception(
                        "`request_result` key not found. It is supposed to contain the expected result of the requst function."
                    )
                body = (
                    json.dumps(request_result)
                    if content_type == "application/fhir+json"
                    else request_result
                )
                self.expect(
                    mock_request(path=path, **request_parameters),
                    mock_response(body=body),
                    timing=times(1),
                )
                self.logger.info(f"Mocking {self.base_url}{path}: {request_parameters}")
        return files

    def expect_files_as_json_requests(
        self,
        folder: Path,
        path: str,
        json_response_body: Dict[str, Any],
        add_file_name: bool = False,
    ) -> List[str]:
        """
        Expects the files as requests
        """
        file_path: str
        files: List[str] = sorted(
            glob.glob(str(folder.joinpath("**/*.json")), recursive=True)
        )
        for file_path in files:
            file_name = os.path.basename(file_path)
            with open(file_path, "r") as file:
                content: Dict[str, Any] = json.loads(file.read())
                path = (
                    f"{path}/{os.path.splitext(file_name)[0]}"
                    if add_file_name
                    else path
                )
                self.expect(
                    mock_request(path=path, body=json_equals([content]), method="POST"),
                    mock_response(body=json.dumps(json_response_body)),
                    timing=times(1),
                )
                self.logger.info(f"Mocking {self.base_url}{path}")
        return files

    def expect_default(
        self,
    ) -> None:
        response1: Dict[str, Any] = mock_response()
        timing: _Timing = times_any()
        self.stub({}, response1, timing, None)
        self.expectations.append(Expectation({}, {}, timing))

    def match_to_recorded_requests(
        self,
        recorded_requests: List[Dict[str, Any]],
    ) -> List[MockServerException]:
        """
        Matches recorded requests with expected requests
        There are 4 cases possible:
        1. There was an expectation without a corresponding request -> fail
        2. There was a request without a corresponding expectation -> save request as expectation
        3. There was a matching request and expectation but the content did not match -> error and show diff
        4. There was a matching request and expectation and the content matched -> nothing to do


        :param recorded_requests:
        :return: list of match exceptions
        """
        exceptions: List[MockServerException] = []
        unmatched_expectations: List[Dict[str, Any]] = []
        unmatched_requests: List[Dict[str, Any]] = [r for r in recorded_requests]
        expected_request: Dict[str, Any]
        self.logger.debug("-------- EXPECTATIONS --------")
        for expectation in self.expectations:
            self.logger.debug(expectation)
        self.logger.debug("-------- END EXPECTATIONS --------")
        self.logger.debug("-------- REQUESTS --------")
        for recorded_request in recorded_requests:
            self.logger.debug(recorded_request)
        self.logger.debug("-------- END REQUESTS --------")

        # get ids of all recorded requests
        recorded_request_ids: List[str] = []
        for recorded_request in recorded_requests:
            json1 = recorded_request.get("body", {}).get("json", None)
            if json1:
                # get ids from body and match
                # see if the property is string
                if isinstance(json1, str):
                    json1 = json.loads(json1)
                if not isinstance(json1, list):
                    json1 = [json1]
                json1_id: str = (
                    json1[0]["id"]
                    if json1 is not None and json1[0] is not None and "id" in json1[0]
                    else None
                )
                if json1_id is not None:
                    recorded_request_ids.append(json1_id)

        # now try to match requests to expectations
        for expectation in self.expectations:
            expected_request = expectation.request
            found_expectation: bool = False
            try:
                found_expectation = self.find_matches_on_request_and_body(
                    expected_request=expected_request,
                    recorded_requests=recorded_requests,
                    unmatched_requests=unmatched_requests,
                )
                if not found_expectation:
                    found_expectation = self.find_matches_on_request_url_only(
                        expected_request=expected_request,
                        recorded_requests=recorded_requests,
                        unmatched_requests=unmatched_requests,
                    )
            except MockServerJsonContentMismatchException as e:
                exceptions.append(e)
            if not found_expectation and "method" in expected_request:
                unmatched_expectations.append(expected_request)
                self.logger.info("---- EXPECTATION NOT MATCHED ----")
                self.logger.info(f"{expected_request}")
                self.logger.info("IDs sent in requests")
                self.logger.info(f'{",".join(recorded_request_ids)}')
                self.logger.info("---- END EXPECTATION NOT MATCHED ----")
        # now fail for every expectation in unmatched_expectations
        for unmatched_expectation in unmatched_expectations:
            exceptions.append(
                MockServerExpectationNotFoundException(
                    url=unmatched_expectation["path"],
                    json=unmatched_expectation["body"]["json"]
                    if "body" in unmatched_expectation
                    and "json" in unmatched_expectation["body"]
                    else None,
                    querystring_params=unmatched_expectation["queryStringParameters"]
                    if "queryStringParameters" in unmatched_expectation
                    else None,
                )
            )
        # and for every request in unmatched_requests
        for unmatched_request in unmatched_requests:
            exceptions.append(
                MockServerRequestNotFoundException(
                    method=unmatched_request["method"],
                    url=unmatched_request["path"],
                    json_dict=unmatched_request["body"]["json"]
                    if "body" in unmatched_request
                    and "json" in unmatched_request["body"]
                    else None,
                )
            )
        return exceptions

    def find_matches_on_request_url_only(
        self,
        *,
        expected_request: Dict[str, Any],
        recorded_requests: List[Dict[str, Any]],
        unmatched_requests: List[Dict[str, Any]],
    ) -> bool:
        """
        Finds matches on url only and then compares the bodies.  Returns if match was found.
        Throws a JsonContentMismatchException if a url match was found but no body match was found


        :param expected_request:
        :param recorded_requests:
        :param unmatched_requests:
        :return:
        """
        found_expectation: bool = False
        for recorded_request in recorded_requests:
            if "method" in expected_request and self.does_request_match(
                request1=expected_request,
                request2=recorded_request,
                check_body=False,
            ):
                # find all requests that match on url since there can be multiple
                # and then check if the bodies match
                # matching_expectations = [
                #     m
                #     for m in self.expectations
                #     if "method" in m.request
                #     and self.does_request_match(
                #         request1=m.request,
                #         request2=recorded_request,
                #         check_body=False,
                #     )
                # ]
                found_expectation = True
                # remove request from unmatched_requests
                unmatched_request_list = [
                    r
                    for r in unmatched_requests
                    if self.does_request_match(
                        request1=r, request2=recorded_request, check_body=True
                    )
                ]
                if "body" in expected_request and "json" in expected_request["body"]:
                    expected_body = expected_request["body"]["json"]
                    actual_body = recorded_request["body"]["json"]
                    assert len(unmatched_request_list) < 2, (
                        f"Found {len(unmatched_request_list)}"
                        f" unmatched requests for {recorded_request}"
                    )
                    if len(unmatched_request_list) > 0:
                        unmatched_requests.remove(unmatched_request_list[0])
                    self.compare_request_bodies(actual_body, expected_body)
                elif "body" in expected_request:
                    expected_body = expected_request["body"]
                    actual_body = recorded_request["body"]
                    if len(unmatched_request_list) > 0:
                        unmatched_requests.remove(unmatched_request_list[0])
                    self.compare_request_bodies(actual_body, expected_body)
        return found_expectation

    def find_matches_on_request_and_body(
        self,
        *,
        expected_request: Dict[str, Any],
        recorded_requests: List[Dict[str, Any]],
        unmatched_requests: List[Dict[str, Any]],
    ) -> bool:
        """
        Matches on both request and body and returns whether it was able to find a match

        :param expected_request:
        :param recorded_requests:
        :param unmatched_requests:
        :return:
        """
        # first try to find all exact matches on both request url and body
        found_expectation: bool = False
        for recorded_request in recorded_requests:
            # first try to match on both request url AND body
            # If match is found then remove this request from list of unmatched requests
            if "method" in expected_request and self.does_request_match(
                request1=expected_request,
                request2=recorded_request,
                check_body=True,
            ):
                found_expectation = True
                # remove request from unmatched_requests
                unmatched_request_list = [
                    r
                    for r in unmatched_requests
                    if self.does_request_match(
                        request1=r, request2=recorded_request, check_body=True
                    )
                ]
                assert (
                    len(unmatched_request_list) >= 0
                ), f"{','.join([str(c) for c in unmatched_request_list])}"
                if len(unmatched_request_list) > 0:
                    unmatched_requests.remove(unmatched_request_list[0])

            # now try to find matches on just url
        return found_expectation

    @staticmethod
    def does_request_match(
        request1: Dict[str, Any], request2: Dict[str, Any], check_body: bool
    ) -> bool:
        return (
            request1["method"] == request2["method"]
            and request1["path"] == request2["path"]
            and MockServerFriendlyClient.normalize_querystring_params(
                request1.get("queryStringParameters")
            )
            == MockServerFriendlyClient.normalize_querystring_params(
                request2.get("queryStringParameters")
            )
            and MockServerFriendlyClient.does_id_in_request_match(
                request1=request1, request2=request2
            )
            and (
                not check_body
                or MockServerFriendlyClient.does_request_body_match(
                    request1=request1, request2=request2
                )
            )
        )

    @staticmethod
    def convert_query_parameters_to_dict(query: str) -> Dict[str, str]:
        params: Dict[str, List[str]] = parse_qs(query)
        return {k: v[0] for k, v in params.items()}

    @staticmethod
    def does_request_body_match(
        request1: Dict[str, Any], request2: Dict[str, Any]
    ) -> bool:
        if "body" not in request1 and "body" not in request2:
            return True
        if "body" in request1 and "body" not in request2:
            return False
        if "body" in request2 and "body" not in request1:
            return False
        body1 = request1["body"]
        body2 = request2["body"]
        if "json" in body1 and "json" in body2:
            json1 = body1["json"]
            if isinstance(json1, str):
                json1 = json.loads(json1)
            json2 = body2["json"]
            if isinstance(json2, str):
                json2 = json.loads(json2)
            return True if json1 == json2 else False
        if "string" in body1 and request1["headers"]["Content-Type"] == [
            "application/x-www-form-urlencoded"
        ]:
            # mockserver stores x-form-url
            body1 = body1["string"]
            if isinstance(body1, str):
                body1 = MockServerFriendlyClient.convert_query_parameters_to_dict(body1)
        if "string" in body2 and request2["headers"]["Content-Type"] == [
            "application/x-www-form-urlencoded"
        ]:
            # mockserver stores x-form-url
            body2 = body2["string"]
            if isinstance(body2, str):
                body2 = MockServerFriendlyClient.convert_query_parameters_to_dict(body2)
        return True if body1 == body2 else False

    @staticmethod
    def does_id_in_request_match(
        request1: Dict[str, Any], request2: Dict[str, Any]
    ) -> bool:
        json1 = request1.get("body", {}).get("json", None)
        json2 = request2.get("body", {}).get("json", None)

        if json1 and json2:
            # get ids from body and match
            # see if the property is string
            if isinstance(json1, str):
                json1 = json.loads(json1)
            if not isinstance(json1, list):
                json1 = [json1]
            json1_id: str = (
                json1[0]["id"]
                if json1 is not None and json1[0] is not None and "id" in json1[0]
                else None
            )
            if isinstance(json2, str):
                json2 = json.loads(json2)
            if not isinstance(json2, list):
                json2 = [json2]
            json2_id: str = (
                json2[0]["id"]
                if json2 is not None and json2[0] is not None and "id" in json2[0]
                else None
            )
            if "id" in json1[0] and "id" in json2[0]:
                return True if json1_id == json2_id else False
            else:
                return True if json1[0] == json2[0] else False
        elif json1 is None and json2 is None:
            return True
        else:
            return False

    @staticmethod
    def compare_request_bodies(
        actual_body: Union[str, bytes], expected_body: Union[str, bytes]
    ) -> None:
        if isinstance(expected_body, bytes):
            expected_body = expected_body.decode("utf-8")
        expected_dict: Union[Dict[str, Any], List[Dict[str, Any]]] = (
            expected_body
            if isinstance(expected_body, dict)
            else json.loads(expected_body)
        )
        if not isinstance(
            expected_dict, list
        ):  # make both lists so the compare works properly
            expected_dict = [expected_dict]
        actual_dict: Union[Dict[str, Any], List[Dict[str, Any]]] = (
            actual_body
            if isinstance(actual_body, dict) or isinstance(actual_body, list)
            else json.loads(actual_body)
        )
        if not isinstance(
            actual_dict, list
        ):  # make both lists so the compare works properly
            actual_dict = [actual_dict]
        differences = list(dictdiffer.diff(expected_dict, actual_dict))
        if len(differences) > 0:
            raise MockServerJsonContentMismatchException(
                actual=actual_dict,
                expected=expected_dict,
                differences=differences,
                expected_file_path=Path(),
            )

    def verify_expectations(
        self, test_name: Optional[str] = None, files: Optional[List[str]] = None
    ) -> None:
        recorded_requests: List[Dict[str, Any]] = self.retrieve()
        self.logger.debug(f"Count of retrieved requests: {len(recorded_requests)}")
        self.logger.debug("-------- All Retrieved Requests -----")
        for recorded_request in recorded_requests:
            self.logger.debug(f"{recorded_request}")
        self.logger.debug("-------- End All Retrieved Requests -----")
        # now filter to requests for this test only
        if test_name is not None:
            recorded_requests = [r for r in recorded_requests if test_name in r["path"]]
        self.logger.debug(
            f"Count of recorded requests for test: {len(recorded_requests)}"
        )
        exceptions: List[MockServerException] = self.match_to_recorded_requests(
            recorded_requests=recorded_requests
        )
        if len(exceptions) > 0:
            raise MockServerVerifyException(exceptions=exceptions, files=files)

    def retrieve(self) -> List[Dict[str, Any]]:
        result = self._call("retrieve")
        # https://app.swaggerhub.com/apis/jamesdbloom/mock-server-openapi/5.11.x#/control/put_retrieve
        return cast(List[Dict[str, Any]], json.loads(result.text))

    @staticmethod
    def normalize_querystring_params(
        querystring_params: Optional[Union[List[Dict[str, Any]], Dict[str, Any]]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        ensure a dictionary of querystring params is formatted so that the param name is the dictionary key.
        querystring dictionaries from requests sometimes look like this. dont want that.
        "queryStringParameters": [
            {
                "name": "contained",
                "values": [
                    "true"
                ]
            },
            {
                "name": "id",
                "values": [
                    "1023011178"
                ]
            }
        ],
        """
        if querystring_params is None:
            return None
        if type(querystring_params) is dict:
            return querystring_params

        normalized_params: Dict[str, Any] = {}
        for param_dict in querystring_params:
            params: Dict[str, Any] = param_dict  # type: ignore
            normalized_params[params["name"]] = params["values"]
        return normalized_params


def mock_request(
    method: Optional[str] = None,
    path: Optional[str] = None,
    querystring: Optional[Dict[str, Any]] = None,
    body: Optional[Union[str, Dict[str, Any]]] = None,
    headers: Optional[Dict[str, Any]] = None,
    cookies: Optional[str] = None,
) -> Dict[str, Any]:
    return _non_null_options_to_dict(
        _Option("method", method),
        _Option("path", path),
        _Option("queryStringParameters", querystring, formatter=_to_named_values_list),
        _Option("body", body),
        _Option("headers", headers, formatter=_to_named_values_list),
        _Option("cookies", cookies),
    )


def mock_response(
    code: Optional[int] = None,
    body: Optional[Union[str, Dict[str, Any]]] = None,
    headers: Optional[Dict[str, Any]] = None,
    cookies: Optional[str] = None,
    delay: Optional[str] = None,
    reason: Optional[str] = None,
) -> Dict[str, Any]:
    return _non_null_options_to_dict(
        _Option("statusCode", code),
        _Option("reasonPhrase", reason),
        _Option("body", body),
        _Option("headers", headers, formatter=_to_named_values_list),
        _Option("delay", delay, formatter=_to_delay),
        _Option("cookies", cookies),
    )


def times(count: int) -> _Timing:
    return _Timing(count)


def times_once() -> _Timing:
    return _Timing(1)


def times_any() -> _Timing:
    return _Timing()


def form(form1: Any) -> Dict[str, Any]:
    # NOTE(lindycoder): Support for mockservers version before https://github.com/jamesdbloom/mockserver/issues/371
    return collections.OrderedDict(
        (("type", "PARAMETERS"), ("parameters", _to_named_values_list(form1)))
    )


def json_equals(payload: Union[Dict[str, Any], List[Dict[str, Any]]]) -> Dict[str, Any]:
    """Expects that the request payload is equal to the given payload."""
    return collections.OrderedDict(
        (("type", "JSON"), ("json", json.dumps(payload)), ("matchType", "STRICT"))
    )


def text_equals(payload: str) -> Dict[str, Any]:
    """Expects that the request payload is equal to the given payload."""
    return collections.OrderedDict(
        (
            ("type", "STRING"),
            ("string", payload),
            ("contentType", "text/plain; charset=utf-8"),
        )
    )


def json_contains(payload: Dict[str, Any]) -> Dict[str, Any]:
    """Expects the request payload to match all given fields. The request may has more fields."""
    return collections.OrderedDict(
        (
            ("type", "JSON"),
            ("json", json.dumps(payload)),
            ("matchType", "ONLY_MATCHING_FIELDS"),
        )
    )


def json_response(
    body: Any = None, headers: Any = None, **kwargs: Any
) -> Dict[str, Any]:
    headers = headers or {}
    headers["Content-Type"] = "application/json"
    return mock_response(body=json.dumps(body), headers=headers, **kwargs)


class _Option:
    def __init__(self, field: Any, value: Any, formatter: Any = None) -> None:
        self.field = field
        self.value = value
        self.formatter = formatter or (lambda e: e)


def seconds(value: int) -> _Time:
    return _Time("SECONDS", value)


def milliseconds(value: int) -> _Time:
    return _Time("MILLISECONDS", value)


def microseconds(value: int) -> _Time:
    return _Time("MICROSECONDS", value)


def nanoseconds(value: int) -> _Time:
    return _Time("NANOSECONDS", value)


def minutes(value: int) -> _Time:
    return _Time("MINUTES", value)


def hours(value: int) -> _Time:
    return _Time("HOURS", value)


def days(value: int) -> _Time:
    return _Time("DAYS", value)


def _non_null_options_to_dict(*options: Any) -> Dict[str, Any]:
    return {o.field: o.formatter(o.value) for o in options if o.value is not None}


def _to_named_values_list(dictionary: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [{"name": key, "values": [value]} for key, value in dictionary.items()]


def _to_time(value: Union[_Time, int]) -> _Time:
    if not isinstance(value, _Time):
        value = seconds(value)
    return value


def _to_delay(delay: _Time) -> Dict[str, Any]:
    delay = _to_time(delay)
    return {"timeUnit": delay.unit, "value": delay.value}


def _to_time_to_live(time: Union[_Time, int]) -> Dict[str, Any]:
    time = _to_time(time)
    return {"timeToLive": time.value, "timeUnit": time.unit, "unlimited": False}
