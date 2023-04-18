import pytest

from custom_list import CustomList


@pytest.mark.parametrize(
    ["first_operand", "copy_first_operand", "second_operand", "copy_second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([6, 8, 10, 11, 8]),
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            CustomList([1, 2, 3, 4, 5, 7]),
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([6, 8, 10, 11, 13, 7]),
        ],
        [
            CustomList([]),
            CustomList([]),
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([5, 6, 7, 7, 8]),
        ],
        [
            CustomList([]),
            CustomList([]),
            [],
            [],
            CustomList([]),
        ],
        [
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4]),
            CustomList([1, 2, 3, 4]),
            CustomList([6, 8, 10, 11, 8]),
        ],
        [
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4, 5, 7]),
            CustomList([1, 2, 3, 4, 5, 7]),
            CustomList([6, 8, 10, 11, 13, 7]),
        ],
        [
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([]),
            CustomList([]),
            CustomList([5, 6, 7, 7, 8]),
        ],
        [
            [],
            [],
            CustomList([]),
            CustomList([]),
            CustomList([]),
        ],
    ],
)
def test_custom_list_add(
    first_operand: CustomList | list,
    copy_first_operand: CustomList | list,
    second_operand: CustomList | list,
    copy_second_operand: CustomList | list,
    result: CustomList | list,
):
    test_result = first_operand + second_operand
    assert test_result == result
    assert len(test_result) == len(result)
    assert all(item == result[index] for index, item in enumerate(test_result))

    assert copy_first_operand == first_operand
    assert len(copy_first_operand) == len(first_operand)
    assert all(item == first_operand[index] for index, item in enumerate(copy_first_operand))

    assert copy_second_operand == second_operand
    assert len(copy_second_operand) == len(second_operand)
    assert all(item == second_operand[index] for index, item in enumerate(copy_second_operand))


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
    assert (first_operand == second_operand) == result


@pytest.mark.parametrize(
    ["first_operand", "copy_first_operand", "second_operand", "copy_second_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            CustomList([1, 2, 3, 4]),
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([-4, -4, -4, -3, -8]),
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            CustomList([1, 2, 3, 4, 5, 7]),
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([-4, -4, -4, -3, -3, 7]),
        ],
        [
            CustomList([]),
            CustomList([]),
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([-5, -6, -7, -7, -8]),
        ],
        [
            CustomList([]),
            CustomList([]),
            [],
            [],
            CustomList([]),
        ],
        [
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4]),
            CustomList([1, 2, 3, 4]),
            CustomList([4, 4, 4, 3, 8]),
        ],
        [
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([1, 2, 3, 4, 5, 7]),
            CustomList([1, 2, 3, 4, 5, 7]),
            CustomList([4, 4, 4, 3, 3, -7]),
        ],
        [
            [5, 6, 7, 7, 8],
            [5, 6, 7, 7, 8],
            CustomList([]),
            CustomList([]),
            CustomList([5, 6, 7, 7, 8]),
        ],
        [
            [],
            [],
            CustomList([]),
            CustomList([]),
            CustomList([]),
        ],
    ],
)
def test_custom_list_sub(
    first_operand: CustomList | list,
    copy_first_operand: CustomList | list,
    second_operand: CustomList | list,
    copy_second_operand: CustomList | list,
    result: CustomList | list,
):
    test_result = first_operand - second_operand
    assert test_result == result
    assert len(test_result) == len(result)
    assert all(item == result[index] for index, item in enumerate(test_result))

    assert copy_first_operand == first_operand
    assert len(copy_first_operand) == len(first_operand)
    assert all(item == first_operand[index] for index, item in enumerate(copy_first_operand))

    assert copy_second_operand == second_operand
    assert len(copy_second_operand) == len(second_operand)
    assert all(item == second_operand[index] for index, item in enumerate(copy_second_operand))


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
    assert (first_operand >= second_operand) == result


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
    assert (first_operand > second_operand) == result


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
    assert (first_operand <= second_operand) == result


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
    assert (first_operand < second_operand) == result


@pytest.mark.parametrize(
    ["first_operand", "result"],
    [
        [
            CustomList([1, 2, 3, 4]),
            f"{[1, 2, 3, 4]}, {10}",
        ],
        [
            CustomList([1, 2, 3, 4, 5, 7]),
            f"{[1, 2, 3, 4, 5, 7]}, {22}",
        ],
        [
            CustomList([]),
            f"{[]}, {0}",
        ],
    ],
)
def test_custom_list_str(
    first_operand: CustomList,
    result: str,
):
    assert str(first_operand) == result
