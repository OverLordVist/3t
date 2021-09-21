import db
import catalog
import config
from telebot import types

bot = config.bot
water_db = db.water_db
product = catalog.product

data_prods = config.data_prods


def add_product_basket(call):
    id_prod = int((product.product_info['add_call']).index(call.data))
    BtnAddOne = types.InlineKeyboardButton(text='➕', callback_data=(product.product_info['add_call'])[id_prod])
    BtnDeleteOne = types.InlineKeyboardButton(text='➖',
                                              callback_data=(product.product_info['delete_call'])[id_prod])
    BtnDeleteAll = types.InlineKeyboardButton(text='Удалить товар из корзины',
                                              callback_data=(product.product_info['all_delete_call'])[id_prod])
    BtnToCatalog = types.InlineKeyboardButton(text='Вернуться в каталог', callback_data='RestCat')
    BtnToBasket = types.InlineKeyboardButton(text='Просмотреть корзину', callback_data='RestBasket')
    if not water_db.check_basket(id_user=call.message.chat.id):
        water_db.add_basket(call.message.chat.id, data_prods[id_prod + 1],
                            (product.product_info["min_amount"])[id_prod])
        bot.send_message(call.message.chat.id,
                         f'Товар был успешно добавлен ({(product.product_info["min_amount"])[id_prod]} шт.)!' +
                         f'\nНаименование товара: {(product.product_info["name"])[id_prod]}' +
                         f'\nДанного товара в корзине: '
                         f'{(water_db.get_data_db(call.message.chat.id, "Basket"))[id_prod + 1]}',
                         reply_markup=types.InlineKeyboardMarkup(row_width=1).add(BtnAddOne, BtnDeleteAll, BtnToCatalog,
                                                                                  BtnToBasket))
        if id_prod == 0:
            water_db.add_basket(call.message.chat.id, 'tara', (product.product_info["min_amount"])[id_prod])

    elif call.data in product.product_info['add_call']:
        water_db.add_basket(call.message.chat.id, data_prods[id_prod + 1], 1)
        bot.send_message(call.message.chat.id,
                         'Товар был успешно добавлен (1 шт.)!' +
                         f'\nНаименование товара: {(product.product_info["name"])[id_prod]}' +
                         f'\nДанного товара в корзине:'
                         f' {(water_db.get_data_db(call.message.chat.id, "Basket"))[id_prod + 1]}',
                         reply_markup=types.InlineKeyboardMarkup(row_width=1).add(BtnAddOne,
                                                                                  BtnDeleteOne,
                                                                                  BtnDeleteAll,
                                                                                  BtnToCatalog,
                                                                                  BtnToBasket))
        if id_prod == 0:
            water_db.add_basket(call.message.chat.id, 'tara', 1)


def remove_product_basket(call):
    id_prod = int((product.product_info['delete_call']).index(call.data))
    BtnAddOne = types.InlineKeyboardButton(text='➕', callback_data=(product.product_info['add_call'])[id_prod])
    BtnDeleteOne = types.InlineKeyboardButton(text='➖',
                                              callback_data=(product.product_info['delete_call'])[id_prod])
    BtnDeleteAll = types.InlineKeyboardButton(text='Удалить товар из корзины',
                                              callback_data=(product.product_info['all_delete_call'])[id_prod])
    BtnToCatalog = types.InlineKeyboardButton(text='Вернуться в каталог', callback_data='RestCat')
    BtnToBasket = types.InlineKeyboardButton(text='Просмотреть корзину', callback_data='RestBasket')
    if (water_db.get_data_db(call.message.chat.id, "Basket"))[id_prod + 1] > \
            (product.product_info["min_amount"])[id_prod]:
        water_db.remove_basket(call.message.chat.id, data_prods[id_prod + 1])
        bot.send_message(call.message.chat.id, 'Товар был успешно убран (1 шт.)!' +
                         f'\nНаименование товара: {(product.product_info["name"])[id_prod]}' +
                         f'\nДанного товара в корзине:'
                         f' {(water_db.get_data_db(call.message.chat.id, "Basket"))[id_prod + 1]}',
                         reply_markup=types.InlineKeyboardMarkup(row_width=1).add(BtnAddOne, BtnDeleteOne,
                                                                                  BtnDeleteAll, BtnToCatalog,
                                                                                  BtnToBasket))
        if id_prod == 0:
            water_db.remove_basket(call.message.chat.id, 'tara')
    else:
        bot.send_message(call.message.chat.id, 'У вас минимальное возможное количество товара!' +
                         '\nЧтобы убрать товар полностью из корзины, нажмите на кнопку "Убрать из корзины".' +
                         f'\nНаименование товара: {(product.product_info["name"])[id_prod]}' +
                         f'\nДанного товара в корзине:'
                         f' {(water_db.get_data_db(call.message.chat.id, "Basket"))[id_prod + 1]}',
                         reply_markup=types.InlineKeyboardMarkup(row_width=1).add(BtnAddOne, BtnDeleteAll,
                                                                                  BtnToCatalog, BtnToBasket))


def delete_all_product(call):
    id_prod = int((product.product_info['all_delete_call']).index(call.data))
    BtnAddOne = types.InlineKeyboardButton(text='➕', callback_data=(product.product_info['add_call'])[id_prod])
    BtnToCatalog = types.InlineKeyboardButton(text='Вернуться в каталог', callback_data='RestCat')
    BtnToBasket = types.InlineKeyboardButton(text='Просмотреть корзину', callback_data='RestBasket')
    water_db.delete_all_basket(call.message.chat.id, data_prods[id_prod + 1])
    bot.send_message(call.message.chat.id, 'Данный товар был успешно удален из Вашей корзины!' +
                     f'\nНаименование товара: {(product.product_info["name"])[id_prod]}',
                     reply_markup=types.InlineKeyboardMarkup(row_width=1).add(BtnAddOne, BtnToCatalog, BtnToBasket))
    if id_prod == 0:
        water_db.delete_all_basket(call.message.chat.id, 'tara')


def show_basket(id_user):
    pass
