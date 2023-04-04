import json
from typing import Callable, Optional


def word_handler(key: str, word: str) -> int:
    return len(word) + len(key)  # pragma: no cover


def parse_json(
        json_str: str,
        keyword_callback: Callable = word_handler,
        required_fields: Optional[str] = None,
        keywords: Optional[str] = None
) -> Optional[tuple[int, list]]:
    if any([required_fields is None, keywords is None, keyword_callback is None]):
        return None
    count_call_callback, responses = 0, []
    json_doc = json.loads(json_str)
    for key, value in json_doc.items():
        if all([
            key in required_fields,
            intersection := set(value.split(" ")).intersection(set(keywords)),
        ]):
            for word in intersection:
                responses.append(keyword_callback(key, word))
                count_call_callback += 1
    return count_call_callback, responses
