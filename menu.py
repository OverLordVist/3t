from telebot import types

BtnProfile = types.KeyboardButton('Профиль')
BtnCatalog = types.KeyboardButton('Каталог')
BtnBasket = types.KeyboardButton('Корзина')
BtnElect = types.KeyboardButton('Избранный заказ')
BtnHelp = types.KeyboardButton('Поддержка')
MainMenu = types.ReplyKeyboardMarkup(resize_keyboard=True).add(BtnProfile, BtnCatalog, BtnBasket, BtnElect, BtnHelp)
