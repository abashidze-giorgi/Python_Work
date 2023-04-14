import os
import datetime


def get_person_age(birth_day: str) -> int:
    age = datetime.datetime.now().year - int(birth_day)
    return age


def normalize_phone_number(phone_number: str) -> str:
    digits = ''.join(c for c in phone_number if c.isdigit())
    if len(digits) == 11:
        return digits
    else:
        return ''


class DataService:

    @staticmethod
    def parse_file(file_path: str, encoding: str) -> list[list[dict[str, str | int]] | list[dict[str, str | int]]]:
        combined_list = []
        cash_h = []
        pos_h = []
        with open(file_path, 'r', encoding=encoding) as f:
            for iter_num, line in enumerate(f.readlines()):
                person = line.split(";")
                for zero in range(0, 4):  # удаление 4 пустых значений из листа.
                    person.remove('')
                """
                Кривые номера при парсинге должны принтануться в консоли с указанием номера строки где были данные 
                найдены,
                а также, именем-отчеством. Формат:"ИО: <имя-отчество>; Телефон: <телефон>".
                Люди с кривыми номерами никуда записываться не должны.
                """
                phone_number = person[0]
                if normalize_phone_number(phone_number) != '':
                    birth_year = person[6].split('.')[2]
                    age = get_person_age(birth_year)
                    person_dict = dict(id=iter_num, name=person[1], fullname=person[2], phone=phone_number,
                                       bd=person[6], age=age, salary_pay_method=person[5])
                    pay_method = person[5]
                    if pay_method == "pos":
                        pos_h.append(person_dict)
                    else:
                        cash_h.append(person_dict)
                else:
                    # i+1 потому, что при подсчете строк человек начинает 1, а не с нуля.
                    name = person[1]
                    phone = person[0]
                    invalid_person = ("номер строки:", i + 1, "ИО:", name, "\nТелефон:", phone)
                    print(invalid_person)
        combined_list.append(pos_h)
        combined_list.append(cash_h)
        print('количество записей в файле - ' + 'pos_h.csv:', len(pos_h))
        print('количество записей в файле - ' + 'cash_h.csv:', len(cash_h))
        print('всего записей:', len(cash_h) + len(pos_h))
        return combined_list

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
                        phone = line[1].split(",")[3].split(":")[1]
                        if phone not in unique_numbers_list:
                            unique_numbers_list.append(phone)
                        else:
                            non_unique_numbers_list.append(line)

            print("Non unique numbers in", file, "-", len(non_unique_numbers_list))
            for val in non_unique_numbers_list:
                print("Person id", val[1].split(",")[0].split(":")[1], "Phone number:",
                      val[1].split(",")[3].split(":")[1])


    def diversification_data_and_save_files(data: list[list[dict[str, str | int]]], encoding: str) -> list():
        file_names = []

        for datalist in data:
            cur_id = 1
            filename = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder',
                                    datalist[0]["salary_pay_method"]+'_h.csv')
            file_names.append(filename)
            with open(filename, 'w', encoding=encoding) as f:
                for item in datalist:
                    item["id"] = cur_id
                    f.write("%s\n" % item)
                    cur_id += 1
        return file_names
