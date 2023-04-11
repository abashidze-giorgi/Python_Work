import FileServices


file_service = FileServices

downloaded_file = file_service.File_Services.Download_File('https://lk.globtelecom.ru/upload/test_prog1.csv', 'test_prog1.csv')
file_content = file_service.File_Services.Read_File(downloaded_file)

if __name__ == '__mane__':
    pass
