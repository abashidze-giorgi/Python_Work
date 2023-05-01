import re
import os
import datetime
import delete_file
import urllib.request
import get_file_encoding
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

        """
        Функция загружает файл по ссылке url и сохраняет его в указанную директорию.
        :param url: ссылка на файл для загрузки
        :param output_directory: директория для сохранения файла
        :return: полный путь к сохраненному файлу.
        """
    def __download_file(self, url: str, output_directory: str) -> str:
        # Создание полного пути для сохранения файла
        saved_file_path = os.path.join(output_directory, os.path.basename(url))
        # Загрузка файла по указанной ссылке и сохранение в указанную директорию
        urllib.request.urlretrieve(url, saved_file_path)
        # Возврат полного пути сохраненного файла
        return saved_file_path

    """
        Функция считывает данные из указанного файла и возвращает словарь с разделением людей по типу оплаты.
        :param file_path: полный путь к файлу
        :return: словарь, где каждый ключ представляет тип оплаты, а каждое значение является списком словарей с 
        информацией о человеке.
    """
    def __parse_file(self, file_path: str) -> dict:

        # Создание словаря для хранения информации о людях с разделением по типу оплаты
        data = {
            'cash': [],
            'pos': [],
            'cards': [],
            'NA': []
        }
        # Считывание содержимого файла и сохранение в переменной file_content
        file_content = read_file_and_return_list.open_file(file_path)
        # Создание индекса, который будет использоваться в качестве id для каждого человека
        index = 1
        # Проход по каждой строке файла
        for line in file_content:
            # Разделение строки на список данных о человеке
            person = line.split(";")
            # Извлечение имени и фамилии из данных о человеке
            name_last_name = person[4].split(' ')
            name = name_last_name[1]
            full_name = person[4]
            # Извлечение метода оплаты из данных о человеке
            pay_method = person[7]
            # Извлечение даты рождения из данных о человеке и определение возраста
            birth_day = person[8]
            age = self.__get_person_age(birth_day)
            # Извлечение номера телефона из данных о человеке и нормализация номера
            phone_number = person[0]
            normalize_phone_number = self.__normalize_phone_number(phone_number)
            # Если номер телефона невалиден, то человек помечается как "NA" (not available)
            if normalize_phone_number == '':
                pay_method = 'NA'
                normalize_phone_number = phone_number
                person = {
                    'id': index,
                    'name': f'{name} {name_last_name[2]}',
                    'phone': normalize_phone_number,
                    'payMethod': pay_method
                }
            else:
                # Добавление данных о человеке в соответствующий список в словаре data
                list_len = len(data[pay_method]) + 1
                person = {
                    'id': list_len,
                    'fullName': full_name,
                    'phone': normalize_phone_number,
                    'birthYear': birth_day,
                    'age': age,
                    'payMethod': pay_method
                }
            # Увеличение индекса на 1 после каждой итерации цикла
            index += 1
            # Добавление данных о человеке в соответствующий список в словаре data
            data[pay_method].append(person)
        # Возврат словаря с данными о людях с разделением по типу оплаты
        return data

    """
        Функция __normalize_phone_number(self, phone_number: str) -> str
        принимает строку, представляющую телефонный номер, и возвращает строку,
        представляющую нормализованный телефонный номер, содержащий только цифры.
    """
    def __normalize_phone_number(self, phone_number: str) -> str:

        # Оставляем в строке только цифры
        digits = re.sub('[^0-9]', "", phone_number)
        # Если количество цифр соответствует заданному количеству, то возвращаем нормализованный номер
        if len(digits) == self.phone_number_len:
            return digits
        # В противном случае возвращаем пустую строку
        else:
            return ''

    """Функция принимает день рождения в формате строки "день.месяц.год" и возвращает полный возраст человека в 
    годах, месяцах и днях. Аргументы: birth_day (str): Строка, содержащая день рождения в формате "день.месяц.год". 
    Возвращает: str: Строка, содержащая полный возраст человека в годах, месяцах и днях. """
    def __get_person_age(self, birth_day: str) -> str:
        # Преобразование строки дня рождения в объект даты
        birth_date = datetime.datetime.strptime(birth_day, '%d.%m.%Y').date()

        # Получение текущей даты
        current_date = datetime.date.today()

        # Вычисление временной разницы между датами
        age_timedelta = current_date - birth_date

        # Вычисление полных лет
        age_years = age_timedelta.days // 365

        # Вычисление полных месяцев
        age_months = (age_timedelta.days % 365) // 30

        # Вычисление оставшихся дней
        age_days = (age_timedelta.days % 365) % 30

        # Формирование строки с результатом
        return f"{age_years} Год, {age_months} Месяцев и {age_days} Дней"

    def get_data(self):
        return self.data

    """
        Функция сохраняет данные из словаря в текстовые файлы в указанную директорию.
        :param data: словарь, содержащий списки людей с разными способами оплаты
        :param output_folder: директория для сохранения файлов
        :return: список полных путей сохраненных файлов
    """
    def __save_files(self, data: dict, output_folder: str):
        # Итерация по элементам словаря с данными
        for key, dictionary in data.items():
            # Если ключ соответствует списку cash, cards или pos
            if key == 'cash' or key == 'cards' or key == 'pos':
                # Создание имени файла из названия ключа и суффикса файла
                filename = os.path.join(os.path.expanduser('~'), output_folder,
                                        key + self.file_suffix)

                # Открытие файла для записи
                with open(filename, 'w') as f:
                    # Запись каждого элемента списка из словаря в отдельной строке файла
                    for item in dictionary:
                        f.write('%s\n' % item)
