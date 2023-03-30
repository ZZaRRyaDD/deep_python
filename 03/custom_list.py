from collections import UserList


class CustomList(UserList):
    def __add__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        if not (len(other) or len(self)):
            return CustomList([])
        items = (
            [item + self[index] for index, item in enumerate(other)] + self[len(other):]
            if len(other) <= len(self)
            else [item + other[index] for index, item in enumerate(self)] + other[len(self):]
        )
        return CustomList(items)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        if not (len(other) or len(self)):
            return CustomList([])
        items = (
            [self[index] - other[index] for index in range(0, len(other))] + self[len(other):]
            if len(self) >= len(other)
            else [item - other[index] for index, item in enumerate(self)] + other[len(self):]
        )
        return CustomList(items)

    def __rsub__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        if not (len(other) or len(self)):
            return CustomList([])
        items = (
            [other[index] - self[index] for index in range(0, len(self))] + other[len(self):]
            if len(other) >= len(self)
            else [item - self[index] for index, item in enumerate(other)] + self[len(other):]
        )
        return CustomList(items)

    def __eq__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        return sum(self) == sum(other)

    def __ge__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        return sum(self) >= sum(other)

    def __gt__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        return sum(self) > sum(other)

    def __le__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        return sum(self) <= sum(other)

    def __lt__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        return sum(self) < sum(other)

    def __str__(self):
        return f"{self.data}, {sum(self)}"  # pragma: no cover
