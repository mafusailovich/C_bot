import requests
import json
from config import keys

class APIExceprion(Exception):
    pass

class Converter:

    @staticmethod
    def get_price(quote:str, base: str, amount:str):
        if quote == base:
            raise APIExceprion(f'Невозможно перевести одинаковые валюты в {base}')

        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIExceprion(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIExceprion(f'Не удалось обработать валюту {base}')

        try:
            amount = float(amount)
        except ValueError:
            raise APIExceprion(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://currate.ru/api/?get=rates&pairs={quote_ticker}{base_ticker}&key=12c53cc5c30d7dbfbe27fcea48fac5a2')
        total_base = json.loads(r.content)['data'][f'{quote_ticker}{base_ticker}']
        total_base = float(total_base) * float(amount)
        return total_base