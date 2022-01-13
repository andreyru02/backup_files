import os
import config
import yadisk


class YaUploader:
    def __init__(self, token_ya, path):
        self.token_ya = token_ya
        self.path = path
        self.file = os.listdir(self.path)
        self.ya = yadisk.YaDisk(token=self.token_ya)
        self.check_token()

    def check_token(self):
        """Проверяем валидацию токена"""
        if self.ya.check_token(self.token_ya) is not True:
            raise Exception('Token is not valid')

    def upload_to_yandex(self):
        """Метод загружает файл на яндекс диск"""
        if len(self.file) != 1:
            raise Exception('There is more than one file in the folder')

        self.ya.upload(f'{self.path}/{self.file[0]}', f'/{self.file[0]}', overwrite=True)
        print(f'File {self.file[0]} uploaded.')


if __name__ == '__main__':
    ya_upload = YaUploader(token_ya=config.TOKEN_YA_DISK, path='safe')
    ya_upload.upload_to_yandex()
