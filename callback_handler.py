import config
from telebot import types
import catalog
import basket

bot = config.bot
product = catalog.product


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "setting":
        keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
        keyboard.add(button_phone)
        bot.send_message(call.message.chat.id, 'Отправьте повторно свой номер телефона.', reply_markup=keyboard)
    elif call.data == 'RestCat':
        product.show_catalog(id_user=call.message.chat.id)
    elif call.data in product.product_info['sticker']:
        product.show_product(call)
    elif call.data in product.product_info['add_call']:
        basket.add_product_basket(call)
    elif call.data in product.product_info['delete_call']:
        basket.remove_product_basket(call)
    elif call.data in product.product_info['all_delete_call']:
        basket.delete_all_product(call)
