import json
from typing import Callable, Optional


def word_handler(word: str) -> int:
    return len(word)  # pragma: no cover


def parse_json(
        json_str: str,
        keyword_callback: Callable = word_handler,
        required_fields: Optional[str] = None,
        keywords: Optional[str] = None
) -> Optional[tuple[int, int]]:
    if any([required_fields is None, keywords is None]):
        return None
    count_call_callback, sum_responses = 0, 0
    json_doc = json.loads(json_str)
    for key, value in json_doc.items():
        if all([
            key in required_fields,
            intersection := set(value.split(" ")).intersection(set(keywords)),
        ]):
            for word in intersection:
                sum_responses += keyword_callback(word)
                count_call_callback += 1
    return count_call_callback, sum_responses
