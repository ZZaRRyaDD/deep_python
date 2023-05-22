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
def test_cjson(json_str: str) -> None:
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)
    assert json_doc == ujson_doc == cjson_doc
    assert json_str == cjson.dumps(cjson.loads(json_str))
