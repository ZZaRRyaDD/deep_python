class CustomMeta(type):

    def __new__(mcs, name, bases, classdict):
        list_changes_keys = [
            key
            for key in classdict.keys()
            if not (key.startswith("__") and key.endswith("__"))
        ]
        for key in list_changes_keys:
            classdict[f"custom_{key}"] = classdict.pop(key)
        classdict["__setattr__"] = CustomMeta.__setattr__
        cls = super().__new__(mcs, name, bases, classdict)
        return cls

    @staticmethod
    def __setattr__(self, name, value):
        if not name.startswith("custom_"):
            object.__setattr__(self, f"custom_{name}", value)


class CustomClass(metaclass=CustomMeta):
    x = 50

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def __str__(self):
        return "Custom_by_metaclass"
