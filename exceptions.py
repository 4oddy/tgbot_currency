class CacheExpired(Exception):
    """ Exception generates when cache has been expired """
    pass


class CacheEmpty(Exception):
    """ Exception generates when cache is empty """
    pass


class CurrencyDoesNotExist(Exception):
    """ Exception generates when currency is not found """
    pass
