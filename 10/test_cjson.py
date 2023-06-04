import json

import pytest
import ujson

import cjson


@pytest.mark.parametrize(
    ["json_str"],
    [
        [
            '{"hello": 10, "world": "value"}',
        ],
        [
            '{"some_key": 1024, "world": "some_value"}',
        ],
        [
            '{"some:key": 1024, "world": "some:value"}',
        ],
    ],
)
def test_cjson_success(json_str: str) -> None:
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)
    assert json_doc == ujson_doc == cjson_doc
    assert json_str == cjson.dumps(cjson.loads(json_str))


@pytest.mark.parametrize(
    ["json_str", "exception", "exception_body"],
    [
        [
            '"hello": 10, "world": "value"}',
            ValueError,
            "Expected start bracket and end bracket in string",
        ],
        [
            '',
            ValueError,
            "String is empty",
        ],
    ],
)
def test_cjson_loads_fail(
    json_str: str,
    exception: Exception,
    exception_body: str,
) -> None:
    with pytest.raises(exception, match=exception_body):
        cjson.loads(json_str)


@pytest.mark.parametrize(
    ["json_object", "exception", "exception_body"],
    [
        [
            {1: "23"},
            TypeError,
            "Expected unicode string object in key",
        ],
        [
            ["123", "123"],
            TypeError,
            "Expected dict object",
        ],
    ],
)
def test_cjson_dumps_fail(
    json_object: list | dict,
    exception: Exception,
    exception_body: str,
) -> None:
    with pytest.raises(exception, match=exception_body):
        cjson.dumps(json_object)
