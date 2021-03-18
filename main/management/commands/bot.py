import telebot
from main.MyToken import token
from telebot import types
from main.models import Post
from main.serializers import PostSerializer, ParsSerializer
from main.pars import main

bot = telebot.TeleBot(token)


def get():
    dict_ = main()
    serializer = ParsSerializer(instance=dict_, many=True).data
    return serializer


income_keyboard = types.InlineKeyboardMarkup()

reply_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
btn1 = types.KeyboardButton('Да')
btn2 = types.KeyboardButton('Нет')
reply_keyboard.add(btn1, btn2)


@bot.message_handler(commands=['start'])
def start(message):
    chat_id = message.chat.id
    msg = bot.send_message(chat_id, 'Хэээй, привет! \nНовости уже ждут тебя! Хочешь на них взглянуть?', reply_markup=reply_keyboard)
    bot.register_next_step_handler(msg, get_inline)


def get_inline(c):
    # chat_id = c.chat.id
    if c.text == 'Да':
        # chat_id = c.chat.id
        index = 1
        list_ = get()
        for list_elem in list_:
            print(list_elem)
            bot.send_message(c.chat.id,
                             f'Новости {list_elem[0]} \n Фото: {list_elem[1]} \n')
    if c.text == 'Нет':
        bot.send_message(c.chat.id, 'эх..')


bot.polling()



