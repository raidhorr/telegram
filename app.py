import telebot
from yaml import safe_load

from extensions import Currency, APIException

with open('config.yaml') as cfg:
    config = safe_load(cfg)
curr = Currency(config['url'])

bot = telebot.TeleBot(config['token'])


@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message):
    text = 'Чтобы начать работу введите команду боту в следующем формате\n '
    text += '<имя валюты продажи> <имя валюты покупки> <количество валюты продажи>\n'
    text += 'где в качестве имени валюты используется международный код валюты\n'
    text += '\n'
    text += 'Примеры:\n USD RUB 100\nRUB UAH 80000\n'
    text += '\n'
    text += 'Просмотр списка валют: \n/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def handle_start_help(message):
    text = curr.get_valute()
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message):
    try:
        params = message.text.split()
        if len(params) != 3:
            raise APIException('Не правильное количество параметров\n')
        base, quote, amount = params
        base = base.upper()
        quote = quote.upper()
        try:
            amount = float(amount)
        except ValueError:
            raise APIException('не числовое количество\n')
        sm = curr.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода: {e}\n')
    except Exception as e:
        bot.reply_to(message, 'Не удалось обработать команду: {e}\n')
    else:
        bot.reply_to(message, f'ЦЕНА за {amount} {base} {sm:.2f} {quote}')

bot.polling(none_stop=True)