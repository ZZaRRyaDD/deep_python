import time
from typing import Any, Callable


class FuncWrapper:
    def __init__(self, func: Callable, count_last_calls: int) -> None:
        self.func = func
        self.nice_index = (-1) * count_last_calls
        self.count_last_calls = count_last_calls
        self.calls = []

    def print_mean(self) -> None:
        runs = self.calls[self.nice_index:]
        print(
            f"Среднее по последним запускам {self.count_last_calls} "
            f"запускам: {sum(runs) / len(runs)}"
        )

    def __call__(self, *args, **kwargs) -> Any:
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()
        self.calls.append(end_time-start_time)
        self.print_mean()
        return result


def mean_deco(count_last_calls: int):
    def _wrapper(func: Callable) -> FuncWrapper:
        return FuncWrapper(func, count_last_calls)
    return _wrapper


@mean_deco(10)
def foo(arg1):
    return 10


@mean_deco(2)
def boo(a, b):
    return a + b


for _ in range(100):
    foo("Walter")  # при каждом вызове выводится среднее по k=10 последним вызовам

# 1 Типы данных в Python, изменяемые/неизменяемые, сложности основных операций контейнерных типов.
# изменяемые - list, dict, set, user define
# не изменяемые - int, bool, str, tuple, frozenset, complex

# 2  Потоки, GIL, особенности использования потоков для различных задач
# Global Interpriter lock. из-за того, что в py object есть поле,
# которое подсчитывает количество ссылок на данный участок в памяти.
# с cpu-bound задачами - в лучшем случае - время такое же
# io-bound - gil отпускает поток и можно добиться прироста производительности

# 3. Написать декоратор, который считает и выводит среднее время выполнения
# последних k вызовов исходной функции.
# k задается через параметр декоратора.
# После каждого вызова задекорированной функции должно выводиться среднее по
# k последним вызовам.
