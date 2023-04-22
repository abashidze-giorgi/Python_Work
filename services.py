import os
import urllib.request
import data_service as ds
import charset_normalizer as csn


if __name__ == '__main__':
    output_dir = os.path.join(os.path.expanduser('~'), output_foleder_name)
    os.makedirs(output_dir, exist_ok=True)
    file_path = download_file('https://lk.globtelecom.ru/upload/test_prog1.csv', output_dir)
    encoding = determine_encoding(file_path)
    data = ds.DataService.parse_file(file_path, encoding)
    ds.DataService.diversification_data_and_save_files(data, encoding)
    delete_file(file_path)
