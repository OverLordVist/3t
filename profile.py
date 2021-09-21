import config
from telebot import types
import db

water_db = db.water_db
bot = config.bot


def open_profile(message):
    stats = water_db.get_data_db(message.from_user.id, 'Users')
    keyboard = types.InlineKeyboardMarkup()
    key_setting = types.InlineKeyboardButton(text='Изменить данные профиля', callback_data="setting")
    keyboard.add(key_setting)
    bot.send_message(message.from_user.id, text='Логин: ' + str(stats[1]) +
                     '\nНомер телефона: ' + str(stats[2]) +
                     '\nГород: ' + str(stats[3]) +
                     '\nУлица (адрес доставки): ' + stats[4], reply_markup=keyboard)
