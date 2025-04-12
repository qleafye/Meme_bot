from telegram import *
from telegram.ext import *


TOKEN = "7945777073:AAHUSHeCe7U6XVNIIUp-zM10JDOo-DNkBVY"


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
        await update.message.reply_text("Poka net memov :(")
    elif text == "👙Закрыть клавиатуру":
        await update.message.reply_text("ИДИ НАФИГ!!!!!1", reply_markup=ReplyKeyboardRemove())






if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("menu", show_buttons))
    app.add_handler(MessageHandler(filters.TEXT, handle_reply_button))


    app.run_polling(poll_interval=3)



