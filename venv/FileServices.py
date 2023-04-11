import urllib.request
import os


class File_Services:

    def Download_File(file_path: str, file_name: str) -> str:
        url = file_path
        file_name = os.path.join(os.path.expanduser('~'), 'Downloads', file_name)
        urllib.request.urlretrieve(url, file_name)
        return file_name

    def Read_File(file_name: str) -> str:
        content = ''
        with open(file_name, 'r') as file:
            content = file.read()

        #print(type(content))
        return content

if __name__ == '__main__':
    file_service = FileServices

    downloaded_file = file_service.Download_File('https://lk.globtelecom.ru/upload/test_prog1.csv', 'test_prog1.csv')

    file_content = file_service.Read_File(downloaded_file)

