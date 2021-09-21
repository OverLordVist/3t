import db
import config
import menu
from telebot import types
import difflib as df

bot = config.bot
water_db = db.water_db


def register_user(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    keyboard.add(button_phone)
    bot.send_message(message.chat.id, 'Приветствуем Вас, ' + message.from_user.first_name +
                     "! Для просмотра каталога и оформления заказа, необходимо отправить нам Ваш номер телефона,"
                     "и адрес доставки (проживания). "
                     "Нажмите на кнопку для отправления Вашего номера телефона.", reply_markup=keyboard)


@bot.message_handler(content_types=['contact'])
def contact(message):
    if message.contact is not None:
        if not water_db.check_db(message):
            water_db.create_user(contact_to_string(message))
        else:
            new_item = {'id': contact_to_string(message)['user_id'],
                        'login': contact_to_string(message)['first_name'],
                        'number': contact_to_string(message)['phone_number']}
            water_db.update_db(id_user=message.from_user.id, new_item=new_item)

        bot.send_message(message.from_user.id, 'Введите Ваш город (только название): ',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, data_town)


def data_town(message):
    if not filter_towns(message):
        bot.send_message(message.from_user.id, 'Такого города не существует. Введите повторно: ')
        bot.register_next_step_handler(message, data_town)
    else:
        bot.register_next_step_handler(message, data_street)
        new_item = {'town': str(filter_towns(message))}
        water_db.update_db(id_user=message.from_user.id, new_item=new_item)
        bot.send_message(message.from_user.id, 'Введите название улицы (ул., дом, квартира): ')


def data_street(message):
    new_item = {'street': message.text}
    water_db.update_db(id_user=message.from_user.id, new_item=new_item)
    bot.send_message(message.from_user.id, 'Заполнение профиля пройдено успешно, ' +
                     message.from_user.first_name + '!',
                     reply_markup=menu.MainMenu)


def contact_to_string(message):
    temp_data = str(message.contact)
    temp_data.replace(':', ': ')
    temp_data.replace(',', ', ')
    temp_data.replace("'", '')
    temp_data = eval(temp_data)
    return temp_data


def filter_towns(message):
    towns_list = []
    with open('towns.txt', encoding='utf-8') as towns:
        for town in towns:
            towns_list.append(town)
    result = df.get_close_matches(message.text, towns_list)
    if not result:
        return False
    else:
        town = str(result[0]).rstrip()
        return town
