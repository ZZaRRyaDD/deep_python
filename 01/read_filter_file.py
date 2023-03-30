import io


def filter_file_generator(
    words: list,
    file_name: str = "",
    file_object: io.TextIOWrapper = None,
):
    """Генератор для чтения и фильтрации файла"""
    file_object_is_none = file_object is None
    if file_object_is_none:
        file_object = open(file_name, mode="r", encoding="utf-8")
    while line := file_object.readline():
        if any(word.lower() in line.lower().split(" ") for word in words):
            yield line.replace("\n", "")
    if file_object_is_none:
        file_object.close()
