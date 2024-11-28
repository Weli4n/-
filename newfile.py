import os
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Функция для команды /start
async def start(update: Update, context: CallbackContext):
    user = update.effective_user
    await update.message.reply_text(f"Привет, {user.first_name}! Я простой бот. Используй /help, чтобы узнать мои команды.")

# Функция для команды /help
async def help_command(update: Update, context: CallbackContext):
    await update.message.reply_text("Доступные команды:\n/start - Начать общение\n/help - Список команд")

# Основной код
def main():
    # Получаем токен из переменной окружения
    TOKEN = os.getenv("BOT_TOKEN")
    PORT = int(os.getenv("PORT", "8443"))
    HOSTNAME = os.getenv("RENDER_EXTERNAL_HOSTNAME")

    if not TOKEN:
        raise ValueError("Токен бота не найден. Убедитесь, что переменная окружения BOT_TOKEN настроена.")

    if not HOSTNAME:
        raise ValueError("Не удалось получить хост Render. Убедитесь, что развертывание проходит в Render.")

    # Создаём приложение
    application = Application.builder().token(TOKEN).build()

    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # Установка Webhook
    webhook_url = f"https://{HOSTNAME}"
    application.run_webhook(
        listen="0.0.0.0",  # Слушать на всех интерфейсах
        port=PORT,         # Порт Render
        url_path="",        # Путь для Webhook
        webhook_url=webhook_url,  # URL Webhook
    )

if __name__ == "__main__":
    main()
