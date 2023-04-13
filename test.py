import csv
import urllib.request

import charset_normalizer


def download_file():
    url = 'https://lk.globtelecom.ru/upload/test_prog1.csv'
    filename = 'test.csv'
    urllib.request.urlretrieve(url, filename)


def detect_encoding(filepath: str):
    with open(filepath, 'rb') as f:
        result = charset_normalizer.detect(f.read())
        return result.get('encoding')


def read_file():
    filepath = './test.csv'
    encoding = detect_encoding(filepath)
    with open(filepath, 'r', encoding=encoding) as f:
        reader = csv.reader(f, delimiter=';')
        for line in reader:
            print(line)

def main():
    download_file()
    read_file()


if __name__ == '__main__':
    main()