import telebot

product_dict = {}
product_list = []
data_prods = {}

with open('cfg.txt', encoding='utf-8') as cfg:
    for product in cfg:
        product_dict[product.rstrip()] = 'INTEGER'
        product_list.append(product.rstrip())

product_dict['tara'] = 'INTEGER'

for i in range(1, len(product_list)+1):
    data_prods[i] = product_list[i-1]

token = '1871649452:AAE84FI1TEncnfTepS-9eJbgg180ClflG2s'
bot = telebot.TeleBot(token)
