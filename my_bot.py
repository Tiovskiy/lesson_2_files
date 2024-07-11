import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from dotenv import load_dotenv

# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN = os.environ.get("TOKEN")


# функция для задания 1 (команда /start)
async def start(update, context):
    await update.message.reply_text('Первая задача выполнена')

# функция для задания 2 (Считаем количество слов)
async def text(update, context):
    await update.message.reply_text(f'Написано {len(update.message.text.split(" "))} слов(а)')

# функция для задание 3 (голосовые сообщения)
async def voice(update, context):
    await update.message.reply_text(f'id твоего аудиосообщения: {update.message.message_id}')

# функция для задания 4 (команда /warcraft)
async def warcraft(update, context):

    # создаем список кнопок
    keyboard = [["Альянс","Орда"]]

    # создаем Reply клавиатуру
    reply_markup = ReplyKeyboardMarkup(keyboard, 
                                       resize_keyboard=True, 
                                       one_time_keyboard=True)

    # выводим клавиатуру с сообщением
    await update.message.reply_text('ТЫ должен сделать свой выбор', reply_markup=reply_markup)

# функция для задания 5 (сохраняем изображение)
async def image(update, context):
    await update.message.reply_text('Твоя фотография получена и сохранена!')

    # достаем файл изображения из сообщения
    file = await update.message.photo[-1].get_file()
    
    # сохраняем изображение на диск
    os.makedirs('images', exist_ok=True)
    await file.download_to_drive(f'images/{update.message.message_id}')

def main():

    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик команды /warcraft
    application.add_handler(CommandHandler("warcraft", warcraft))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик сообщений с изображением
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()