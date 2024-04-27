from config import *
from telebot import TeleBot
from logic import DB_Manager
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

bot = TeleBot(TOKEN)

def gen_inline_markup(rows):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    for row in rows:
        markup.add(InlineKeyboardButton(row, callback_data=row))
    return markup

def gen_markup(rows):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 1
    for row in rows:
        markup.add(KeyboardButton(row))
    return markup

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id, """Привет! Я бот-менеджер футбольных мачтей 1872-2024 гг.!
Я помогу тебе узнать информацию о всех футбольных матчах с 1872 г. вплоть до 2024 г.!
""")
    info(message)
    
def info(message):
    bot.send_message(message.chat.id,
"""
Вот команды которые могут тебе помочь:

/goalscorer_date - узнайте информацию о забитых голах по дате(введите нужную дату)
/goalscorer_country - узнайте информацию о забитых голах по стране(введите нужную страну)
/result_date - узнайте все результаты любого матча по дате(введите нужную дату)
/result_country - узнайте все результаты любого матча по стране(введите нужную страну)

Также вы можете ввести имя футболиста и узнать информацию о нем!""")
    
attributes_of_result = {'Дата' : ["date"],
                          "Домашняя команда" : ["home_team"],
                          "Гостевая команда" : ["away_team"],
                          "Счет" : ["home_score", "away_score"],
                          "Турнир" : ["tournament"],
                          "Город" : ["city"],
                          "Страна" : ["country"],
                          "Нейтральный" : ["neutral"]}

@bot.message_handler(commands=['result_date'])
def reslt_date(message):
    bot.send_message(message.chat.id, "Введите дату матча(xxxx-xx-xx):")
    bot.register_next_step_handler(message, info_result)

def info_result(message):
    date = message.text
    info = manager.get_result_date(date)[0]
    bot.send_message(message.chat.id, f"""Date: {info[0]}
Home team: {info[1]}
Away team: {info[2]}
Home score: {info[3]}
Away score: {info[4]}
Tournament: {info[5]}
City: {info[6]}
Country: {info[7]}
Neutral: {info[8]}
""")

if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    bot.infinity_polling()