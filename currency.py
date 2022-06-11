import os
import json
from datetime import datetime
import requests


class RussianCurrencyManager:
    # Russian central bank's API
    __URL = "https://www.cbr-xml-daily.ru/daily_json.js"

    @classmethod
    def dollar_exchange_rate(cls, value):
        try:
            value = float(value)
            result = cls.__load_dollar_exchange_rate()
            result["exchange_rate"] = round(result["exchange_rate"] * value, 2)

            return result
        except Exception:
            return None

    @classmethod
    def euro_exchange_rate(cls, value):
        try:
            value = float(value)
            result = cls.__load_euro_exchange_rate()
            result["exchange_rate"] = round(result["exchange_rate"] * value, 2)

            return result
        except Exception:
            return None

    @classmethod
    def exchange_currency(cls, from_this, to_this, value=1):
        """ Exchange currency method
            Takes three positional arguments: from_this, to_this and value (non required)
            Returns one currency (from_this) converted to another (to_this)
            List of all currencies: https://www.cbr-xml-daily.ru/daily_json.js
        """
        try:
            first_currency = cls.__get_exchange_rate(from_this)["exchange_rate"]
            second_currency = cls.__get_exchange_rate(to_this)["exchange_rate"]
            first_currency *= int(value)
            result = round(first_currency / second_currency, 2)
            return result
        except Exception:
            return None

    @classmethod
    def __get_exchange_rate(cls, currency):
        response = requests.get(cls.__URL).json()
        exchange_rate = response["Valute"][currency]["Value"]
        date = cls.__get_date_now()
        result = {"date": date, "exchange_rate": exchange_rate}
        return result

    @classmethod
    def __update_dollar_exchange_rate_cache(cls):
        with open("cache_dollar_exchange_rate.json", "w") as cache:
            data = cls.__get_exchange_rate("USD")
            json.dump(data, cache)

        return data

    @classmethod
    def __update_euro_exchange_rate_cache(cls):
        with open('cache_euro_exchange_rate.json', 'w') as cache:
            data = cls.__get_exchange_rate("EUR")
            json.dump(data, cache)

        return data

    @classmethod
    def __load_dollar_exchange_rate_cache(cls):
        with open("cache_dollar_exchange_rate.json", "r") as cache:
            data = json.load(cache)
        return data

    @classmethod
    def __load_euro_exchange_rate_cache(cls):
        with open("cache_euro_exchange_rate.json", "r") as cache:
            data = json.load(cache)
        return data

    @classmethod
    def __load_dollar_exchange_rate(cls):
        if os.path.exists("cache_dollar_exchange_rate.json"):
            data = cls.__load_dollar_exchange_rate_cache()
            if not data["date"] == cls.__get_date_now():
                data = cls.__update_dollar_exchange_rate_cache()
        else:
            data = cls.__update_dollar_exchange_rate_cache()

        return data

    @classmethod
    def __load_euro_exchange_rate(cls):
        if os.path.exists("cache_euro_exchange_rate.json"):
            data = cls.__load_euro_exchange_rate_cache()
            if not data["date"] == cls.__get_date_now():
                data = cls.__update_euro_exchange_rate_cache()
        else:
            data = cls.__update_euro_exchange_rate_cache()

        return data

    @classmethod
    def __get_date_now(cls):
        return datetime.now().strftime("%d.%m.%Y")
