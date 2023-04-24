import os
import ast
import json
import get_file_encoding
import charset_normalizer
from tabulate import tabulate
import read_file_and_return_list


class DataAnalysis:

    dir_path = ''
    file_encoding = ''

    def __init__(self, output_folder: str):
        self.dir_path = output_folder

        list_of_file_names = self.get_file_names_from_directory()
        self.find_and_print_repeteably_phone_numbers(list_of_file_names)
        self.print_bad_phone_numbers(list_of_file_names)
        self.find_same_last_name_persons(list_of_file_names)
    def get_file_names_from_directory(self,) -> list:
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
        non_unique_phone_numbers = 0
        non_unique_phone_number_person_list = []
        for name in list_of_files:
            file_path = os.path.join(self.dir_path, name)
            if os.path.isfile(os.path.join(self.dir_path, name)):
                try:
                    file_content = read_file_and_return_list.open_file(file_path)
                    string_list = [string.strip() for string in file_content]

                    for line in string_list:
                        dictionary = eval(line)
                        if dictionary['payMethod'] != 'bad':
                            temp_list.append(dictionary)

                    for person in temp_list:
                        if person['phone'] not in checked_phones:
                            checked_phones.append(person['phone'])
                            temp_list.remove(person)

                        else:
                            temp_list.remove(person)
                            non_unique_phone_numbers += 1
                            non_unique_phone_number_person_list.append(person)


                except:
                    print('something gone wrong in "find_and_print_repeteably_phone_numbers" method')
        if non_unique_phone_numbers > 0:
            print("")
            print(f"Повторяющиеся номера телефонов в файлах:: {non_unique_phone_numbers}")
            self.sample_of_print(non_unique_phone_number_person_list)

    def print_bad_phone_numbers(self, list_of_files):
        dict_data = []

        for name in list_of_files:
            file_path = os.path.join(self.dir_path, name)
            if os.path.isfile(os.path.join(self.dir_path, name)):
                file_content = read_file_and_return_list.open_file(file_path)
                string_list = [string.strip() for string in file_content]

                for line in string_list:
                    dictionary = eval(line)
                    if dictionary['payMethod'] == 'bad':
                        dict_data.append(dictionary)
        print('')
        print('Кривые номера')
        self.sample_of_print(dict_data)

    def find_same_last_name_persons(self, list_of_files):
        same_person_data = []
        temp_list = []
        checked_persons = []

        for name in list_of_files:
            file_path = os.path.join(self.dir_path, name)
            if os.path.isfile(os.path.join(self.dir_path, name)):
                file_content = read_file_and_return_list.open_file(file_path)
                string_list = [string.strip() for string in file_content]

                for line in string_list:
                    dictionary = eval(line)
                    temp_list.append(dictionary['lastName'])

        for lastName in temp_list:
            if lastName not in checked_persons:
                checked_persons.append(lastName)
                last_name_count = temp_list.count(lastName)
                if(last_name_count) > 1:
                    same_person = {
                        'lastName': lastName,
                        'count' : last_name_count
                    }
                    same_person_data.append(same_person)
        fullsame = 0
        for la in same_person_data:
            fullsame += la['count']

        newlist = set(temp_list)
        print (len(newlist))
        print(fullsame)

    def sample_of_print(self, data):
        try:
            headers = data[0].keys()
            table = [[row[col] for col in headers] for row in data]
            print(tabulate(table, headers=headers, tablefmt='fancy_grid'))
        except:
            print('something gone wrong in "sample_of_print" method')
