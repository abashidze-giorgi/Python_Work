import os
import re
import datetime
import urllib.request
import get_file_encoding
import charset_normalizer as csn
import read_file_and_return_list


class FileWork:

    file_suffix = '_h.csv'
    phone_number_len = 11
    file_list = []

    def __init__(self, url: str, output_directory: str):
        saved_file_path = self.__download_file(url, output_directory)
        big_data = self.__parse_file(saved_file_path)
        self.__delete_file(saved_file_path)
        self.file_list = self.__diversification_data_and_save_files(big_data, output_directory)

    def __download_file(self, url: str, output_directory: str) -> str:
        saved_file_name = os.path.join(output_directory, os.path.basename(url))
        urllib.request.urlretrieve(url, saved_file_name)
        return saved_file_name

    def __parse_file(self, file_path: str) -> dict:
        data = {
            'cash': [],
            'pos': [],
            'cards': [],
            'bad': []
        }
        file_content = read_file_and_return_list.open_file(file_path)
        for line in file_content:
            person = line.split(";")

            """
            Кривые номера при парсинге должны принтануться в консоли с указанием номера строки где были данные 
            найдены,
            """

            name_last_name = person[3].split(' ')
            name = name_last_name[0]
            last_name = name_last_name[1]
            full_name = person[4]
            pay_method = person[7]
            birth_year = person[8].split('.')[2]
            age = self.__get_person_age(birth_year)
            phone_number = person[0]
            normalize_phone_number = self.__normalize_phone_number(phone_number)
            if normalize_phone_number == '':
                pay_method = 'bad'
            list_len = len(data[pay_method]) + 1
            person = {
                'id': list_len,
                'name': name,
                'lastName': last_name,
                'fullName': full_name,
                'phone': normalize_phone_number,
                'birthYear': birth_year,
                'age': age,
                'payMethod': pay_method
            }

            data[pay_method].append(person)
        print(type(data))
        for file in data:
            file_prefix = file.split(",")[0]
            print(f'количество записей в файле - {file_prefix}_h.csv: {len(data[file])}')

        return data

    def __normalize_phone_number(self, phone_number: str) -> str:
        digits = re.sub('[^0-9]', "", phone_number)
        if len(digits) == self.phone_number_len:
            return digits
        else:
            return ''

    def __get_person_age(self, birth_day: str) -> int:
        return datetime.datetime.now().year - int(birth_day)

    def __diversification_data_and_save_files(self, big_data: dict, output_folder: str) -> list:
        file_names = []

        for dictionary in big_data.items():
            pay_method_name = dictionary[0]
            filename = os.path.join(os.path.expanduser('~'), output_folder,
                                    pay_method_name + self.file_suffix)
            file_names.append(filename)
            file_encoding = get_file_encoding.get_encoding(filename)
            with open(filename, 'w', encoding=file_encoding) as f:
                for item in dictionary[1]:
                    f.write('%s\n' % item)
        return file_names

    def __delete_file(self, filepath: str):
        # Проверьте, существует ли файл
        if os.path.exists(filepath):
            # Удалить файл
            os.remove(filepath)
            print('File -', filepath, 'deleted.')
