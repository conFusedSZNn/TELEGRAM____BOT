import requests
import json
from config import keys



class APIExeption(Exception):
    pass



class TONconverter:
    @staticmethod
    def convert(quote: str, base: str, amount: str ):
        if quote == base:
            raise APIExeption(f'нельзя перевести одинаковые валюты {base}')
        try:
            quote_ticket = keys[quote]
        except KeyError:
            raise APIExeption(f'не удалось обработать валюту {quote} :/')
        try:
            base_ticket = keys[base]
        except KeyError:
            raise APIExeption(f'не удалось обработать валюту {base} :/')
        try:
            amount = float(amount)
        except ValueError:
            raise APIExeption(f'не удалось обработать количество {amount}')
        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticket}&tsyms={base_ticket}')
        total_base = json.loads(r.content)[keys[base]]
        return total_base
