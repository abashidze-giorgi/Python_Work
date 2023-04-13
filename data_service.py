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
    def diversification_data_and_save_files(data: list[list[dict[str, str | int]]], encoding: str):
        for datalist in data:
            filename = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder',
                                    datalist[0]["salary_pay_method"]+'_h.csv')
            with open(filename, 'w', encoding=encoding) as f:
                for item in datalist:
                    f.write("%s\n" % item)

    @staticmethod
    def parse_file(file_path: str, encoding: str) -> list[list[dict[str, str | int]] | list[dict[str, str | int]]]:
        combined_list = []
        cash_h = []
        pos_h = []
        with open(file_path, 'r', encoding=encoding) as f:
            for i, line in enumerate(f.readlines()):
                line = line.split(";")
                for zero in range(0, 4):  # удаление 4 пустых значений из листа.
                    line.remove('')
                """
                Кривые номера при парсинге должны принтануться в консоли с указанием номера строки где были данные 
                найдены,
                а также, именем-отчеством. Формат:"ИО: <имя-отчество>; Телефон: <телефон>".
                Люди с кривыми номерами никуда записываться не должны.
                """

                if normalize_phone_number(line[0]) != '':
                    birth_year = line[6].split('.')[2]
                    age = get_person_age(birth_year)
                    person_dict = dict(ИО=line[1], ФИО=line[2], Телефон=line[0], Дата_рождения=line[6], Возраст=age,
                                       salary_pay_method=line[5])
                    if line[5] == "pos":
                        pos_h.append(person_dict)
                    else:
                        cash_h.append(person_dict)
                else:
                    # i+1 потому, что при подсчете строк человек начинает 1, а не с нуля.
                    invalid_person = ("номер строки:", i + 1, "ИО:", line[1], "\nТелефон:", line[0])
                    print(invalid_person)
        combined_list.append(pos_h)
        combined_list.append(cash_h)
        return combined_list
