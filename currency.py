import requests

from exceptions import CacheExpired, CacheEmpty, CurrencyDoesNotExist
from cache import CacheManager
from utils import get_current_date


class RussianCurrencyManager:
    # Russian central bank's API
    __URL = 'https://www.cbr-xml-daily.ru/daily_json.js'
    _cache_manager = CacheManager(cache_file_name='currency_cache.json')

    @classmethod
    def dollar_exchange_rate(cls, value: float | int = 1) -> float | int:
        rate = cls.__get_exchange_rate("USD")['exchange_rate'] * value
        return rate

    @classmethod
    def euro_exchange_rate(cls, value: float | int = 1) -> float | int:
        rate = cls.__get_exchange_rate("EUR")['exchange_rate'] * value
        return rate

    @classmethod
    def exchange_currency(cls, from_this: str, to_this: str, value: int = 1) -> float | int:
        """ Exchange currency method
            Takes three positional arguments: from_this, to_this and value (non required)
            Returns one currency (from_this) converted to another (to_this)
            List of all currencies: https://www.cbr-xml-daily.ru/daily_json.js
        """
        first_currency = cls.__get_exchange_rate(from_this)['exchange_rate'] * value
        second_currency = cls.__get_exchange_rate(to_this)['exchange_rate']
        result = round(first_currency / second_currency, 2)
        return result

    @classmethod
    def __get_exchange_rate(cls, currency: str) -> dict:
        date = get_current_date()

        try:
            cache = cls._cache_manager.get_cache()

            if currency not in cache['Valute']:
                raise CurrencyDoesNotExist(f'Currency {currency} does not exist')

            result = {'date': date, 'exchange_rate': cache['Valute'][currency]['Value']}

        except (CacheExpired, CacheEmpty):
            print('setting cache')
            cache = cls._cache_manager.set_cache(requests.get(cls.__URL).json())
            result = {'date': date, 'exchange_rate': cache['Valute'][currency]['Value']}

        return result
