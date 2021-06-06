import requests


class SuperHero:
    __token = '2619421814940190'
    __url = f'https://superheroapi.com/api/{__token}/search'

    def __init__(self, name):
        self.name = name
        response = requests.get(f'{SuperHero.__url}/{self.name}')
        if response.status_code != 200:
            raise RuntimeError(f"Ошибка при получение ответа код: {response.status_code}")
        self.info = response.json()['results'][0]

    def get_power_stat(self, stat_name):
        powerstats = self.info['powerstats']
        if stat_name not in powerstats:
            raise ValueError(f"нет такого стата {stat_name}")
        return powerstats[stat_name]

    def __str__(self):
        return self.name


if __name__ == "__main__":
    Hulk = SuperHero('Hulk')
    Captain = SuperHero('Captain America')
    Thanos = SuperHero('Thanos')

    hero_list = [Hulk, Captain, Thanos]

    most_clever = sorted(hero_list, key=lambda hero: hero.get_power_stat('intelligence'))[0]
    print(most_clever)
