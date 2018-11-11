import requests
import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

updater = Updater(token="768912317:AAEp51lJL9IniuEVEtjjZRShJBreVSXz2f8")
dispatcher = updater.dispatcher

print("Bot is alive")


def get_answer(text) -> str:
    url = "https://7b68ccdb.ngrok.io/send_message"
    response_text = {"message": text}
    print("LOG[JSON.QUERY]: " + str(json.dumps(response_text)))
    question = requests.post(url=url, data=response_text)
    response = question.json()
    print("LOG[JSON.RESPONSE]: " + str(response) + " " + str(question) + "\n")
    return response['message']


def json_string_to_dict(text: str) -> dict:
    text_entities = text.strip('{}').split(",")
    string_dict = {}
    for i in text_entities:
        temp = i.split(":")
        string_dict.update({temp[0].lstrip(" \"").rstrip("\" "): temp[1].strip().lstrip(" \"").rstrip("\" ")})
    return string_dict


def text_message(bot, update):
    message = update.message
    chat_id = update.message.chat_id
    temp_text = str(message.text).lower()
    answer = get_answer(temp_text)

    if not answer.find("Type") == -1:
        answer_dict = json.loads(answer)
        if answer_dict["Type"] == "film":
            film_description = "Фильм: " + answer_dict["Title"] + "\n" + \
                               "Дата релиза: " + answer_dict["Released"] + "\n" + \
                               "Трейлер: " + answer_dict["Video"] + "\n" + \
                               "Постер: " + answer_dict["Poster"] + "\n" + \
                               "Описание: " + answer_dict["Tagline"] + "\n" + \
                               "Рейтинг: " + answer_dict["Score"] + "\n" + \
                               "В прокате: " + answer_dict["Status"].replace("true", "Да").replace("false",
                                                                                                   "Нет") + "\n"
            if answer_dict["Status"] == "true":
                keyboard = [[InlineKeyboardButton('Купить билеты:', url='https://karofilm.ru/theatres/26')]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                update.message.reply_text(film_description, reply_markup=reply_markup)
            else:
                bot.send_message(chat_id=chat_id, text=film_description)
        elif answer_dict["Type"] == "location":
            bot.send_message(chat_id=chat_id, text="Вот несколько банкоматов поблизости:")
            bot.send_location(chat_id=chat_id, latitude=55.780311, longitude=49.133646, live_period=80)
            bot.send_location(chat_id=chat_id, latitude=55.779603, longitude=49.135085, live_period=80)
        elif answer_dict["Type"] == 'auto':
            bot.send_message(chat_id=update.message.chat_id, text="Вот несколько наших автосалонов поблизости")
            bot.send_message(chat_id=update.message.chat_id, text="Московская ул., 20, Казань, Респ. Татарстан, 420111")
            bot.send_location(chat_id=update.message.chat_id, latitude=55.7906596, longitude=49.1052328, live_period=80)
            bot.send_message(chat_id=update.message.chat_id, text="Казань, Респ. Татарстан, 420061")
            bot.send_location(chat_id=update.message.chat_id, latitude=55.7967087, longitude=49.1912644, live_period=80)
            bot.send_message(chat_id=update.message.chat_id,
                             text="ул. Габдуллы Тукая, 115 корпус 3, Казань, Респ. Татарстан")
            bot.send_location(chat_id=update.message.chat_id, latitude=55.766002, longitude=49.1269089, live_period=80)
        elif answer_dict["Type"] == "Kasko":
            bot.send_message(text="Информация о КАСКО: ", url='https://goo.gl/bbihY9')
        elif answer_dict["Type"] == "Osago":
            bot.send_message(text="Информация об ОСАГО: ", url='https://goo.gl/ngmzCH')
        elif answer_dict["Type"] == "ticket":
            bot.send_message(chat_id=chat_id, text="Origin:" + answer_dict["Origin"] + "\n" +
                                                   "Destination:" + answer_dict["Destination"] + "\n" +
                                                   "Price:" + answer_dict["Price"])
            bot.send_message(chat_id=chat_id,
                             text="Вы можете застраховать себя от несчастных случаев, потери багажа и задержки рейса" + "\n"
                                  + "Узнать больше: ", url='https://sgabs.ru/products/pilgrim.php')
        else:
            bot.send_message(chat_id=chat_id, text=answer_dict)
    else:
        bot.send_message(chat_id=chat_id, text=str(answer))


def start_command(bot, update):
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text='Привет! Чем могу помочь?')


start_command_handler = CommandHandler('start', start_command)
text_message_handler = MessageHandler(Filters.text, text_message)

dispatcher.add_handler(text_message_handler)
dispatcher.add_handler(start_command_handler)

updater.start_polling(clean=True)