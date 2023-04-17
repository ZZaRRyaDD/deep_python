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
    ["num", "name", "price"],
    [
        [
            2,
            "some string",
            3,
        ],
    ],
)
def test_descriptors_change_values(num, name, price):
    instance = Data(num, name, price)
    with pytest.raises(ValueError, match="Значение 2 не является числовым"):
        instance.num = "2"
    assert instance.num == num

    with pytest.raises(ValueError, match="Значение 2 не является строковым"):
        instance.name = 2
    assert instance.name == name

    with pytest.raises(ValueError, match="Значение 2 не является числовым"):
        instance.price = "2"
    assert instance.price == price

    with pytest.raises(ValueError, match="Значение -2 не больше нуля"):
        instance.price = -2
    assert instance.price == price


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
