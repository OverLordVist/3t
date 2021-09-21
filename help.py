import config

bot = config.bot


@bot.message_handler(commands=['help'])
def get_support(message):
    bot.send_message(message.from_user.id, 'ТУТ БУДЕТ ПОДДЕРЖКА ИЗ ДВУХ ТАНКОВ')
