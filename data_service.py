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
        return None


class DataService:

    @staticmethod
    def diversification_data_and_save_files(data: str, encoding: str):
        filename = ''
        for list in data:
            filename = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder', list[0]["salary_pay_method"]+'_h.cvs')
            with open(filename, 'w', encoding=encoding) as f:
                for item in list:
                    f.write("%s\n" % item)

    @staticmethod
    def parse_file(file_path: str, encoding: str) -> str:
        combined_list = []
        cash_h = []
        pos_h = []
        with open(file_path, 'r', encoding=encoding) as f:
            for i, line in enumerate(f.readlines()):
                # for line in f.readlines():
                line = line.split(";")

                for zero in range(0, 4):  # удаление 4 пустых значений из листа.
                    line.remove('')
                """
                Кривые номера при парсинге должны принтануться в консоли с указанием номера строки где были данные найдены, 
                а также, именем-отчеством. Формат: 
                "ИО: <имя-отчество>; Телефон: <телефон>". 
                Люди с кривыми номерами никуда записываться не должны. 
                """
                """
                1: телефон
                2:ио
                3:фио
                4:зарплата
                5:дата выдачи зарплаты
                6:метод выдачи зарплаты
                7:дата рождения
                8:?
                9:зарплата
                10:?
                """
                if normalize_phone_number(line[0]):
                    birth_year = line[6].split('.')[2]
                    age = get_person_age(birth_year)
                    person_dict = dict(name=line[1], full_name=line[2], phone=line[0], birth_day=line[6], age=age,
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
