import os
import telebot
from dotenv import load_dotenv
from currency import RussianCurrencyManager

load_dotenv("token.env")

# loads token from current env
TOKEN = os.environ.get("token")

# Useful dictionary to map all funcs
bot_func_mapper = {
    "commands": {
        "all_with_text": "Вот мои команды:\n1) Перевести валюту (формат: 1 [значение - необяз.] USD EUR)"
                         "\n2) Курс доллара в рублях (формат: 2 [значение - необяз.]\n3) Курс евро в рублях"
                         " (формат: 3 [значение - необяз.]",
        "all": ["1", "2", "3"],
        "dollar_exchange_rate": "{0} USD = {1}₽\nДанные от: {2}",
        "euro_exchange_rate": "{0} EUR = {1}₽\nДанные от: {2}"
    },
    "errors": {
        "unknown_command": "Я не знаю такой команды! Пропиши /help для списка команд",
        "unknown_currency": "Не удалось найти заданную валюту!",
        "error": "Произошла ошибка!"
    }
}

bot = telebot.TeleBot(TOKEN)


def get_currency_ex_rate(message, currency):
    if len(message.text.split()) == 1:
        value = 1
    else:
        msg = message.text.split()
        value = msg[1]

    result = RussianCurrencyManager.dollar_euro_exchange_rate(currency, value)

    return value, result


@bot.message_handler(commands=['start'])
def start_command(message):
    user = message.chat.username
    msg = f"Привет, {user}\nВведи /help для списка команд"
    bot.send_message(message.chat.id, msg)


# /help command reply
@bot.message_handler(commands=["help"])
def help_command(message):
    bot.send_message(message.chat.id, bot_func_mapper["commands"]["all_with_text"])


# reply for inputted command
@bot.message_handler(content_types=["text"])
def get_message(message):
    # exchange currency
    if message.text[0] == "1" and len(message.text.split()) > 2:
        data = message.text.split()
        if len(data) > 3:
            value = data[1]
            first_currency = data[2].upper()
            second_currency = data[3].upper()
        else:
            value = 1
            first_currency = data[1].upper()
            second_currency = data[2].upper()
        result = RussianCurrencyManager.exchange_currency(first_currency, second_currency, value)
        if result is not None:
            bot.send_message(message.chat.id, f"{value if value else 1} {first_currency}"
                                              f" = {result} {second_currency}")
        else:
            bot.send_message(message.chat.id, bot_func_mapper["errors"]["unknown_currency"])

    # dollar rate
    elif message.text[0] == "2":
        result = get_currency_ex_rate(message, "USD")

        value, result = result

        if result is not None:
            bot.send_message(message.chat.id,
                             bot_func_mapper["commands"]["dollar_exchange_rate"].format(value, result["exchange_rate"],
                                                                                        result["date"]))
        else:
            bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])

    # euro rate
    elif message.text[0] == "3":
        result = get_currency_ex_rate(message, "EUR")

        value, result = result

        if result is not None:
            bot.send_message(message.chat.id,
                             bot_func_mapper["commands"]["euro_exchange_rate"].format(value, result["exchange_rate"],
                                                                                      result["date"]))
        else:
            bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])

    else:
        bot.send_message(message.chat.id, bot_func_mapper["errors"]["unknown_command"])


if __name__ == '__main__':
    bot.infinity_polling()
