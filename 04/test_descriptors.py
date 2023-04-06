import pytest

from descriptors import Data


@pytest.mark.parametrize(
    ["num", "name", "price", "num_result", "name_result", "price_result"],
    [
        [
            2,
            "some string",
            3,
            2,
            "some string",
            3,
        ],
        [
            -5,
            "some string",
            3,
            -5,
            "some string",
            3,
        ],
        [
            -5,
            "some string",
            1,
            -5,
            "some string",
            1,
        ],
    ],
)
def test_descriptors_success(
    num,
    name,
    price,
    num_result,
    name_result,
    price_result,
):
    instance = Data(num, name, price)
    assert (instance.num, instance.name, instance.price) == (num_result, name_result, price_result)


@pytest.mark.parametrize(
    ["num", "name", "price", "message"],
    [
        [
            -2,
            "some string",
            "-3",
            "Значение -3 не является числовым",
        ],
        [
            -2,
            "some string",
            -3,
            "Значение -3 не больше нуля",
        ],
        [
            "-2",
            "some string",
            -3,
            "Значение -2 не является числовым",
        ],
        [
            None,
            "some string",
            -3,
            "Значение None не является числовым",
        ],
        [
            5,
            2,
            -3,
            "Значение 2 не является строковым",
        ],
        [
            "5",
            2,
            -3,
            "Значение 5 не является числовым",
        ],
    ],
)
def test_descriptors_failed(
    num,
    name,
    price,
    message,
):
    with pytest.raises(ValueError, match=message):
        Data(num, name, price)
