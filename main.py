import os
from datetime import datetime
import config
import yadisk
import pyminizip


def clear_folder(path, name):
    """Удаление архива после загрузки на яндекс диск"""
    os.remove(f'{path}/{name}')
    return 'Архив удален.'


class Encrypt:
    """Класс архивирования файлов"""
    def __init__(self, password):
        self.password = password
        self.path_to_files = []

    def encrypt(self, path, files):
        """Архивирование файлов"""
        name = datetime.today().strftime(f'%Y%m%d-%H-%M-%S')
        self.path_to_files.clear()
        for file in files:
            self.path_to_files.append(f'{path}/{file}')

        pyminizip.compress_multiple(
            self.path_to_files,
            [],
            f'{path}/{name}.zip',
            self.password,
            5
        )
        print(f'Архив {name}.zip создан.')

        return f'{name}.zip'

    def delete_files(self):
        """Удаление файлов из папки после архивирования"""
        for file in self.path_to_files:
            os.remove(file)
        print('Файлы удалены после архивирования.')


class YaUploader(Encrypt):
    """Класс загрузки на яндекс диск"""
    def __init__(self, token_ya, path, password):
        super().__init__(password)
        self.token_ya = token_ya
        self.path = path
        self.files = os.listdir(self.path)
        self.ya = yadisk.YaDisk(token=self.token_ya)
        self.check_token()

    def check_token(self):
        """Проверяем валидацию токена"""
        if self.ya.check_token(self.token_ya) is not True:
            raise Exception('Токен недействителен')

    def upload_to_yandex(self):
        """Метод загружает файл на яндекс диск"""
        if len(self.files) == 0:
            raise Exception('Папка пуста.')
        name_archive = self.encrypt(self.path, self.files)
        self.delete_files()
        self.ya.upload(f'{self.path}/{name_archive}', f'/{name_archive}', overwrite=True)
        print(f'Файл {name_archive} загружен на яндекс диск.')
        print(clear_folder(self.path, name_archive))


if __name__ == '__main__':
    ya_upload = YaUploader(token_ya=config.TOKEN_YA_DISK, path='safe', password=config.PASSWORD)
    ya_upload.upload_to_yandex()
