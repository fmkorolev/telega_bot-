from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from config import TOKEN


def start(update, context):
    arg = context.args
    if not arg:
        context.bot.send_message(update.effective_chat.id, "Привет этот бот показывает список дел")
    else:
        context.bot.send_message(update.effective_chat.id, f"{''.join(arg)}")


def info(update, context):
    context.bot.send_message(update.effective_chat.id, "Чтобы посмотреть список дел напишите покажи список дел")


def message(update, context):
    text = update.message.text
    if text.lower() == 'покажи список дел':
        context.bot.send_message(update.effective_chat.id, '1. покормить кота/ 2. позвонить бабушке')
    else:
        context.bot.send_message(update.effective_chat.id, 'я тебя не понимаю')


def unknown(update, context):
    context.bot.send_message(update.effective_chat.id, f'Шо сказал, не пойму')