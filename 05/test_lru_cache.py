from lru_cache import LRUCache


def test_lru_cache():
    cache = LRUCache(2)

    cache.set("k1", "val1")
    cache.set("k2", "val2")

    assert cache.get("k3") is None
    assert cache.get("k2") == "val2"
    assert cache.get("k1") == "val1"

    cache.set("k3", "val3")

    assert cache.get("k3") == "val3"
    assert cache.get("k2") is None
    assert cache.get("k1") == "val1"


def test_lru_cache_limit_1():
    cache = LRUCache(1)

    cache.set(1, "val1")
    cache.set(2, "val2")

    assert cache.get(3) is None
    assert cache.get(2) == "val2"
    assert cache.get(1) is None

    cache.set(3, "val3")

    assert cache.get(3) == "val3"
    assert cache.get(2) is None
    assert cache.get(1) is None


def test_lru_cache_change_exists_key():
    cache = LRUCache(3)

    cache.set("k1", "val1")
    cache.set("k2", "val2")
    cache.set("k3", "val3")

    cache.set("k1", "val1_new")

    cache.set(4, "new")

    assert cache.get("k1") == "val1_new"
    assert cache.get("k2") is None
    assert cache.get("k3") == "val3"
    assert cache.get(4) == "new"
