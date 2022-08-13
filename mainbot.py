from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from config import TOKEN
from file_work import *

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher

TITLE, TASK = range(2)

one_task = {
    'title': None,
    'description': None
}


def start(update, context):
    arg = context.args
    if not arg:
        context.bot.send_message(update.effective_chat.id, ""'Привет! Я бот- помошник список дел.\n \
 Я помогу организовать твой день,  \
 Смогу отследить твои дедлайны  \
 Используй эти команды:\n\
 /add <имя> <дату> <время> - добавить новое событие или дедлайн \n \
 /remove Удаляет задание из списка дел (в стадии бета :D)\n \
 
    else:
        context.bot.send_message(update.effective_chat.id, f"{' '.join(arg)}")


def info(update, context):
    context.bot.send_message(update.effective_chat.id,
                             """Доступны следующие команды:
                             /start - старт бота и немножко описания по командам,
                             /info - информация  по командам,
                             /add - добавить задачу""")


def message(update, context):
    text = update.message.text
    if text.lower() == 'привет':
        context.bot.send_message(update.effective_chat.id, 'Привет! Этот бот создан для списка дел для этого нажми /info')
    else:
        context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')


def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, f'Моя  твоя, не понимать')


def add(update, context):
    context.bot.send_message(update.effective_chat.id,
                             f'введите заголовок задачи')
    return TITLE


def add_title(update, context):
    global one_task
    text = update.message.text
    if abs(len(text)) > 30:
        context.bot.send_message(
            update.effective_chat.id, f'Слишком длинный заголовок')
        return
    one_task['title'] = text
    add_to_temp_file(text)
    context.bot.send_message(
            update.effective_chat.id, f'Обновлен заголовок. Сейчас словарь выглядит так: {one_task}')
    context.bot.send_message(
            update.effective_chat.id, f' жду описание')
    return TASK

def add_task(update, context):
    global one_task
    text = update.message.text
    if abs(len(text)) > 50:
        context.bot.send_message(
            update.effective_chat.id, f'Слишком длинный текст задачи')
    one_task['description'] = text
    add_to_temp_file(text)
    write_to_database(one_task)
    clear_temp_file()
    context.bot.send_message(
            update.effective_chat.id, f'Обновлена задача. Сейчас словарь выглядит так: {one_task}')
    context.bot.send_message(
            update.effective_chat.id, f'Задача добавлена в базу данных')
    return ConversationHandler.END

def exit_add(update,context):
    context.bot.send_message(
            update.effective_chat.id, f'Операция прервана')
    return ConversationHandler.END
    
    
start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('add', add)],
    states={
        
        TITLE: [MessageHandler(Filters.text, add_title),CommandHandler('no', exit_add)],
        TASK: [MessageHandler(Filters.text, add_task),CommandHandler('no', exit_add)]
    
        },
    fallbacks=[CommandHandler('no', exit_add)]
)

message_handler = MessageHandler(Filters.text, message)
unknown_handler = MessageHandler(Filters.command, unknown)  # /game


dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(conv_handler)
dispatcher.add_handler(unknown_handler)
dispatcher.add_handler(message_handler)


print('server started')
updater.start_polling()
updater.idle()
