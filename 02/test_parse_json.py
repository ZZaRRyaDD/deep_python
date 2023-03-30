from typing import Optional

import pytest
from pytest_mock import MockerFixture

from parse_json import parse_json


@pytest.mark.parametrize(
    ["json_str", "required_fields", "keywords", "responses", "result"],
    [
        [
            '{"key1": "word word1 word2"}',
            None,
            None,
            None,
            None,
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            ['key'],
            None,
            None,
            None,
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            ['key'],
            ['word1'],
            None,
            (0, 0),
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            ['key1', 'key2'],
            ['word1'],
            [3, 3],
            (2, 6),
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            None,
            ['word1'],
            None,
            None,
        ],
    ],
)
def test_parse_json(
    mocker: MockerFixture,
    json_str: str,
    required_fields: Optional[str],
    keywords: Optional[str],
    responses: list[int],
    result: list,
):
    func = mocker.Mock(side_effect=responses)
    assert parse_json(json_str, func, required_fields=required_fields, keywords=keywords) == result
