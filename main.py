import telebot
import os
import json
import schedule
import time
import threading
import datetime

bot = telebot.TeleBot(os.getenv('BOT_TOKEN'))
json_dir = "./users.json"
deadline = [20, 30] #POMENYAT SUKA NE ZABUD'


@bot.message_handler(commands=['start'])
def start(message):
    create_user(message.chat.id)
    bot.send_message(message.chat.id, "Привет! Я буду напоминать тебе о показаниях счетчика")


@bot.message_handler(commands=['done'])
def done(message):
    reset_user(message.chat.id)
    bot.send_message(message.chat.id, "Отлично! До следующего месяца")


def create_user(id):
    with open(json_dir) as f:
        data = json.load(f)

    exist = False
    for user in data["users"]:
        if user["id"] == id:
            user["remind"] = True
            exist = True

    if not exist:
        data["users"].append({"id": id, "remind": True})
    with open(json_dir, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def reset_user(id):
    with open(json_dir) as f:
        data = json.load(f)

    for user in data["users"]:
        if user["id"] == id:
            user["remind"] = False
    with open(json_dir, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)


def get_users():
    with open(json_dir) as f:
        data = json.load(f)

    return data["users"]

def remind():
    day = datetime.datetime.now().strftime("%d")
    print(day)
    if int(day) > deadline[0] and int(day) < deadline[1]:
        users = get_users()
        for user in users:
            if user["remind"]:
                bot.send_message(user["id"], "А ты не забыл отправить показания?")
    
    if day == 1:
        users = get_users()
        for user in users:
            create_user(user["id"])


def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)


schedule.every().day.at("14:17").do(remind)
# schedule.every(1).minutes.do(remind)

if __name__ == "__main__":
    x = threading.Thread(target=run_schedule)
    x.start()
    bot.polling(none_stop=True)
    x.join()