import os
import urllib.request
import charset_normalizer as csn
import data_service as ds


def download_file(url: str, saved_file_name: str) -> str:
    saved_file_name = os.path.join(saved_file_name, os.path.basename(url))
    urllib.request.urlretrieve(url, saved_file_name)
    return saved_file_name


def determine_encoding(file_path: str) -> str:
    # read the file
    with open(file_path, 'rb') as f:
        content = f.read()
    # detect the encoding
    result = csn.detect(content)
    print(f"Detected encoding: {result['encoding']}")
    return result['encoding']


if __name__ == "__main__":
    output_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder')
    os.makedirs(output_dir, exist_ok=True)
    file_name = download_file("https://lk.globtelecom.ru/upload/test_prog1.csv", output_dir)
    encoding = determine_encoding(file_name)
    data = ds.DataService.parse_file(file_name, encoding)
    ds.DataService.diversification_data_and_save_files(data, encoding)
