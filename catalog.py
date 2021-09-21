import config
from telebot import types
import db
from collections import defaultdict

water_db = db.water_db
bot = config.bot


class Product:
    def __init__(self):
        self.product_info = defaultdict(list)
        for id_prod in range(1, water_db.count_prods()+1):
            product_list = water_db.get_product_data(id_prod)
            print(product_list)
            self.product_info['id'].append(id_prod)
            self.product_info['name'].append(product_list[1])
            self.product_info['price_id'].append(product_list[2])
            self.product_info['photo'].append(product_list[3])
            self.product_info['description'].append(product_list[4])
            self.product_info['sticker'].append(product_list[5])
            self.product_info['min_amount'].append(product_list[6])
            self.product_info['add_call'].append(product_list[7])
            self.product_info['delete_call'].append(product_list[8])
            self.product_info['all_delete_call'].append(product_list[9])

    def show_catalog(self, id_user):
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        names = list(self.product_info['name'])
        callbacks = list(self.product_info['sticker'])
        for i in range(0, len(self.product_info['id'])):
            keyboard.add(types.InlineKeyboardButton(text=names[i],
                                                    callback_data=callbacks[i]))
        bot.send_photo(id_user, 'https://i.imgur.com/GzBhhGc.png',
                       caption='Представленные товары в каталоге',
                       reply_markup=keyboard)

    def show_product(self, call):
        id_prod = int((self.product_info['sticker']).index(call.data))
        BtnAddToBasket = types.InlineKeyboardButton(text='Добавить товар в корзину',
                                                    callback_data=(self.product_info['add_call'])[id_prod])
        BtnBackToCatalog = types.InlineKeyboardButton(text='Вернуться в каталог', callback_data='RestCat')
        bot.send_photo(call.message.chat.id, (self.product_info['photo'])[id_prod],
                       caption=(self.product_info['description'])[id_prod],
                       reply_markup=types.InlineKeyboardMarkup(row_width=1).add(BtnAddToBasket, BtnBackToCatalog))


product = Product()
