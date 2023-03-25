import pytest

from task_01_custom_list import CustomList


@pytest.mark.parametrize(
    ["first_operand", "second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            CustomList([6, 8, 10, 11, 8]),
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            [5, 6, 7, 7, 8],
            CustomList([6, 8, 10, 11, 13, 7]),
        ],
        [
            CustomList([]),
            [5, 6, 7, 7, 8],
            CustomList([5, 6, 7, 7, 8]),
        ],
        [
            CustomList([]),
            [],
            CustomList([]),
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4]),
            CustomList([6, 8, 10, 11, 8]),
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4, 5, 7]),
            CustomList([6, 8, 10, 11, 13, 7]),
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([]),
            CustomList([5, 6, 7, 7, 8]),
        ],
        [
            [],
            CustomList([]),
            CustomList([]),
        ],
    ],
)
def test_custom_list_add(
    first_operand: CustomList | list,
    second_operand: CustomList | list,
    result: CustomList | list,
):
    result_add = first_operand + second_operand
    assert result_add == result


@pytest.mark.parametrize(
    ["first_operand", "second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            CustomList([-4, -4, -4, -3, 8]),
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            [5, 6, 7, 7, 8],
            CustomList([-4, -4, -4, -3, -3, 7]),
        ],
        [
            CustomList([]),
            [5, 6, 7, 7, 8],
            CustomList([5, 6, 7, 7, 8]),
        ],
        [
            CustomList([]),
            [],
            CustomList([]),
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4]),
            CustomList([4, 4, 4, 3, 8]),
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4, 5, 7]),
            CustomList([4, 4, 4, 3, 3, 7]),
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([]),
            CustomList([5, 6, 7, 7, 8]),
        ],
        [
            [],
            CustomList([]),
            CustomList([]),
        ],
    ],
)
def test_custom_list_sub(
    first_operand: CustomList | list,
    second_operand: CustomList | list,
    result: CustomList | list,
):
    result_sub = first_operand - second_operand
    assert result_sub == result


@pytest.mark.parametrize(
    ["first_operand", "second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            False,
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            [1, 2, 3, 4, 5, 7],
            True,
        ],
        [
            CustomList([]),
            [5, 6, 7, 7, 8],
            False,
        ],
        [
            CustomList([]),
            [],
            True,
        ],
        [
            [4, 3, 2, 1],
            CustomList([1, 2, 3, 4]),
            True,
        ],
    ],
)
def test_custom_list_eq(
    first_operand: CustomList | list,
    second_operand: CustomList | list,
    result: CustomList | list,
):
    result_eq = first_operand == second_operand
    assert result_eq == result


@pytest.mark.parametrize(
    ["first_operand", "second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            False,
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            [1, 2, 3, 4, 5, 7],
            True,
        ],
        [
            CustomList([]),
            [5, 6, 7, 7, 8],
            False,
        ],
        [
            CustomList([]),
            [],
            True,
        ],
        [
            [4, 3, 2, 1],
            CustomList([1, 2, 3, 4]),
            True,
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4]),
            True,
        ],
    ],
)
def test_custom_list_ge(
    first_operand: CustomList | list,
    second_operand: CustomList | list,
    result: CustomList | list,
):
    result_ge = first_operand >= second_operand
    assert result_ge == result


@pytest.mark.parametrize(
    ["first_operand", "second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            False,
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            [1, 2, 3, 4, 5, 7],
            False,
        ],
        [
            CustomList([]),
            [5, 6, 7, 7, 8],
            False,
        ],
        [
            CustomList([]),
            [],
            False,
        ],
        [
            [4, 3, 2, 1],
            CustomList([1, 2, 3, 4]),
            False,
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4]),
            True,
        ],
    ],
)
def test_custom_list_gt(
    first_operand: CustomList | list,
    second_operand: CustomList | list,
    result: CustomList | list,
):
    result_gt = first_operand > second_operand
    assert result_gt == result


@pytest.mark.parametrize(
    ["first_operand", "second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            True,
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            [1, 2, 3, 4, 5, 7],
            True,
        ],
        [
            CustomList([]),
            [5, 6, 7, 7, 8],
            True,
        ],
        [
            CustomList([]),
            [],
            True,
        ],
        [
            [4, 3, 2, 1],
            CustomList([1, 2, 3, 4]),
            True,
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4]),
            False,
        ],
    ],
)
def test_custom_list_le(
    first_operand: CustomList | list,
    second_operand: CustomList | list,
    result: CustomList | list,
):
    result_gt = first_operand <= second_operand
    assert result_gt == result


@pytest.mark.parametrize(
    ["first_operand", "second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            True,
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            [1, 2, 3, 4, 5, 7],
            False,
        ],
        [
            CustomList([]),
            [5, 6, 7, 7, 8],
            True,
        ],
        [
            CustomList([]),
            [],
            False,
        ],
        [
            [4, 3, 2, 1],
            CustomList([1, 2, 3, 4]),
            False,
        ],
        [
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4]),
            False,
        ],
    ],
)
def test_custom_list_lt(
    first_operand: CustomList | list,
    second_operand: CustomList | list,
    result: CustomList | list,
):
    result_gt = first_operand < second_operand
    assert result_gt == result
