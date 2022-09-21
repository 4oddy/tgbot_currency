import os
import json

from exceptions import CacheExpired, CacheEmpty
from utils import get_current_date


class CacheManager:
    def __init__(self, cache_file_name: str = 'cache.json'):
        self.file_name = cache_file_name
        self._time_stamp_name = 'datetime'

    def set_cache(self, data: dict) -> dict:
        """ Method to set cache
            Takes one positional argument: data [dict]
        """
        data[self._time_stamp_name] = get_current_date()

        with open(self.file_name, 'w') as file:
            json.dump(data, file)

        return data

    def get_cache(self) -> dict:
        """ Method to get cache """
        if os.path.exists(self.file_name):
            with open(self.file_name, 'r') as file:
                cache = json.load(file)

                # if there is not only date in cache
                if len(cache.keys()) > 1:
                    if cache[self._time_stamp_name] != get_current_date():
                        raise CacheExpired('Cache has been expired')
                else:
                    raise CacheEmpty('Cache is empty')

        else:
            self.set_cache({})
            cache = self.get_cache()

        return cache
