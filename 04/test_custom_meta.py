from custom_meta import CustomClass


def test_custom_meta():
    assert CustomClass.custom_x == 50

    instance = CustomClass()
    assert hasattr(instance, "x") is False
    assert hasattr(instance, "val") is False
    assert hasattr(instance, "line") is False
    assert hasattr(instance, "yyy") is False
    assert instance.custom_x == 50
    assert instance.custom_val == 99
    assert instance.custom_line() == 100
    assert str(instance) == "Custom_by_metaclass"

    instance.dynamic = "added later"
    assert hasattr(instance, "dynamic") is False
    assert instance.custom_dynamic == "added later"
