import os
import urllib.request
from typing import List, Dict, Tuple, Optional
import charset_normalizer as csn
import csv
import datetime


def download_file(url: str, output_dir: str) -> str:
    file_name = os.path.join(output_dir, os.path.basename(url))
    urllib.request.urlretrieve(url, file_name)
    return file_name

def determine_encoding(file_path: str) -> str:
    # Read file content
    with open(file_path, 'rb') as f:
        content = f.read()

    # Detect encoding
    result = csn.detect(content)
    print(f"Detected encoding: {result['encoding']}")
    return result['encoding']
    # Normalize encoding to UTF-8
    normalized_content = content.decode(result['encoding']).encode('utf-8')

    # Write normalized content to file
    with open('normalized_filename.csv', 'wb') as f:
        f.write(normalized_content)

def parse_file(file_path: str, encoding: str) -> List[Dict[str, str]]:
    with open(file_path, mode='r', encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=';')
        data = [row for row in reader]
    return data

def normalize_phone_number(phone_number: str) -> Optional[str]:
    digits = ''.join(c for c in phone_number if c.isdigit())
    if len(digits) == 11:
        return digits
    else:
        return None



def record_person(person: dict, file_name: str):
    name = person['ФИО:'] + ' ' + person['имя-отчество'] #ФИО: <фио>
    phone = person['Телефон:']
    dob_str = person['Дата рождения:']
    dob = datetime.datetime.strptime(dob_str, '%d.%m.%Y').date()
    age = (datetime.date.today() - dob).days // 365
    with open(file_name, mode='a', newline='') as f:
        writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Name: ' + name, 'Phone: ' + phone, 'Date of birth: ' + dob_str, 'Age today: ' + str(age)])

def parse_and_record_data(file_path: str, encoding: str):
    cash_file = 'cash_h.csv'
    pos_file = 'pos_h.csv'
    with open(file_path, mode='r', encoding=encoding) as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            if row['Payment type'] == 'cash':
                record_person(row, cash_file)
            elif row['Payment type'] == 'pos':
                record_person(row, pos_file)
            else:
                continue


def write_to_file(data, file_name):
    with open(file_name, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f, delimiter=';')
        for row in data:
            writer.writerow(row)


def main():
    # Step 1: Download file
    url = 'https://lk.globtelecom.ru/upload/test_prog1.csv'
    output_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder')
    os.makedirs(output_dir, exist_ok=True)
    file_path = download_file(url, output_dir)

    # Step 2: Determine encoding and parse
    with open(file_path, mode='r', newline='', encoding=determine_encoding(file_path)) as f:
        reader = csv.reader(f, delimiter=';')
        header = next(reader)  # skip header row
        cash_rows = []
        pos_rows = []
        for row in reader:
            # Step 4: Normalize phone number and print if it's invalid
            phone_number = normalize_phone_number(row[4])
            if phone_number is None:
                print(f"ИО: {row[1]} {row[2]}; Телефон: {row[4]}")

            # Step 3: Record people in 2 different files
            else:
                output_data = [
                    ['ФИО', row[1] + ' ' + row[2]],
                    ['Телефон', phone_number],
                    ['Дата рождения', row[5]],
                    ['Возраст на сегодня', str(datetime.date.today().year - int(row[5][-4:]))]
                ]
                if row[7] == 'cash':
                    cash_rows.append(output_data)
                elif row[7] == 'pos':
                    pos_rows.append(output_data)

    write_to_file(cash_rows, os.path.join(output_dir, 'cash_h.csv'))
    write_to_file(pos_rows, os.path.join(output_dir, 'pos_h.csv'))

if __name__ == "__main__":
    """
    output_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder')
    os.makedirs(output_dir, exist_ok=True)

    file_name = download_file("https://lk.globtelecom.ru/upload/test_prog1.csv", output_dir)
    encod = determine_encoding(file_name)
    data = parse_file(file_name, encod)
    print(data)
    parse_and_record_data(file_name, encod)
    """
    main()