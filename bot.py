import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# Включаем логирование
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# STRATZ API URL
STRATZ_API_URL = "https://api.stratz.com/api/v1/hero-meta"
STRATZ_API_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJTdWJqZWN0IjoiYjZhNjQ1NjEtNTgyZi00MTc1LTk3NjgtYjdmNjUxNGMwYWYzIiwiU3RlYW1JZCI6Ijc2MzUyOTU1IiwibmJmIjoxNzQzNDg5MTY2LCJleHAiOjE3NzUwMjUxNjYsImlhdCI6MTc0MzQ4OTE2NiwiaXNzIjoiaHR0cHM6Ly9hcGkuc3RyYXR6LmNvbSJ9.eg_iaj1BXJfRyv6dt4nFbWpEtEeseeOnElvtxcbZK50'

# Заголовки для авторизации
headers = {
    "Authorization": f"Bearer {STRATZ_API_KEY}"
}

# Асинхронная функция старта
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Привет! Я помогу выбрать героя для Dota 2 по текущей мете.\n"
                                    "Введите команду /hero, чтобы получить героя для своей линии.")

# Асинхронная функция для получения героев по линии
async def hero(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Для какой линии вам нужно выбрать героя? Напишите 'top', 'mid' или 'bot'.")

# Функция для получения меты с API Stratz
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

# Функция для выбора линии
async def line(update: Update, context: CallbackContext) -> None:
    meta = get_meta_from_stratz()
    if not meta:
        await update.message.reply_text("Не удалось получить актуальную мету.")
        return
    line_choice = update.message.text.lower().strip()
    if line_choice in meta:
        heroes = meta[line_choice]
        hero_list = "\n".join(heroes)
        await update.message.reply_text(f"Вот герои для линии {line_choice.capitalize()}:\n{hero_list}\n\n"
                                       "Теперь напишите героя противника, чтобы я предложил контрпики.")
    else:
        await update.message.reply_text("Я не понимаю эту линию. Напишите 'top', 'mid' или 'bot'.")

# Функция для контрпиков
async def get_counterpick(update: Update, context: CallbackContext) -> None:
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
        await update.message.reply_text(f"Контрпики для {opponent_hero}:\n{counter_list}")
    else:
        await update.message.reply_text(f"Извините, у меня нет информации о контрпиках для {opponent_hero}.")

# Основная функция
def main() -> None:
    token = '8164777557:AAHLCs97peJ5C6mC2HegBxcTo8DN315aDP8'  # Токен для бота
    application = Application.builder().token(token).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("hero", hero))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, line))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_counterpick))

    # Запускаем бота
    application.run_polling()

if __name__ == '__main__':
    main()
def get_meta_from_stratz():
    response = requests.get(STRATZ_API_URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print("API Response:", data)  # Логируем ответ API
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
        print(f"Ошибка при запросе: {response.status_code}")  # Логируем код ошибки
        return None
