import requests
import os
from mytoken import TOKEN


class YaUploader:
    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': self.token}

    def __get_url(self, file_name: str):
        resp = requests.get('https://cloud-api.yandex.net/v1/disk/resources/upload',
                            headers=self.headers, params={'path': file_name})

        text = resp.json()
        if resp.status_code != 200:
            raise ValueError(text['message'])

        return text['href']

    def upload(self, file_path: str):
        """Метод загруджает файл file_path на яндекс диск"""

        file_name = os.path.basename(file_path)

        try:
            file = open(file_path, 'rb')
            file_content = file.read()
            file.close()
        except:
            return f'ошибка открытия файла {file_path}'

        try:
            href = self.__get_url(file_name)
            resp = requests.put(href, headers=self.headers, data=file_content)
        except ValueError as error:
            return error

        if resp.status_code != 201:
            return resp.json()['message']

        return 'Файл создан успешно'

    def disk_info(self):
        resp = requests.get('https://cloud-api.yandex.net:443', headers=self.headers)
        if resp.status_code != 200:
            raise ValueError(f'ошибка при ответе: {resp.status_code}')

        return resp.json()


if __name__ == '__main__':
    uploader = YaUploader(TOKEN)
    print(uploader.upload('./requirements.txt'))