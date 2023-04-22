from foo import FileWork
import os

output_foleder_name = "Documents\\my_output_folder"
file_name = 'https://lk.globtelecom.ru/upload/test_prog1.csv'

if __name__ == '__main__':
    #output_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder')
    output_dir = os.path.join(os.path.expanduser('~'), output_foleder_name)
    file_list = FileWork(file_name, output_dir)



    # output_dir = os.path.join(os.path.expanduser('~'), 'Documents', 'my_output_folder')
    # os.makedirs(output_dir, exist_ok=True)
    # file_name = services.download_file('https://lk.globtelecom.ru/upload/test_prog1.csv', output_dir)
    # encoding = services.determine_encoding(file_name)
    # data = DataService.parse_file(file_name, encoding)
    # new_files = DataService.diversification_data_and_save_files(data, encoding)
    # DataService.print_non_unique_phone_numbers(new_files, encoding)
    # services.delete_file(file_name)