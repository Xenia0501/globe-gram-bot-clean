import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    ConversationHandler,
    filters,
)
from config import TELEGRAM_BOT_TOKEN
from generator.post_generator import generate_full_post
from storage import set_group, get_group, set_user_settings, get_user_settings

logging.basicConfig(level=logging.INFO)

STYLES = ["дружелюбный", "информационный", "креативный"]
STYLE, TOPICS, SCHEDULE = range(3)
reply_keyboard = [[s] for s in STYLES]
markup = ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True, resize_keyboard=True)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "📩 Привет! Я — тревел-бот и помогу тебе с автопостингом.\n\n"
        "🖊️ Чтобы настроить автопубликацию постов в группу:\n"
        "1️⃣ Добавь меня в свою группу\n"
        "2️⃣ Назначь админом\n"
        "3️⃣ В группе введи команду /register\n\n"
        "⚙️ Затем в личке настроишь стиль, темы и расписание через /settings"
    )

# /register в группе
async def register_group(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    user = update.effective_user

    if chat.type not in ["group", "supergroup"]:
        await update.message.reply_text("Команду /register нужно запускать в группе.")
        return

    set_group(user.id, chat.id)
    await update.message.reply_text(
        f"✅ Группа зарегистрирована! Теперь я буду публиковать в: `{chat.id}`\n\n"
        "💬 Чтобы задать стиль, темы и расписание, напиши мне в личку команду /settings",
        parse_mode="Markdown"
    )

# /settings — сохраняем предпочтения пользователя
async def settings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌈 Выбери стиль для автопостов:", reply_markup=markup)
    return STYLE

async def set_style(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["style"] = update.message.text
    await update.message.reply_text("✏️ Введи темы через запятую (или напиши /skip):")
    return TOPICS

async def set_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topics = [t.strip() for t in update.message.text.split(",") if t.strip()]
    context.user_data["topics"] = topics
    await update.message.reply_text("⏰ Введи расписание (например: каждый день в 10:00):")
    return SCHEDULE

async def skip_topics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["topics"] = []
    await update.message.reply_text("⏰ Введи расписание (например: каждый день в 10:00):")
    return SCHEDULE

async def set_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    schedule = update.message.text
    user_id = update.effective_user.id
    set_user_settings(user_id, {
        "style": context.user_data["style"],
        "topics": context.user_data["topics"],
        "schedule": schedule
    })
    await update.message.reply_text("✅ Настройки сохранены! Мы настроим автопостинг по ним.")
    return ConversationHandler.END

# /publish — вызовется вручную или Make/Zapier
async def publish(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    group_id = get_group(user_id)
    settings = get_user_settings(user_id)

    if not group_id or not settings:
        await update.message.reply_text("⚠️ Нет зарегистрированной группы или настроек. Используй /register и /settings.")
        return

    style = settings.get("style")
    topics = settings.get("topics", [])
    topic = topics[0] if topics else None  # Берём первую тему, если есть

    post = generate_full_post(style=style, topic=topic)

    try:
        await context.bot.send_photo(chat_id=group_id, photo=post["image_url"], caption=post["text"])
        await update.message.reply_text("✅ Пост опубликован в группу.")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка при публикации: {e}")

# /help
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ Инструкция по использованию:\n\n"
        "1️⃣ Добавь бота в группу\n"
        "2️⃣ Сделай админом\n"
        "3️⃣ В группе напиши /register\n"
        "4️⃣ В личке введи /settings и задай стиль, темы, расписание\n\n"
        "⚙️ Публикация будет выполняться через Make или Zapier по сохранённым настройкам"
    )

# /cancel
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚫 Отменено.")
    return ConversationHandler.END

# MAIN
def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    conv_settings = ConversationHandler(
        entry_points=[CommandHandler("settings", settings)],
        states={
            STYLE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_style)],
            TOPICS: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, set_topics),
                CommandHandler("skip", skip_topics)
            ],
            SCHEDULE: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_schedule)]
        },
        fallbacks=[CommandHandler("cancel", cancel)]
    )

    app.add_handler(conv_settings)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register_group))
    app.add_handler(CommandHandler("settings", settings))
    app.add_handler(CommandHandler("publish", publish))
    app.add_handler(CommandHandler("help", help_command))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
