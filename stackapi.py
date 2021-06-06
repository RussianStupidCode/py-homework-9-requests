import requests
from datetime import datetime

STACK_API_URL = 'https://api.stackexchange.com/2.2/questions'


def date_to_seconds(date):
    delta = (date - datetime(1970, 1, 1))
    return int(delta.total_seconds())


def params(date):
    to_date = date_to_seconds(date)
    from_date = to_date - 48 * 3600

    result = {
        'order': 'desc',
        'sort': 'activity',
        'tagged': 'Python',
        'site': 'stackoverflow',
        'to_date': to_date,
        'from_date': from_date,
    }

    return result


if __name__ == "__main__":
    current_date = datetime.now()
    response = requests.get(STACK_API_URL, params=params(current_date))
    print(response.json())
