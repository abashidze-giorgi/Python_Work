import os
import datetime
import re

phone_number_len = 11


def get_person_age(birth_day: str) -> int:
    age = datetime.datetime.now().year - int(birth_day)
    return age


def normalize_phone_number(phone_number: str) -> str:
    digits = re.sub('[^0-9]', "", phone_number)

    if len(digits) == phone_number_len:
        return digits
    else:
        return ''


class DataService:

    @staticmethod
    def parse_file(file_path: str, encoding: str) -> dict:
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
                phone_number = person[0]
                phone_number = normalize_phone_number(phone_number)
                if phone_number != '':
                    name = person[3]
                    birth_year = person[8].split('.')[2]
                    age = get_person_age(birth_year)
                    full_name = person[4]
                    pay_method = person[7]
                    list_len = len(data[pay_method]) + 1
                    person_dict = {
                        'id': list_len,
                        'name': name,
                        'fullname': full_name,
                        'phone': phone_number,
                        'birth_year': birth_year,
                        'age': age,
                        'pay_method': pay_method
                    }
                    data[pay_method].append(person_dict)
                else:
                    # iter_num+1 потому, что при подсчете строк человек начинает 1, а не с нуля.
                    name = person[4]
                    list_len = len(data['bad']) + 1
                    invalid_phone_number_person = ("номер строки:", list_len, "ФИО:", name, "\nТелефон:", phone_number)
                    data['bad'].append(invalid_phone_number_person)
        print('количество записей в файле - ' + 'pos_h.csv:', len(data['pos']))
        print('количество записей в файле - ' + 'cash_h.csv:', len(data['cash']))
        print('количество записей в файле - ' + 'cards_h.csv:', len(data['cards']))
        print('всего записей:', len(data['pos']) + len(data['cash']) + len(data['cards']))
        return data
    
    
#     for p_type, p_data in parse_file().items():
#         for item in p_data:
#             print(p_type, item['id])

    """5. По завершении парсинга файла и сохранения данных в файлы, в консоль, в табличном виде, должны принтануться 
    следующие данные: 5.1. Кол-во не уникальных номеров телефонов, и сами номера 5.2. Статистика по людям: сколько 
    человек в какой год родилось, кол-во однофамильцев 

    """
    def print_non_unique_phone_numbers(self: list, encoding: str):

        for file in self:
            unique_numbers_list = []
            non_unique_numbers_list = []
            if os.path.exists(file):
                with open(file, 'r', encoding=encoding) as f:
                    for line in enumerate(f.readlines()):
                        phone = line[1].split(',')[3].split(':')[1]
                        if phone not in unique_numbers_list:
                            unique_numbers_list.append(phone)
                        else:
                            non_unique_numbers_list.append(line)

            print('Non unique numbers in', file, '-', len(non_unique_numbers_list))
            for val in non_unique_numbers_list:
                print('Person id', val[1].split(',')[0].split(':')[1], 'Phone number:',
                      val[1].split(',')[3].split(':')[1])

    def diversification_data_and_save_files(data: dict, encoding: str) -> list():
        file_names = []

        for dictionary in data.items():

            filename = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder',
                                    datalist + '_h.csv')
            file_names.append(filename)
            with open(filename, 'w', encoding=encoding) as f:
                for item in datalist:
                    f.write('%s\n' % item)
        return file_names
