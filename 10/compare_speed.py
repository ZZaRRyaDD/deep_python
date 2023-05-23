import time
import json

import ujson

import cjson
from json_factory import json_factory


def cjson_operations(json_strs):
    start_time = time.time()
    results_loads = [cjson.loads(item) for item in json_strs]
    end_time = time.time()
    time_loads = end_time - start_time

    start_time = time.time()
    _ = [cjson.dumps(item) for item in results_loads]
    end_time = time.time()
    time_dumps = end_time - start_time
    return time_loads, time_dumps


def ujson_operations(json_strs):
    start_time = time.time()
    results_loads = [ujson.loads(item) for item in json_strs]
    end_time = time.time()
    time_loads = end_time - start_time

    start_time = time.time()
    _ = [ujson.dumps(item) for item in results_loads]
    end_time = time.time()
    time_dumps = end_time - start_time
    return time_loads, time_dumps


def json_operations(json_strs):
    start_time = time.time()
    results_loads = [json.loads(item) for item in json_strs]
    end_time = time.time()
    time_loads = end_time - start_time

    start_time = time.time()
    _ = [json.dumps(item) for item in results_loads]
    end_time = time.time()
    time_dumps = end_time - start_time
    return time_loads, time_dumps


def compare_speed_cjson():
    json_strs = json_factory()
    modules = {
        "cjson": cjson_operations,
        "ujson": ujson_operations,
        "json": json_operations,
    }
    for module, func in modules.items():
        time_loads, time_dumps = func(json_strs)
        print(
            f"Время работы {module}: "
            f"loads - {time_loads}; "
            f"dumps - {time_dumps}"
        )


if __name__ == "__main__":
    compare_speed_cjson()
