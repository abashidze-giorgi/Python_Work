import get_file_encoding


def open_file(file_path: str) -> list:
    file_encoding = get_file_encoding.get_encoding(file_path)
    with open(file_path, 'r', encoding=file_encoding) as f:
        file_content = f.readlines()
        return file_content

