import argparse
import logging
import logging.config

from custom_logger import conf


class LRUCache:

    def __init__(self, limit: int = 42):
        parser = argparse.ArgumentParser(
            description="Сбор параметров для логирования",
        )
        parser.add_argument(
            "-s",
            type=bool,
            help="Дополнительное логирование в stdout",
        )
        parser.add_argument(
            "-f",
            type=bool,
            help="Флаг применение кастомного фильтра",
        )
        self.args = parser.parse_args()
        logging.config.dictConfig(conf)
        self.main_logger = logging.getLogger("main")
        self.stdout_logger = None
        if self.args.s:
            self.stdout_logger = logging.getLogger("stdout")
            if self.args.f:
                self.stdout_logger.addFilter()  # добавить фильтр
        self.limit = limit
        self.elements = {}
        self.main_logger.warning(f"Объект кеша инициализирован с емкостью {self.limit}")
        self.stdout_logger.warning(f"Объект кеша инициализирован с емкостью {self.limit}")

    def get(self, key):
        if key not in self.elements:
            self.main_logger.warning(f"Ключа {key} не существует")
            self.stdout_logger.warning(f"Ключа {key} не существует")
            return None
        value = self.elements.pop(key)
        self.main_logger.info(f"Взятие ключа {key} со значением {value}")
        if self.args.s:
            self.stdout_logger.info(f"Взятие ключа {key} со значением {value}")
        self.elements[key] = value
        self.stdout_logger.debug(f"Ключ {key} со значением {value} перемещен в конец")
        return value

    def set(self, key, value):
        if key in self.elements:
            self.main_logger.info(f"Ключ {key} скоро поменяет свое значение")
            self.stdout_logger.info(f"Ключ {key} скоро поменяет свое значение")
            self.elements.pop(key, None)
        else:
            self.main_logger.warning(f"Ключа {key} нет в кеше")
            self.stdout_logger.warning(f"Ключа {key} нет в кеше")
            if len(self.elements) == self.limit:
                for_delete = next(iter(self.elements))
                self.main_logger.critical(f"Ключ {for_delete} удаляется из кеша")
                self.stdout_logger.critical(f"Ключ {for_delete} удаляется из кеша")
                self.elements.pop(for_delete)
        self.main_logger.debug(f"Ключ {key} добавляется в кеш со значением {value}")
        self.stdout_logger.debug(f"Ключ {key} добавляется в кеш со значением {value}")
        self.elements[key] = value


if __name__ == "__main__":
    cache = LRUCache(5)
