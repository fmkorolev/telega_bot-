import time
from bs4 import BeautifulSoup
import requests
import telebot
import datetime

bot = telebot.TeleBot("TOKEN") 
channel_id = 5574098304
url = "https://dtf.ru/kek/entries/new"
header = {
    "user-agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.90 Safari/537.36"
}

while True: # Бесконечный цикл
    def meme(): # Обьявляем функцию
        r = requests.get(url, headers=header).text
        soup = BeautifulSoup(r, 'html.parser')
        bs = soup.find('div', class_='content-image')
        bs2 = bs.find('div', class_='andropov_image')
        list = open("list.txt", "w+")
        link = (bs2['data-image-src']) # Сам парсер мемов
        if link not in list:
            with open("list.txt", "w") as file:
                file.write(link)
                bot.send_photo(channel_id, link) # Отправляем сообщение
                print(f"[{datetime.datetime.now()}] Отправил") # лог в консоль
        else:
            print(f"[{datetime.datetime.now()}] Новых мемов пока нет") # лог в консоль
    meme() # вызываем функцию
    time.sleep(10) # перерыв между проверкой на новые мемы(время в секундах)
