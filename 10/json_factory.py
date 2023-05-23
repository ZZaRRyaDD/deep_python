from json import dumps
from random import randint

from faker import Faker

N = 1000


def json_factory(count_keys: int = N) -> list[str]:
    finish_dict = {}
    key, value = None, None
    fake = Faker()
    jsons = []
    for _ in range(count_keys):
        key = "".join(fake.words(6))
        while key in finish_dict:
            key = "".join(fake.words(6))

        is_int = randint(0, 1)
        value = (
            fake.random_number(digits=6)
            if is_int
            else "".join(fake.words(6))
        )
        finish_dict[key] = value
        if len(finish_dict) == 5:
            jsons.append(dumps(finish_dict).replace("'", "\""))
            finish_dict.clear()
    if finish_dict:
        jsons.append(dumps(finish_dict).replace("'", "\""))
    return jsons
