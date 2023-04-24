import os
import ast
import json
import logging
import delete_file
import get_file_encoding
import charset_normalizer
from tabulate import tabulate
import read_file_and_return_list


class DataAnalysis:
    dir_path = ''
    file_encoding = ''

    def __init__(self, output_folder: str):
        logging.basicConfig()
        self.dir_path = output_folder
        list_of_file_names = self.get_file_names_from_directory()
        self.print_bad_phone_numbers_and_delete_bad_file(list_of_file_names)
        self.find_and_print_repeteably_phone_numbers(list_of_file_names)
        self.find_same_last_name_persons(list_of_file_names)
        self.birth_year_counter(list_of_file_names)
    def get_file_names_from_directory(self, ) -> list:
        res = []

        # Iterate directory
        for path in os.listdir(self.dir_path):
            # check if current path is a file
            if os.path.isfile(os.path.join(self.dir_path, path)):
                res.append(path)
        return res

    """5. По завершении парсинга файла и сохранения данных в файлы, в консоль, в табличном виде, должны принтануться 
        следующие данные: 5.1. Кол-во не уникальных номеров телефонов, и сами номера 5.2. Статистика по людям: сколько 
        человек в какой год родилось, кол-во однофамильцев.
        """

    def find_and_print_repeteably_phone_numbers(self, list_of_files: list):
        temp_list = []
        checked_phones = []
        non_unique_phone_count = 0
        non_unique_phone_number_list = []
        for name in list_of_files:
            file_path = os.path.join(self.dir_path, name)
            if os.path.isfile(os.path.join(self.dir_path, name)):
                try:
                    file_content = read_file_and_return_list.open_file(file_path)
                    string_list = [string.strip() for string in file_content]
                    for line in string_list:
                        dictionary = eval(line)
                        if dictionary['payMethod'] != 'bad':
                            temp_list.append(dictionary['phone'])
                    for phone in temp_list:
                        if phone not in checked_phones:
                            checked_phones.append(phone)
                            temp_list.remove(phone)
                        else:
                            temp_list.remove(phone)
                            non_unique_phone_count += 1
                            non_unique_phone = {
                                'None unique phone': phone
                            }
                            non_unique_phone_number_list.append(non_unique_phone)
                except:
                    print('something gone wrong in "find_and_print_repeteably_phone_numbers" method')
        if non_unique_phone_count > 0:
            self.sample_of_print(non_unique_phone_number_list, f'Повторяющиеся номера телефонов в файлах: {non_unique_phone_count}')

    def print_bad_phone_numbers_and_delete_bad_file(self, list_of_files):
        dict_data = []

        for name in list_of_files:
            file_path = os.path.join(self.dir_path, name)
            if os.path.isfile(os.path.join(self.dir_path, name)):
                file_content = read_file_and_return_list.open_file(file_path)
                string_list = [string.strip() for string in file_content]
                pay_method = eval(string_list[0])['payMethod']
                if pay_method == 'NA':
                    for line in string_list:
                        dictionary = eval(line)
                        dict_data.append(dictionary)
                    delete_file.delete_file(file_path)

        self.sample_of_print(dict_data, 'Кривые номера')

    def find_same_last_name_persons(self, list_of_files):
        temp_list = []
        checked_persons = []
        same_person_data = []

        for name in list_of_files:
            file_path = os.path.join(self.dir_path, name)
            if os.path.isfile(os.path.join(self.dir_path, name)):
                file_content = read_file_and_return_list.open_file(file_path)
                string_list = [string.strip() for string in file_content]
                for line in string_list:
                    dictionary = eval(line)
                    last_name = dictionary['fullName'].split(' ')[0]
                    temp_list.append(last_name)

        for lastName in temp_list:
            if lastName not in checked_persons:
                checked_persons.append(lastName)
                last_name_count = temp_list.count(lastName)
                if last_name_count > 1:
                    same_person = {
                        'lastName': lastName,
                        'count': last_name_count
                    }
                    same_person_data.append(same_person)
        full_same = 0
        for la in same_person_data:
            full_same += la['count']
        print("")
        print(f'Всего однофамильцев - {full_same}')
        # print(f'Количество повторяющихся фамилии -  - {len(same_person_data)}')
        # self.sample_of_print(same_person_data)

    def birth_year_counter(self, list_of_files):
        temp_list = []
        checked_year = []
        birth_year_counter = []
        for name in list_of_files:
            file_path = os.path.join(self.dir_path, name)
            if os.path.isfile(os.path.join(self.dir_path, name)):
                file_content = read_file_and_return_list.open_file(file_path)
                string_list = [string.strip() for string in file_content]
                for line in string_list:
                    dictionary = eval(line)
                    birth_year = dictionary['birthYear']
                    temp_list.append(birth_year)
        count = {}
        for year in temp_list:
            if year in count:
                count[year] += 1
            else:
                count[year] = 1
        result = [
            {"year": year, "count": count[year]} for year in count
            ]

        self.sample_of_print(result, 'сколько человек в какой год родились')
    def sample_of_print(self, data, message: str):
        try:
            headers = data[0].keys()
            print('')
            print(message)
            table = [[row[col] for col in headers] for row in data]
            print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
        except Exception:
            logging.error('Failed.', exc_info=True)
            print('something gone wrong in "sample_of_print" method')
