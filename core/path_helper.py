from os import sep

# обычно называют просто helper файлик
def get_path(
    path_to_file: str,
    file_name: str,
    file_type: str,
) -> str:
    """
    Полный путь к файлу

    Args:
        path_to_file: путь до файла
        file_name: имя файла
        file_type: тип файла

    Returns:
        str: полный путь к файлу
    """
    if path_to_file:
        return sep.join((path_to_file, file_name)) + f".{file_type}"
    else:
        return file_name + f".{file_type}"
