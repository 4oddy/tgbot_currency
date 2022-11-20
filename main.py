import os
import telebot
from dotenv import load_dotenv
from currency import RussianCurrencyManager

from exceptions import CurrencyDoesNotExist


load_dotenv("token.env")

# loads token from current env
TOKEN = os.environ.get("token")

# Useful dictionary to map all funcs
bot_func_mapper = {
    "commands": {
        "all_with_text": "Вот мои команды:\n1) Перевести валюту (формат: /ex [значение] USD EUR)\n"
                         "2) Курс доллара (формат: /usd [значение]\n"
                         "3) Курс евро (формат: /eur [значение]",
        "all": ["1", "2", "3"],
    },
    "errors": {
        "unknown_currency": "Не удалось найти заданную валюту!",
        "error": "Произошла ошибка!",
    }
}

bot = telebot.TeleBot(TOKEN)


def parse_for_exchange(data: list) -> dict:
    value = float(data[1])
    from_this = data[2].upper()
    to_this = data[3].upper()
    return {'value': value, 'from_this': from_this, 'to_this': to_this}


# /start command reply
@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.chat.username
    msg = f"Привет, {user}\nВведи /help для списка команд"
    bot.send_message(message.chat.id, msg)


# /help command reply
@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, bot_func_mapper["commands"]["all_with_text"])


@bot.message_handler(commands=['ex'])
def exchange_command(message):
    try:
        data = parse_for_exchange(message.text.split())
    except Exception:
        bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])
    else:
        try:
            output = RussianCurrencyManager.exchange_currency(**data)
            bot.send_message(message.chat.id, f"{data['value']} {data['from_this']}"
                                              f" = {output} {data['to_this']}")
        except CurrencyDoesNotExist:
            bot.send_message(message.chat.id, bot_func_mapper["errors"]["unknown_currency"])


@bot.message_handler(commands=['usd'])
def usd_rate(message):
    data = message.text.split()

    try:
        value = float(data[1])
        result = RussianCurrencyManager.dollar_exchange_rate(value)
        bot.send_message(message.chat.id, f"{value} USD = {result} RUB")
    except Exception:
        bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])


@bot.message_handler(commands=['eur'])
def euro_rate(message):
    data = message.text.split()

    try:
        value = float(data[1])
        result = RussianCurrencyManager.euro_exchange_rate(value)
        bot.send_message(message.chat.id, f"{value} EUR = {result} RUB")
    except Exception:
        bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])


if __name__ == '__main__':
    bot.infinity_polling()
