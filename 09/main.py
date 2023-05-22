import argparse
import logging
import logging.config

from custom_logger import conf, CustomFilter
from lru_cache import LRUCache


def main():
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
    args = parser.parse_args()
    logging.config.dictConfig(conf)
    main_logger = logging.getLogger("main")
    stdout_handler = None
    if args.s:
        stdout_handler = logging.StreamHandler()
        format_file = logging.Formatter(
            "%(asctime)s\t%(levelname)s\t[STDOUT]\t%(message)s",
        )
        main_logger.addHandler(stdout_handler)
        stdout_handler.setFormatter(format_file)
    if args.f:
        if stdout_handler is not None:
            stdout_handler.addFilter(CustomFilter())
        main_logger.addFilter(CustomFilter())
    cache = LRUCache(main_logger, 5)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.set("k3", "val3")

    cache.get("k2")
    cache.get("k3")
    cache.get(4)

    cache.set("k1", "val1_new")

    cache.set(4, "new")


if __name__ == "__main__":
    main()
