class CustomMeta(type):

    def __new__(mcs, name, bases, classdict, **kwargs):
        list_changes_keys = [
            key
            for key in classdict.keys() if not (key.startswith("__") and key.endswith("__"))
        ]
        for key in list_changes_keys:
            classdict[f"custom_{key}"] = classdict.pop(key)
        cls = super().__new__(mcs, name, bases, classdict)
        print('Meta __new__', cls, bases, classdict, kwargs)
        return cls

    def __init__(cls, name, bases, classdict, **kwargs):
        list_changes_keys = [
            key
            for key in classdict.keys() if not (key.startswith("__") and key.endswith("__"))
        ]
        for key in list_changes_keys:
            classdict[f"custom_{key}"] = classdict.pop(key)
        print(classdict)
        super().__init__(name, bases, classdict)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"

assert CustomClass.custom_x == 50

inst = CustomClass()
assert inst.custom_x == 50
assert inst.custom_val == 99
assert inst.custom_line() == 100
assert str(inst) == "Custom_by_metaclass"

inst.x  # ошибка
inst.val  # ошибка
inst.line()  # ошибка
inst.yyy  # ошибка

inst.dynamic = "added later"
assert inst.custom_dynamic == "added later"
inst.dynamic  # ошибка
