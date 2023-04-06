class Integer:
    def __init__(self):
        self._instance_attr_name = ""

    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_integer_{name}"

    def __get__(self, obj, object_type):
        if obj is None:
            return None  # pragma: no cover
        return getattr(obj, self._instance_attr_name)

    def __set__(self, obj, value):
        if obj is None:
            return None  # pragma: no cover
        if not isinstance(value, int):
            raise ValueError(f"Значение {value} не является числовым")
        return setattr(obj, self._instance_attr_name, value)

    def __delete__(self, obj):
        if obj is None:
            return None  # pragma: no cover
        return delattr(obj, self._instance_attr_name)


class String:
    def __init__(self):
        self._instance_attr_name = ""

    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_string_{name}"

    def __get__(self, obj, object_type):
        if obj is None:
            return None  # pragma: no cover
        return getattr(obj, self._instance_attr_name)

    def __set__(self, obj, value):
        if obj is None:
            return None  # pragma: no cover
        if not isinstance(value, str):
            raise ValueError(f"Значение {value} не является строковым")
        return setattr(obj, self._instance_attr_name, value)

    def __delete__(self, obj):
        if obj is None:
            return None  # pragma: no cover
        return delattr(obj, self._instance_attr_name)


class PositiveInteger:
    def __init__(self):
        self._instance_attr_name = ""

    def __set_name__(self, owner, name):
        self._instance_attr_name = f"_positive_integer_{name}"

    def __get__(self, obj, object_type):
        if obj is None:
            return None  # pragma: no cover
        return getattr(obj, self._instance_attr_name)

    def __set__(self, obj, value):
        if obj is None:
            return None  # pragma: no cover
        if not isinstance(value, int):
            raise ValueError(f"Значение {value} не является числовым")
        if value <= 0:
            raise ValueError(f"Значение {value} не больше нуля")
        return setattr(obj, self._instance_attr_name, value)

    def __delete__(self, obj):
        if obj is None:
            return None  # pragma: no cover
        return delattr(obj, self._instance_attr_name)


class Data:
    num = Integer()
    name = String()
    price = PositiveInteger()

    def __init__(self, number, name, price):
        self.num = number
        self.name = name
        self.price = price
