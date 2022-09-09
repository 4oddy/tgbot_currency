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
        "all_with_text": "Вот мои команды:\n1) Перевести валюту (формат: 1 [значение - необязательно] USD EUR)\n"
                         "2) Курс доллара (формат: 2 [значение - необязательно]\n"
                         "3) Курс евро (формат: 3 [значение - необязательно]",
        "all": ["1", "2", "3"],
    },
    "errors": {
        "unknown_command": "Я не знаю такой команды! Пропиши /help для списка команд",
        "unknown_currency": "Не удалось найти заданную валюту!",
        "error": "Произошла ошибка!"
    }
}

bot = telebot.TeleBot(TOKEN)


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


# reply for inputted command
@bot.message_handler(content_types=["text"])
def get_message(message):
    # translate currency
    if message.text[0] in bot_func_mapper["commands"]["all"]:
        if message.text[0] == "1" and len(message.text.split()) > 2:
            data = message.text.split()

            value = None

            if len(data) > 3:
                # if value is defined
                try:
                    value = float(data[1])
                except Exception:
                    bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])

                first_currency = data[2].upper()
                second_currency = data[3].upper()
            else:
                first_currency = data[1].upper()
                second_currency = data[2].upper()

            try:
                result = RussianCurrencyManager.exchange_currency(first_currency, second_currency, value)
                bot.send_message(message.chat.id, f"{value if value else 1} {first_currency}"
                                                f" = {result} {second_currency}")
            except Exception:
                bot.send_message(message.chat.id, bot_func_mapper["errors"]["unknown_currency"])

        elif message.text[0] == "2":
            data = message.text.split()

            value = None

            if len(data) > 1:
                try:
                    value = float(data[1])
                except Exception:
                    bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])

            try:
                result = RussianCurrencyManager.dollar_exchange_rate(value)
                bot.send_message(message.chat.id, f"{value if value else 1} USD = {result} RUB")
            except Exception:
                bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])

        elif message.text[0] == "3":
            data = message.text.split()

            value = None

            if len(data) > 1:
                try:
                    value = float(data[1])
                except Exception:
                    bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])

            try:
                result = RussianCurrencyManager.euro_exchange_rate(value)
                bot.send_message(message.chat.id, f"{value if value else 1} EUR = {result} RUB")
            except Exception:
                bot.send_message(message.chat.id, bot_func_mapper["errors"]["error"])

        else:
            bot.send_message(message.chat.id, bot_func_mapper["errors"]["unknown_command"])

    else:
        bot.send_message(message.chat.id, bot_func_mapper["errors"]["unknown_command"])


if __name__ == '__main__':
    bot.infinity_polling()
