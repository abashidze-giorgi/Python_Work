import os
import re
import datetime
import urllib.request
import charset_normalizer as csn



class FileWork:

    file_suffix = '_h.csv'
    phone_number_len = 11
    file_list = []
    file_encoding = ''

    def __init__(self, url: str, output_directory: str):
        saved_file_path = self.__download_file(url, output_directory)
        self.file_encoding = self.__determine_encoding(saved_file_path)
        big_data = self.__parse_file(saved_file_path, self.file_encoding)
        self.__delete_file(saved_file_path)
        self.file_list = self.__diversification_data_and_save_files(big_data, output_directory, self.file_encoding)
        #self.__print_non_unique_phone_numbers()

    def __download_file(self, url: str, output_directory: str) -> str:
        saved_file_name = os.path.join(output_directory, os.path.basename(url))
        urllib.request.urlretrieve(url, saved_file_name)
        return saved_file_name

    def __determine_encoding(self, filepath: str) -> str:
        # read the file
        if os.path.exists(filepath):
            with open(filepath, 'rb') as f:
                content = f.read()
            # detect the encoding
            result = csn.detect(content)
            file_encoding = result["encoding"]
            print(f'Detected encoding: {file_encoding}')
            return file_encoding

    def __parse_file(self, file_path: str, encoding: str) -> dict:
        data = {
            'cash': [],
            'pos': [],
            'cards': [],
            'bad': []
        }
        with open(file_path, 'r', encoding=encoding) as f:
            for iter_num, line in enumerate(f.readlines()):
                person = line.split(";")

                """
                Кривые номера при парсинге должны принтануться в консоли с указанием номера строки где были данные 
                найдены,
                а также, именем-отчеством. Формат:"ИО: <имя-отчество>; Телефон: <телефон>".
                Люди с кривыми номерами никуда записываться не должны.
                """

                name = person[3]
                full_name = person[4]
                pay_method = person[7]
                birth_year = person[8].split('.')[2]
                age = self.__get_person_age(birth_year)
                phone_number = person[0]
                normalize_phone_number = self.__normalize_phone_number(phone_number)
                if normalize_phone_number != '':
                    list_len = len(data[pay_method]) + 1
                    person = {
                        'id': list_len,
                        'name': name,
                        'fullName': full_name,
                        'phone': normalize_phone_number,
                        'birthYear': birth_year,
                        'age': age,
                        'payMethod': pay_method
                    }
                else:
                    # iter_num+1 потому, что при подсчете строк человек начинает 1, а не с нуля.
                    list_len = len(data['bad']) + 1
                    person = {
                        "номер строки:": list_len,
                        "ФИО:": name,
                        "\nТелефон:": phone_number,
                        'pay_method': 'bad'
                    }
                data[pay_method].append(person)

        print('количество записей в файле - ' + 'pos_h.csv:', len(data['pos']))
        print('количество записей в файле - ' + 'cash_h.csv:', len(data['cash']))
        print('количество записей в файле - ' + 'cards_h.csv:', len(data['cards']))
        print('всего записей:', len(data['pos']) + len(data['cash']) + len(data['cards']))
        return data

    def __normalize_phone_number(self, phone_number: str) -> str:
        digits = re.sub('[^0-9]', "", phone_number)
        if len(digits) == self.phone_number_len:
            return digits
        else:
            return ''

    def __get_person_age(self, birth_day: str) -> int:
        age = datetime.datetime.now().year - int(birth_day)
        return age

    def __diversification_data_and_save_files(self, big_data: dict, output_folder: str, encoding: str) -> list:
        file_names = []

        for dictionary in big_data.items():
            pay_method_name = dictionary[0]
            filename = os.path.join(os.path.expanduser('~'), output_folder,
                                    pay_method_name + self.file_suffix)
            file_names.append(filename)
            with open(filename, 'w', encoding=encoding) as f:
                for item in dictionary[1]:
                    f.write('%s\n' % item)
        return file_names

    """5. По завершении парсинга файла и сохранения данных в файлы, в консоль, в табличном виде, должны принтануться 
        следующие данные: 5.1. Кол-во не уникальных номеров телефонов, и сами номера 5.2. Статистика по людям: сколько 
        человек в какой год родилось, кол-во однофамильцев.

        """

    def FindNonUniqueSureNames(self):
        none

    def __print_non_unique_phone_numbers(self):

        for file in self.file_list:
            unique_numbers_list = []
            non_unique_numbers_list = []
            if os.path.exists(file):
                with open(file, 'r', encoding=self.file_encoding) as f:
                    for line in enumerate(f.readlines()):
                        person = list(line[1].split(','))
                        phone = person[3]
                        if phone not in unique_numbers_list:
                            unique_numbers_list.append(phone)
                        else:
                            non_unique_numbers_list.append(person)

            print('Non unique numbers in', file, '-', len(non_unique_numbers_list))
            for val in non_unique_numbers_list:
                print(val['id'], val['fullname'], val['Phone number'])

    def __delete_file(self, filepath: str):
        # Проверьте, существует ли файл
        if os.path.exists(filepath):
            # Удалить файл
            os.remove(filepath)
            print('File -', filepath, 'deleted.')
