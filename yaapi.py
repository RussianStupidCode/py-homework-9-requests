import requests
import os


class YaUploader:
    __base_url = 'https://cloud-api.yandex.net/v1/disk'
    __prefix = 'disk:'

    def __init__(self, token: str):
        self.token = token
        self.headers = {'Authorization': self.token}

    def __get_url_for_load(self, file_name: str):
        """Получение адреса для загрузки файла"""

        params = {'path': file_name}
        resp = requests.get(f'{YaUploader.__base_url}/resources/upload', headers=self.headers, params=params)

        text = resp.json()
        if resp.status_code != 200:
            raise ValueError(text['message'])

        return text['href']

    def make_directory(self, dir_path):
        """Создание дирректории на я.диске"""

        dir_path = dir_path.strip().strip("/")
        params = {'path': dir_path}
        resp = requests.put(f'{YaUploader.__base_url}/resources', headers=self.headers, params=params)

        text = resp.json()
        if resp.status_code != 201:
            raise ValueError(text['message'])
        return 'Директория создана успешно'

    def upload(self, file_path: str, dir_path=""):
        """Метод загружает файл с базоввым именнем на яндекс диск"""

        file_name = os.path.basename(file_path)

        try:
            file = open(file_path, 'rb')
            file_content = file.read()
            file.close()
        except:
            return f'ошибка открытия файла {file_path}'

        normalize_path = f'{dir_path.strip().strip("/")}'
        ya_dir_path = f'{normalize_path}/{file_name}'
        print(ya_dir_path)

        try:
            href = self.__get_url_for_load(ya_dir_path)
            resp = requests.put(href, headers=self.headers, data=file_content)
        except ValueError as error:
            return error

        if resp.status_code != 201:
            text = resp.json()
            return text['message']

        return 'Файл создан успешно'

    def disk_info(self):
        resp = requests.get(f'{YaUploader.__base_url}/', headers=self.headers)
        if resp.status_code != 200:
            raise ValueError(f'ошибка при ответе: {resp.status_code}')

        return resp.json()


if __name__ == '__main__':
    try:
        from mytoken import TOKEN

        uploader = YaUploader(TOKEN)
        print(uploader.upload('./requirements.txt'))
    except ImportError:
        pass
