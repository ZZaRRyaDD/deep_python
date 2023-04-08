class LRUCache:

    def __init__(self, limit: int = 42):
        self.limit = limit
        self.elements = {}

    def get(self, key):
        if key not in self.elements:
            return None
        value = self.elements.pop(key)
        self.elements[key] = value
        return value

    def set(self, key, value):
        item = self.elements.pop(key, None)
        if item is None and len(self.elements) == self.limit:
            for_delete = next(iter(self.elements))
            self.elements.pop(for_delete)
        self.elements[key] = value
