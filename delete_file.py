import os


def delete_file(filepath: str):
    # Проверьте, существует ли файл
    if os.path.exists(filepath):
        # Удалить файл
        os.remove(filepath)
        #print('File -', filepath, 'deleted.')