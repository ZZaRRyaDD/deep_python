import argparse
import logging
import logging.config

from custom_logger import conf, CustomFilter


class LRUCache:

    def __init__(self, limit: int = 42):
        parser = argparse.ArgumentParser(
            description="Сбор параметров для логирования",
        )
        parser.add_argument(
            "-s",
            action='store_true',
            help="Дополнительное логирование в stdout",
        )
        parser.add_argument(
            "-f",
            action='store_true',
            help="Флаг применение кастомного фильтра",
        )
        self.args = parser.parse_args()
        logging.config.dictConfig(conf)
        self.main_logger = logging.getLogger("main")
        self.stdout_logger = None
        if self.args.s:
            self.stdout_logger = logging.getLogger("stdout")
        if self.args.f:
            if self.stdout_logger is not None:
                self.stdout_logger.addFilter(CustomFilter())
            self.main_logger.addFilter(CustomFilter())
        self.limit = limit
        self.elements = {}
        self.main_logger.info(
            "Объект кеша инициализирован с емкостью %d", self.limit,
        )
        if self.args.s:
            self.stdout_logger.info(
                "Объект кеша инициализирован с емкостью %d", self.limit,
            )

    def get(self, key):
        if key not in self.elements:
            self.main_logger.warning("Ключа %s не существует", key)
            if self.args.s:
                self.stdout_logger.warning("Ключа %s не существует", key)
            return None
        value = self.elements.pop(key)
        self.main_logger.info("Успешное взятие ключа %s", key)
        if self.args.s:
            self.stdout_logger.info("Успешное взятие ключа %s", key)
        self.elements[key] = value
        if self.args.s:
            self.stdout_logger.debug("Ключ %s перемещен в конец", key)
        return value

    def set(self, key, value):
        if key in self.elements:
            self.main_logger.info("Ключ %s скоро поменяет свое значение", key)
            if self.args.s:
                self.stdout_logger.info("Ключ %s скоро поменяет свое значение", key)
            self.elements.pop(key, None)
        else:
            self.main_logger.warning("Ключа %s нет в кеше", key)
            if self.args.s:
                self.stdout_logger.warning("Ключа %s нет в кеше", key)
            if len(self.elements) == self.limit:
                for_delete = next(iter(self.elements))
                self.main_logger.critical("Ключ %s удаляется из кеша", for_delete)
                if self.args.s:
                    self.stdout_logger.critical("Ключ %s удаляется из кеша", for_delete)
                self.elements.pop(for_delete)
        self.main_logger.debug("Ключ %s добавляется в кеш со значением %s", key, value)
        if self.args.s:
            self.stdout_logger.debug("Ключ %s добавляется в кеш со значением %s", key, value)
        self.elements[key] = value


if __name__ == "__main__":
    cache = LRUCache(5)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.set("k3", "val3")

    cache.get("k2")
    cache.get("k3")
    cache.get(4)

    cache.set("k1", "val1_new")

    cache.set(4, "new")
