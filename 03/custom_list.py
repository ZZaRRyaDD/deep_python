from collections import UserList


class CustomList(UserList):
    def __add__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        if not (len(other) or len(self)):
            return CustomList([])
        items = []
        if len(other) <= len(self):
            items = [item + self[index] for index, item in enumerate(other)]
            items.extend(self[len(other):])
        else:
            items = [item + other[index] for index, item in enumerate(self)]
            items.extend(other[len(self):])
        return CustomList(items)

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        if not len(self):
            return CustomList([-item for item in other])
        if not len(other):
            return CustomList(self)
        items = []
        if len(self) >= len(other):
            items = [self[index] - other[index] for index in range(0, len(other))]
            items.extend(self[len(other):])
        else:
            items = [item - other[index] for index, item in enumerate(self)]
            items.extend([-item for item in other[len(self):]])
        return CustomList(items)

    def __rsub__(self, other):
        if not isinstance(other, (list, CustomList)):
            raise NotImplementedError  # pragma: no cover
        if not len(self):
            return CustomList(other)
        if not len(other):
            return CustomList([-item for item in self])
        items = []
        if len(other) >= len(self):
            items = [other[index] - self[index] for index in range(0, len(self))]
            items.extend(other[len(self):])
        else:
            items = [item - self[index] for index, item in enumerate(other)]
            items.extend([-item for item in self[len(other):]])
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
        return f"{self.data}, {sum(self, 0)}"  # pragma: no cover
