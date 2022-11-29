import telebot
from config import TOKEN,keys
from extensions import Converter,APIException

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения, содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду боту в следующем формате: \n<название валюты, из которой надо перевести> <в какую валюту перевести>  ' \
           '<количество переводимой валюты> \nСписок всех доступных валют доступе командой: /values'
    bot.reply_to(message, text)

#обработка команды '/values'
@bot.message_handler(commands=['values',])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

#обработка текстовых сообщений
@bot.message_handler(content_types=['text',])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров.')

        quote, base, amount = values
        total_base = Converter.get_price(quote,base,amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка ввода на стороне пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message,f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} - {total_base} {base}'
        bot.send_message(message.chat.id, text)



bot.polling(none_stop=True)

