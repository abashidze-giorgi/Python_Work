import os
import charset_normalizer


def get_encoding(file_path: str) -> str:
    # read the file
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            content = f.read()
        # detect the encoding
        result = charset_normalizer.detect(content)
        file_encoding = result["encoding"]
        return file_encoding
