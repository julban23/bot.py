import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# STRATZ API URL
STRATZ_API_URL = "https://api.stratz.com/api/v1/hero-meta"
STRATZ_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYjZhNjQ1NjEtNTgyZi00MTc1LTk3NjgtYjdmNjUxNGMwYWYzIiwiU3RlYW1JZCI6Ijc2MzUyOTU1IiwibmJmIjoxNzQzNDg5MTY2LCJleHAiOjE3NzUwMjUxNjYsImlhdCI6MTc0MzQ4OTE2NiwiaXNzIjoiaHR0cHM6Ly9hcGkuc3RyYXR6LmNvbSJ9.eg_iaj1BXJfRyv6dt4nFbWpEtEeseeOnElvtxcbZK50'

# Заголовки для авторизации
headers = {
    "Authorization": f"Bearer {STRATZ_API_KEY}"
}

def get_meta_from_stratz():
    response = requests.get(STRATZ_API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        meta = {
            "top": [],
            "mid": [],
            "bot": [],
        }
        for hero in data:
            if hero['lane'] == "top":
                meta["top"].append(hero['name'])
            elif hero['lane'] == "mid":
                meta["mid"].append(hero['name'])
            elif hero['lane'] == "bottom":
                meta["bot"].append(hero['name'])
        return meta
    else:
        return None

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Привет! Я помогу выбрать героя для Dota 2 по текущей мете.\n"
                              "Введите команду /hero, чтобы получить героя для своей линии.")

def hero(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Для какой линии вам нужно выбрать героя? Напишите 'top', 'mid' или 'bot'.")

def counterpick(update: Update, context: CallbackContext) -> None:
    update.message.reply_text("Введите имя героя противника на английском языке, и я предложу контрпик.")

def line(update: Update, context: CallbackContext) -> None:
    meta = get_meta_from_stratz()
    if not meta:
        update.message.reply_text("Не удалось получить актуальную мету.")
        return
    line_choice = update.message.text.lower().strip()
    if line_choice in meta:
        heroes = meta[line_choice]
        hero_list = "\n".join(heroes)
        update.message.reply_text(f"Вот герои для линии {line_choice.capitalize()}:\n{hero_list}\n\n"
                                  "Теперь напишите героя противника, чтобы я предложил контрпики.")
    else:
        update.message.reply_text("Я не понимаю эту линию. Напишите 'top', 'mid' или 'bot'.")

def get_counterpick(update: Update, context: CallbackContext) -> None:
    opponent_hero = update.message.text.strip()
    counterpicks = {
        "Anti-Mage": ["Legion Commander", "Axe", "Silencer"],
        "Invoker": ["Anti-Mage", "Naga Siren", "Tinker"],
        "Tinker": ["Silencer", "Viper", "Necrophos"],
        "Dazzle": ["Lion", "Silencer", "Pugna"],
    }
    if opponent_hero in counterpicks:
        counters = counterpicks[opponent_hero]
        counter_list = "\n".join(counters)
        update.message.reply_text(f"Контрпики для {opponent_hero}:\n{counter_list}")
    else:
        update.message.reply_text(f"Извините, у меня нет информации о контрпиках для {opponent_hero}.")

def main() -> None:
    token = 'YOUR_BOT_API_TOKEN'  # Токен для бота
    updater = Updater(token)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("hero", hero))
    dispatcher.add_handler(CommandHandler("counterpick", counterpick))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, line))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, get_counterpick))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
