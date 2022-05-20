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
                         "\n2) Курс доллара в рублях\n3) Курс евро в рублях",
        "all": ["1", "2", "3"],
        "dollar_exchange_rate": "Курс доллара: {0}₽\nДанные от: {1}",
        "euro_exchange_rate": "Курс евро: {0}₽\nДанные от: {1}"
    },
    "errors": {
        "unknown_command": "Я не знаю такой команды! Пропиши /help для списка команд"
    }
}

bot = telebot.TeleBot(TOKEN)


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
            bot.send_message(message.chat.id, "Не удалось найти заданную валюту!")

    # dollar rate
    elif message.text == "2":
        result = RussianCurrencyManager.dollar_euro_exchange_rate("USD")
        bot.send_message(message.chat.id,
                         bot_func_mapper["commands"]["dollar_exchange_rate"].format(result["exchange_rate"],
                                                                                    result["date"]))
    # euro rate
    elif message.text == "3":
        result = RussianCurrencyManager.dollar_euro_exchange_rate("EUR")
        bot.send_message(message.chat.id,
                         bot_func_mapper["commands"]["euro_exchange_rate"].format(result["exchange_rate"],
                                                                                  result["date"]))

    else:
        bot.send_message(message.chat.id, bot_func_mapper["errors"]["unknown_command"])


if __name__ == '__main__':
    bot.infinity_polling()
