import telebot
from config import keys, TOKEN
from utils import CryptoConverter, ConvertionException
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введи запрос боту в следующем формате: \n<название валюты> \
<в какую валюту необходимо перевести> \
<количество переводимой валюты> \
<например: доллар рубль 120> \nЧтобы увидеть список всех доступных валют задай команду: /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text,key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=["text",])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    if len(values) != 3:
        raise ConvertionException('Указаны неверные данные, должно быть ровно три значения, как в примере')

    # quote, base, amount = message.text.split(' ')
    quote, base, amount = values
    total_base = CryptoConverter.convert(quote, base, amount)


    text = f'Стоимость {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()