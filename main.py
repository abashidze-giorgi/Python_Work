from file_service import FileWork
from data_analysis import DataAnalysis
import os

output_foleder_name = "Documents\\my_output_folder"
file_name = 'https://lk.globtelecom.ru/upload/test_prog1.csv'


if __name__ == '__main__':
    #
    output_dir = os.path.join(os.path.expanduser('~'), output_foleder_name)
    file_work = FileWork(file_name, output_dir)

    data = file_work.get_data()
    DataAnalysis(data)
