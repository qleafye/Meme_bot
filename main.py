from telegram import *
from telegram.ext import *
import os
import json
import random

TOKEN = "8018994940:AAHOX82aalcenjG_wFoAP29O3EnEdDrCQc0"

photos_dir = "photos"
database_file = "database.json"
os.makedirs(photos_dir, exist_ok=True)


def load_db():
    if not os.path.exists(database_file):
        return []
    with open(database_file, "r", encoding="utf-8") as f:
        return json.load(f)

def save_db(data):
    with open(database_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

async def send_random_meme(update: Update, context: ContextTypes.DEFAULT_TYPE):
    memes = load_db()

    if not memes:
        await update.message.reply_text("ПРОСТИТИ ПОКА НЭТ МЭМИВ")
        return

    meme = random.choice(memes)

    if not os.path.exists(meme["file_path"]):
        await update.reply_text("Ошибка мем не найден, извинити")
        return

    await update.message.reply_photo(photo=open(meme["file_path"], "rb"), \
                                     caption=f"Описание:{meme['descrition']}")



async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await  update.message.reply_text("ПРИВЕЕЕЕТ Я ТВОЙ БОТ БУДУ ДЕЛАТЬ МЕМИ")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await  update.message.reply_text("1.	Есть какая то база данным с мемами, и по запросу пользователя мем отправляется.\n\
2.	Совместить надпись с фото.\n\
3.	Прикрутить нейросеть для анекдота\n\
4.	Мем-баттл\n")

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await  update.message.reply_text("ЭТО КАСТОМНАЯ КОМАНДА")

async def show_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    buttons = [["😂Отправить мем", "😜Анекдот", "Meme-BATTLE"],
               ["🚨Помощь", "🔧Настройки"],
               ["👙Закрыть клавиатуру"]
               ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Выберете прикол", reply_markup=reply_markup)

async def handle_reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "😂Отправить мем":
        await send_random_meme(update=update, context=ContextTypes.DEFAULT_TYPE)
    elif text == "👙Закрыть клавиатуру":
        await update.message.reply_text("ИДИ НАФИГ!!!!!1", reply_markup=ReplyKeyboardRemove())






if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("menu", show_buttons))
    app.add_handler(CommandHandler("meme",  send_random_meme))
    app.add_handler(MessageHandler(filters.TEXT, handle_reply_button))


    app.run_polling(poll_interval=3)



