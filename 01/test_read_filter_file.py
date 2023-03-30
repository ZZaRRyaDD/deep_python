from typing import Any

import pytest

from read_filter_file import filter_file_generator


@pytest.mark.parametrize(
    ["words", "strings", "result"],
    [
        [
            [
                "Строка",
                "БУДЕТ",
            ],
            [
                "Какая-то строка, которая будет записана",
                "в файлик",
                "Еще одна строка"
            ],
            [
                "Какая-то строка, которая будет записана",
                "Еще одна строка"
            ],
        ],
        [
            [
                "Строка",
                "БУДЕТ",
            ],
            [
                "Еще какие-то странные предложения",
                "которые будут записаны",
                "в файлик Еще одна строка"
            ],
            [
                "в файлик Еще одна строка",
            ],
        ],
        [
            [
                "Строка",
                "БУДЕТ",
            ],
            [
                "Еще какие-то странные предложения",
                "которые будут записаны",
            ],
            [],
        ],
    ],
)
def test_generator_func_file_name(
    tmpdir: Any,
    words: list,
    strings: list,
    result: list,
    file_name: str = "some_file",
):
    directory = tmpdir.mkdir("directory")
    path_file = directory.join(file_name)
    path_file.write("\n".join(strings))
    assert list(filter_file_generator(words, path_file.strpath)) == result


@pytest.mark.parametrize(
    ["words", "strings", "result"],
    [
        [
            [
                "Строка",
                "БУДЕТ",
            ],
            [
                "Какая-то строка, которая будет записана",
                "в файлик",
                "Еще одна строка"
            ],
            [
                "Какая-то строка, которая будет записана",
                "Еще одна строка"
            ],
        ],
        [
            [
                "Строка",
                "БУДЕТ",
            ],
            [
                "Еще какие-то странные предложения",
                "которые будут записаны",
                "в файлик Еще одна строка"
            ],
            [
                "в файлик Еще одна строка",
            ],
        ],
        [
            [
                "Строка",
                "БУДЕТ",
            ],
            [
                "Еще какие-то странные предложения",
                "которые будут записаны",
            ],
            [],
        ],
    ],
)
def test_generator_func_file_object(
    tmpdir: Any,
    words: list,
    strings: list,
    result: list,
    file_name: str = "some_file",
):
    directory = tmpdir.mkdir("directory")
    path_file = directory.join(file_name)
    path_file.write("\n".join(strings))
    file_ptr = open(path_file, mode="r", encoding="utf-8")
    assert list(filter_file_generator(words, file_object=file_ptr)) == result
    file_ptr.close()
