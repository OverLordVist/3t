import telebot.types

import basket
import catalog
import config
import db
import help
import menu
import profile
import register
import callback_handler
import os
from flask import Flask, request



water_db = db.water_db
# water_db.create_product()
bot = config.bot
product = catalog.product



@bot.message_handler(commands=['start'])
def hello_message(message):
    if not water_db.check_db(message):
        register.register_user(message)
    else:
        bot.send_message(message.from_user.id, 'Приветствуем вас, ' + message.from_user.first_name + '!',
                         reply_markup=menu.MainMenu)


@bot.message_handler(content_types=['text'])
def main_menu(message):
    if not water_db.check_db(message):
        register.register_user(message)
    if message.text == 'Профиль':
        bot.delete_message(message.chat.id, message.message_id)
        profile.open_profile(message)
    elif message.text == 'Поддержка':
        bot.delete_message(message.chat.id, message.message_id)
        help.get_support(message)
    elif message.text == 'Каталог':
        bot.delete_message(message.chat.id, message.message_id)
        product.show_catalog(id_user=message.from_user.id)
    elif message.text == 'Избранный заказ':
        bot.delete_message(message.chat.id, message.message_id)
        bot.send_message(message.from_user.id, 'Обычный заказ')
    elif message.text == 'Корзина':
        bot.delete_message(message.chat.id, message.message_id)
        basket.show_basket(message)


if __name__ == '__main__':
    bot.infinity_polling()
