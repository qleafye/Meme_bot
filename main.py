from telegram import *
from telegram.ext import *
import os
import json
import random

TOKEN = ""

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


def load_db_anecdots():
    if not os.path.exists("databaseanekdots.json"):
        return []
    with open("databaseanekdots.json", "r", encoding="utf-8") as f:
        return json.load(f)


def save_db_anecdots(data):
    with open("databaseanekdots.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


async def send_random_anecdot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    anekdot = load_db_anecdots()

    if not anekdot:
        await update.message.reply_text("ПРОСТИТИ ПОКА НЭТ АНЕКДОТИВ")
        return

    anekdot = random.choice(anekdot)

    await update.message.reply_text(anekdot["anekdot_text"])


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
    buttons = [["😂Отправить мем", "😜Анекдот", "💨Meme-BATTLE💨"],
               ["🚨Помощь", "🔧Настройки"],
               ["👙Закрыть клавиатуру"]
               ]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    await update.message.reply_text("Выберете прикол", reply_markup=reply_markup)


async def handle_reply_button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if text == "😂Отправить мем":
<<<<<<< HEAD
        await send_random_meme(update, context)
    elif text == "😜Анекдот":
        await send_random_anecdot(update, context)
    elif text == "💨Meme-BATTLE💨":
        await start_meme_battle(update, context)
=======
        await send_random_meme(update=update, context=ContextTypes.DEFAULT_TYPE)
>>>>>>> origin/master
    elif text == "👙Закрыть клавиатуру":
        await update.message.reply_text("ИДИ НАФИГ!!!!!1", reply_markup=ReplyKeyboardRemove())


async def start_meme_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if context.user_data.get(f'{user_id}_meme_battle_active', False):
        await update.message.reply_text("Баттл уже идет! Продолжай выбирать!")
        return

    all_memes_data = load_db()
    all_meme_paths = [meme["file_path"] for meme in all_memes_data if os.path.exists(meme["file_path"])]

    if len(all_meme_paths) < 2:
        await update.message.reply_text("Для баттла нужно минимум 2 мема! 😢")
        return

    await update.message.reply_text("🔥🔥🔥 MEME BATTLE НАЧИНАЕТСЯ! 🔥🔥🔥")

    context.user_data[f'{user_id}_meme_battle_active'] = True
    context.user_data[f"{user_id}_meme_battle_candidates"] = all_meme_paths.copy()
    context.user_data[f"{user_id}_meme_battle_winners"] = []
    context.user_data[f"{user_id}_meme_battle_round"] = 1
    context.user_data[f"{user_id}_meme_battle_message_id"] = None

    await _send_next_meme_pair(update, context)


async def _send_next_meme_pair(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    candidates = context.user_data.get(f"{user_id}_meme_battle_candidates", [])
    winners = context.user_data.get(f"{user_id}_meme_battle_winners", [])
    prev_message_id = context.user_data.get(f"{user_id}_meme_battle_message_id")

    # Если осталось 0 или 1 мемов в текущем раунде
    if len(candidates) <= 1:
        # Если есть победители из предыдущего раунда - добавляем оставшийся мем
        if len(candidates) == 1:
            winners.append(candidates.pop())

        # Проверяем общее количество мемов для следующего раунда
        if len(winners) < 2:
            if len(winners) == 1:
                # Объявляем победителя
                await _declare_winner(update, context, winners[0])
                return
            else:
                await update.message.reply_text("Баттл завершился без победителя! 😱")
                await _cleanup_battle_data(context, user_id)
                return

        # Начинаем новый раунд
        context.user_data[f"{user_id}_meme_battle_round"] += 1
        context.user_data[f"{user_id}_meme_battle_candidates"] = winners.copy()
        context.user_data[f"{user_id}_meme_battle_winners"] = []
        candidates = winners.copy()
        random.shuffle(candidates)
        await update.message.reply_text(f"🌀 РАУНД {context.user_data[f'{user_id}_meme_battle_round']} НАЧИНАЕТСЯ! 🌀")

    # Берем первые два мема из списка
    meme1 = candidates.pop(0)
    meme2 = candidates.pop(0) if len(candidates) > 0 else None

    # Формируем сообщение с кнопками
    keyboard = [
        [InlineKeyboardButton("👉 1 Мем 👈", callback_data="vote_0"),
         InlineKeyboardButton("👉 2 Мем 👈", callback_data="vote_1")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Собираем медиа-группу из двух фото
    media_group = []
    media_group.append(InputMediaPhoto(media=open(meme1, 'rb')))
    if meme2:
        media_group.append(InputMediaPhoto(media=open(meme2, 'rb')))

    # Удаляем предыдущее сообщение если есть
    if prev_message_id:
        try:
            await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=prev_message_id)
        except:
            pass

    # Отправляем новое сообщение
    sent_message = await context.bot.send_media_group(
        chat_id=update.effective_chat.id,
        media=media_group
    )

    # Отправляем кнопки отдельным сообщением и сохраняем ID
    message_with_buttons = await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Выбери лучший мем:",
        reply_markup=reply_markup
    )

    # Сохраняем данные
    context.user_data[f"{user_id}_meme_battle_current_pair"] = [meme1, meme2] if meme2 else [meme1]
    context.user_data[f"{user_id}_meme_battle_candidates"] = candidates
    context.user_data[f"{user_id}_meme_battle_message_id"] = message_with_buttons.message_id


async def vote_in_battle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    choice = int(query.data.split("_")[1])

    if not context.user_data.get(f'{user_id}_meme_battle_active', False):
        await query.answer("Баттл уже завершен!")
        return

    current_pair = context.user_data.get(f"{user_id}_meme_battle_current_pair", [])
    winners = context.user_data.get(f"{user_id}_meme_battle_winners", [])

    if len(current_pair) < 2:
        winners.append(current_pair[0])
    else:
        winners.append(current_pair[choice])

    context.user_data[f"{user_id}_meme_battle_winners"] = winners

    # Удаляем сообщение с кнопками
    try:
        await context.bot.delete_message(
            chat_id=query.message.chat_id,
            message_id=query.message.message_id
        )
    except:
        pass

    await _send_next_meme_pair(update, context)


async def _declare_winner(update: Update, context: ContextTypes.DEFAULT_TYPE, winner_path: str):
    user_id = update.effective_user.id
    winner_data = next((meme for meme in load_db() if meme["file_path"] == winner_path), None)

    if winner_data:
        caption = f"🏆 ПОБЕДИТЕЛЬ БАТТЛА! 🏆\nОписание: {winner_data['descrition']}"
        await update.message.reply_photo(
            photo=open(winner_path, 'rb'),
            caption=caption
        )
    else:
        await update.message.reply_text("⚠️ Победитель не найден в базе!")

    await _cleanup_battle_data(context, user_id)


async def _cleanup_battle_data(context, user_id):
    keys_to_remove = [
        f'{user_id}_meme_battle_active',
        f'{user_id}_meme_battle_candidates',
        f'{user_id}_meme_battle_winners',
        f'{user_id}_meme_battle_current_pair',
        f'{user_id}_meme_battle_message_id',
        f'{user_id}_meme_battle_round'
    ]
    for key in keys_to_remove:
        if key in context.user_data:
            del context.user_data[key]



if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("custom", custom_command))
    app.add_handler(CommandHandler("menu", show_buttons))
    app.add_handler(MessageHandler(filters.TEXT, handle_reply_button))
    app.add_handler(CallbackQueryHandler(vote_in_battle, pattern="^vote_"))

    app.run_polling(poll_interval=3)

