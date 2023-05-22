class LRUCache:
    def __init__(self, logger, limit: int = 42):
        self.limit = limit
        self.logger = logger
        self.elements = {}
        self.logger.info(
            "Объект кеша инициализирован с емкостью %d", self.limit,
        )

    def get(self, key):
        if key not in self.elements:
            self.logger.warning("Ключа %s не существует", key)
            return None
        value = self.elements.pop(key)
        self.logger.info("Успешное взятие ключа %s", key)
        self.elements[key] = value
        self.logger.debug("Ключ %s перемещен в конец", key)
        return value

    def set(self, key, value):
        if key in self.elements:
            self.logger.info("Ключ %s скоро поменяет свое значение", key)
            self.elements.pop(key, None)
        else:
            self.logger.warning("Ключа %s нет в кеше", key)
            if len(self.elements) == self.limit:
                for_delete = next(iter(self.elements))
                self.logger.critical("Ключ %s удаляется из кеша", for_delete)
                self.elements.pop(for_delete)
        self.logger.debug(
            "Ключ %s добавляется в кеш со значением %s",
            key,
            value,
        )
        self.elements[key] = value
