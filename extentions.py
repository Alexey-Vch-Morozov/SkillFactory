import requests
import json
from config import KEY, keys


class ConvertionException(Exception):
    pass


class Converter:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно перевести одинаковые валюты {base}.')
        if base not in list(keys) or quote not in list(keys):
            raise ConvertionException(f'Ошибка в написании названия валюты {base}, {quote}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}.')

#Бесплатный доступ к API не позволяет ни использовать Convert Endpoint ни менять базовую валюту евро на что-то другое
#Поэтому запрос всегда одинаковый - получить отношение евро к доллару и евро к рублю

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={KEY}&symbols=USD,RUB')
        result = json.loads(r.content)
# result = {'success': True, 'timestamp': 1649660823, 'base': 'EUR', 'date': '2022-04-11',
# 'rates': {'USD': 1.0881, 'RUB': 88.951615}}
        EUR_to_RUB = result['rates']['RUB']
        EUR_to_USD = result['rates']['USD']
        if quote == 'евро':
            if base == 'рубль':
                total_base = EUR_to_RUB * amount
            elif base == 'доллар':
                total_base = EUR_to_USD * amount
        if quote == 'доллар':
            if base == 'рубль':
                total_base = EUR_to_RUB / EUR_to_USD * amount
            elif base == 'евро':
                total_base = 1 / EUR_to_USD * amount
        if quote == 'рубль':
            if base == 'евро':
                total_base = 1 / EUR_to_RUB * amount
            elif base == 'доллар':
                total_base = EUR_to_USD / EUR_to_RUB * amount

        return total_base
