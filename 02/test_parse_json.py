from typing import Optional

import pytest
from pytest_mock import MockerFixture

from parse_json import parse_json


@pytest.mark.parametrize(
    ["json_str", "required_fields", "keywords", "responses", "args", "result"],
    [
        [
            '{"key1": "word word1 word2"}',
            None,
            None,
            None,
            [],
            None,
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            ['key'],
            None,
            None,
            [],
            None,
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            ['key'],
            ['word1'],
            None,
            [],
            (0, []),
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            ['key1', 'key2'],
            ['word1'],
            [4, 4],
            [(("key1", "word1"),), (("key2", "word1"),)],
            (2, [4, 4]),
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            ['key1', 'key2'],
            ['word1', 'word2'],
            [4, 4, 4, 4],
            [
                (("key1", "word1"),),
                (("key1", "word2"),),
                (("key2", "word1"),),
                (("key2", "word2"),),
            ],
            (4, [4, 4, 4, 4]),
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            ['key1', 'key2'],
            ['word3'],
            [3, 3],
            [],
            (0, []),
        ],
        [
            '{"key1": "word word1 word2", "key2": "word1 word2"}',
            None,
            ['word1'],
            None,
            [],
            None,
        ],
    ],
)
def test_parse_json(
    mocker: MockerFixture,
    json_str: str,
    required_fields: Optional[str],
    keywords: Optional[str],
    responses: Optional[list[int]],
    args: Optional[tuple],
    result: Optional[list],
):
    func = mocker.Mock(side_effect=responses)
    assert parse_json(json_str, func, required_fields=required_fields, keywords=keywords) == result
    assert sorted(func.call_args_list) == args
