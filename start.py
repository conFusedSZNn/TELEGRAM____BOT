import telebot
from config import TOKEN, keys
from extensions import TONconverter, APIExeption



bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=["start", "help"])
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следующем формате: \n \
<имя валюты, цену которой он хочет узнать> \n \
<имя валюты, в которой надо узнать цену первой валюты> \n \
<количество первой валюты>\n \
Вводите данные через пробел\n Чтобы увидеть список доступных валют:\n /values"
    bot.reply_to(message, text)



@bot.message_handler(commands=["values"])
def values(message: telebot.types.Message):
    text = "Список доступных валют:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)



@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')
        if len(values) > 3:
            raise APIExeption('Слишком много параметров')
        if len(values) < 3:
            raise APIExeption('Слишком мало параметров')
        quote, base, amount = values
        total_base = TONconverter.convert(quote, base, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base}'
        bot.send_message(message.chat.id, text )
bot.polling()
