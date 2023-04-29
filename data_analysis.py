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

    def __init__(self, data: dict):

        # logging.basicConfig()
        # self.dir_path = output_folder
        # self.print_bad_phone_numbers_and_delete_bad_file(data['NA'])
        self.sample_of_print(data['NA'], 'Кривые номера')

        self.find_and_print_repeteably_phone_numbers(data)
        self.find_same_last_name_persons(data)
        self.birth_year_counter(data)

    """5. По завершении парсинга файла и сохранения данных в файлы, в консоль, в табличном виде, должны принтануться 
        следующие данные: 5.1. Кол-во не уникальных номеров телефонов, и сами номера 5.2. Статистика по людям: сколько 
        человек в какой год родилось, кол-во однофамильцев.
        """

    def find_and_print_repeteably_phone_numbers(self, data: dict):
        temp_list = []
        checked_phones = []
        non_unique_phone_count = 0
        non_unique_phone_number_list = []
        for list_name in data:
            try:
                data_list = data[list_name]
                for row in data_list:
                    if row['payMethod'] != 'NA':
                        temp_list.append(row['phone'])
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
            self.sample_of_print(non_unique_phone_number_list,
                                 f'Повторяющиеся номера телефонов в файлах: {non_unique_phone_count}')

    def print_bad_phone_numbers_and_delete_bad_file(self, data: list):
        dict_data = []

        for row in data:
            dict_data.append(row)

        self.sample_of_print(data, 'Кривые номера')

    def find_same_last_name_persons(self, data: dict):
        temp_list = []
        checked_persons = []
        same_person_data = []

        for list_name in data:
            try:
                data_list = data[list_name]
                for row in data_list:
                    if row['payMethod'] != 'NA':
                        last_name = row['fullName'].split(' ')[0]
                        temp_list.append(last_name)
            except:
                None

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
        for row in same_person_data:
            full_same += row['count']
        print("")
        print(f'Всего однофамильцев - {full_same}')
        # print(f'Количество повторяющихся фамилии -  - {len(same_person_data)}')
        # self.sample_of_print(same_person_data)

    def birth_year_counter(self, data: dict):

        temp_list = []
        #
        for list_name in data:
            try:
                data_list = data[list_name]
                for row in data_list:
                    if row['payMethod'] != 'NA':
                        temp_list.append(row['birthYear'])
            except:
                None

        count = {}
        for year in temp_list:
            if year in count:
                count[year] += 1
            else:
                count[year] = 1
        result = []
        for year in count:
            year_count = {"year": year, "count": count[year]}
            result.append(year_count)

        self.sample_of_print(result, 'сколько человек в какой год родились')

    def sample_of_print(self, data, message: str):
        try:
            headers = data[0].keys()
            print('')
            print(message)
            table = [[row[col] for col in headers] for row in data]
            print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
        except:
            print('something gone wrong in "sample_of_print" method')
