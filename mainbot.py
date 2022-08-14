from telegram import ReplyKeyboardMarkup, KeyboardButton  
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler, ConversationHandler
from file_work import*
from config import TOKEN
import os



updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


ID = 'id'
TASK = 'task'
COMPLETE = 'complete'
temp_task = None
temp_id = None

keyboard = ReplyKeyboardMarkup([
    [KeyboardButton('Посмотреть все'),
     KeyboardButton('Посмотреть готовые'),
     KeyboardButton('Посмотреть в работе')],

    [KeyboardButton('Добавить'),
     KeyboardButton('Изменить'),
     KeyboardButton('Удалить')],


], resize_keyboard=True)

def tasks_bot(TOKEN):
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

def start(update, context):
    arg = context.args
    if not arg:
        context.bot.send_message(update.effective_chat.id,
    "Привет! Я бот- помошник список дел. Также могу расказать пару шуток для этого напиши шутку или шутка и я выдам тебе анекдот\n \
    Я помогу организовать твой день,  \
    Смогу отследить твои дедлайны. Пользуйся кнопочками и все будет окей.\n \Для пасхалки нажми /info\n \
    Я еще тупенький бот и мой хозяин развивает меня. Совсем скоро я начну кидать мемы и рассказывать кучу шуток", reply_markup=keyboard)
    else:
        context.bot.send_message(update.effective_chat.id, f"{' '.join(arg)}")


def info(update, context):
    context.bot.send_message(update.effective_chat.id, "I'm Batman. Where's the trigger?")

def enter_task(update, context):
        update.message.reply_text(add_task(all_tasks, update.message.text))
        return ConversationHandler.END

def edit_id(update, _):
        update.message.reply_text('Введите ID задачи, которую вы хотите изменить:')
        return ID

def enter_edit_task(update, _):
        global temp_id
        temp_id = int(update.message.text)
        update.message.reply_text('Введите изменения в задачу:')
        return TASK

def edit_t(update, _):
        global temp_task
        temp_task = update.message.text
        update.message.reply_text('Введите статус задачи: 1 - выполнено, 0 - не выполнено')
        return COMPLETE

def edit_file(update, context):
        temp_flag = update.message.text
        for k, v in all_tasks.items():
            if temp_id == k:
                v['task'] = temp_task
                v['complete'] = temp_flag
        update.message.reply_text('Задача изменена')
        return ConversationHandler.END

def message(update, context):
        text = update.message.text
        if text.lower() == 'как дела?':
            context.bot.send_message(update.effective_chat.id, 'все хорошо,ты как?')
        if text.lower() == 'хорошо':
                context.bot.send_message(update.effective_chat.id, 'вот тебе мем')
        if text.lower() == 'чем занят?':
            context.bot.send_message(update.effective_chat.id, 'хозяин пытается добавить функцию мемов')
        if text.lower() == 'шутку':
            context.bot.send_message(update.effective_chat.id, 'Программиста спрашивают: – Как вам удалось так быстро выучить английский язык?!! – Та, ерунда какая. Они там почти все слова из С++ взяли.')
        if text.lower() == 'шутка':
            context.bot.send_message(update.effective_chat.id, 'Иван-дурак приходит к царю: — Я выполнил свое обещание, вот голова дракона. А ты выполнишь свое? — Да, вот рука принцессы')
        if text.lower() == 'привет':
            context.bot.send_message(update.effective_chat.id, 'И тебе привет..')
        elif text.lower() == 'посмотреть все':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_tasks, 1)}')
        elif text.lower() == 'посмотреть готовые':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_tasks, 2)}')
        elif text.lower() == 'посмотреть в работе':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_tasks, 3)}')
        elif text.lower() == 'добавить':
            context.bot.send_message(update.effective_chat.id, 'Введите задачу:')
            return TASK
        elif text.lower() == 'изменить':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_tasks, 1)}')
        elif text.lower() == 'сохранить изменения':
            context.bot.send_message(update.effective_chat.id, f'{save_data(all_tasks)}')
        elif text.lower() == 'удалить':
            context.bot.send_message(update.effective_chat.id, f'{print_todo(all_tasks, 1)}')
            context.bot.send_message(update.effective_chat.id, 'Введите ID задачи для удаления:')
            return ID
        else:
            context.bot.send_message(update.effective_chat.id, f'я тебя не понимаю')
        return update.message.text

def add(update, _):
        update.message.reply_text('Введите дело для добавления')
        return TASK

def delete(update, _):
        update.message.reply_text('Введите ID задачи, которую вы хотите удалить:')
        return ID

def delete_task(update, context):
        update.message.reply_text(del_task(all_tasks, update.message.text))
        return ConversationHandler.END

def cancel(update, _):
        update.message.reply_text('Окей, отменяем')
        return ConversationHandler.END

def stop(update, context):
        context.message.send_message(update.effective_chat.id, "Пока!")


def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, f'не понимаю Вас, Сударь')

conv_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(добавить|Добавить)$'), add)],
        states={
            TASK: [MessageHandler(Filters.text, enter_task)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
conv_handler2 = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(удалить|Удалить)$'), delete)],
        states={
            ID: [MessageHandler(Filters.text, delete_task)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
conv_handler3 = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex('^(изменить|Изменить)$'), edit_id)],
        states={
            ID: [MessageHandler(Filters.text, enter_edit_task)],
            TASK: [MessageHandler(Filters.text, edit_t)],
            COMPLETE: [MessageHandler(Filters.text, edit_file)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    
start_handler = CommandHandler('start', start)
info_handler = CommandHandler('info', info)
stop_handler = CommandHandler('stop', stop)
new_rask_handler = CommandHandler('add', add)
enter_task_handler = CommandHandler('enter_task', enter_task)
cancel_handler = CommandHandler('cancel', cancel)
delete_task_handler = CommandHandler('delete', delete)
delete_task_id_handler = CommandHandler('delete_task', delete_task)
edit_id_handler = CommandHandler('edit_id', edit_id)
enter_edit_task_handler = CommandHandler('enter_edit_task', enter_edit_task)
edit_f_handler = CommandHandler('edit_f', edit_file)
edit_t_handler = CommandHandler('edit_t', edit_t)

message_handler = MessageHandler(Filters.text, message)
unknown_handler = MessageHandler(Filters.command, unknown)  

dispatcher.add_handler(conv_handler)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(info_handler)
dispatcher.add_handler(stop_handler)
dispatcher.add_handler(new_rask_handler)
dispatcher.add_handler(enter_task_handler)
dispatcher.add_handler(conv_handler2)
dispatcher.add_handler(conv_handler3)
dispatcher.add_handler(cancel_handler)
dispatcher.add_handler(delete_task_handler)
dispatcher.add_handler(delete_task_id_handler)
dispatcher.add_handler(edit_id_handler)
dispatcher.add_handler(enter_edit_task_handler)
dispatcher.add_handler(edit_f_handler)
dispatcher.add_handler(edit_t_handler)
dispatcher.add_handler(message_handler)
dispatcher.add_handler(unknown_handler)

print('server started')
updater.start_polling()
# "bot.polling(none_stop=True)" # почитал и вроде как должен работать без перебоев / не работает
updater.idle()


