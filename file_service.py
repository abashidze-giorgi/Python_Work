import re
import os
import datetime
import urllib.request
import get_file_encoding
import delete_file
import charset_normalizer as csn
import read_file_and_return_list


class FileWork:

    file_suffix = '_h.csv'
    phone_number_len = 11
    file_list = []
    data = None

    def __init__(self, url: str, output_directory: str):
        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        saved_file_path = self.__download_file(url, output_directory)
        self.data = self.__parse_file(saved_file_path)
        self.__save_files(self.data, output_directory)
        delete_file.delete_file(saved_file_path)

    def __download_file(self, url: str, output_directory: str) -> str:
        saved_file_path = os.path.join(output_directory, os.path.basename(url))
        urllib.request.urlretrieve(url, saved_file_path)
        return saved_file_path

    def __parse_file(self, file_path: str) -> dict:
        data = {
            'cash': [],
            'pos': [],
            'cards': [],
            'NA': []
        }
        file_content = read_file_and_return_list.open_file(file_path)
        index = 1
        for line in file_content:
            person = line.split(";")

            """
            Кривые номера при парсинге должны принтануться в консоли с указанием номера строки где были данные 
            найдены,
            """

            name_last_name = person[4].split(' ')
            name = name_last_name[1]
            # last_name = name_last_name[0]
            full_name = person[4]
            pay_method = person[7]
            birth_day = person[8]
            age = self.__get_person_age(birth_day)
            phone_number = person[0]
            normalize_phone_number = self.__normalize_phone_number(phone_number)
            if normalize_phone_number == '':
                pay_method = 'NA'
                normalize_phone_number = person[0]
                person = {
                    'id': index,
                    'name': f'{name} {name_last_name[2]}',
                    'phone': normalize_phone_number,
                    'payMethod': pay_method
                    }
            else:
                list_len = len(data[pay_method]) + 1
                person = {
                    'id': list_len,
                    'fullName': full_name,
                    'phone': normalize_phone_number,
                    'birthYear': birth_day,
                    'age': age,
                    'payMethod': pay_method
                    }
            index += 1
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

    def __get_person_age(self, birth_day: str) -> str:
        birth_date = datetime.datetime.strptime(birth_day, '%d.%m.%Y').date()
        current_date = datetime.date.today()
        age_timedelta = current_date - birth_date
        age_years = age_timedelta.days // 365
        age_months = (age_timedelta.days % 365) // 30
        age_days = (age_timedelta.days % 365) % 30
        return f"{age_years} Год, {age_months} Месяцев и {age_days} Дней"

    def get_data(self):
        return self.data

    def __save_files(self, data: dict, output_folder: str)
        file_names = []

        for key, dictionary in data.items():
            if key == 'cash' or key == 'cards' or key == 'pos':
                filename = os.path.join(os.path.expanduser('~'), output_folder,
                                        key + self.file_suffix)
                file_names.append(filename)

                with open(filename, 'w') as f:  # Open the file to write data
                    for item in dictionary:
                        f.write('%s\n' % item)  # Use the file object to write data to the file
