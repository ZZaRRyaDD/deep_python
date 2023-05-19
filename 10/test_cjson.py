import json

import ujson

import cjson

def main():
    json_str = '{"hello": 10, "world": "value"}'
    json_doc = json.loads(json_str)
    ujson_doc = ujson.loads(json_str)
    cjson_doc = cjson.loads(json_str)
    print(json_doc)
    print(ujson_doc)
    print(cjson_doc)
    assert json_doc == ujson_doc == cjson_doc
    assert json_str == cjson.dumps(cjson.loads(json_str))


if __name__ == "__main__":
    main()
