import telebot

bot = telebot.TeleBot("1132979507:AAG92LMX_Wn-a6SrdYcA2pvadQBDvrkJULs")

users = []
last = ["ls"]

help_commans_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
help_commans_keyboard.row('/start', '/help', '/knowledge', '/send_my_geo', '/create_room', '/show_map', '/create_rout')
@bot.message_handler(commands=['commands', 'c'])
def help_commands_menu(message):
    bot.send_message(message.chat.id, 'Привет, перед тобой список доступных команд:', reply_markup=help_commans_keyboard)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")
    userId = message.from_user.id
    isFound = False
    for user in users:
        if (user[0] == userId):
            isFound = True
    if (not isFound):
        users.append([userId, message.from_user.username])

# заглушки из таска в ПМ.
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "Чем мы можем вам помочь?")

@bot.message_handler(commands=['send_my_geo'])
def send_help(message):
    bot.reply_to(message, "Бот получил геоданные")

@bot.message_handler(commands=['create_room'])
def send_help(message):
    bot.reply_to(message, "Создание комнаты")

@bot.message_handler(commands=['show_map'])
def send_help(message):
    bot.reply_to(message, "Типо карта")

@bot.message_handler(commands=['create_rout'])
def send_help(message):
    bot.reply_to(message, "Маршрут на карте (можно как-то передать данные другого пользователя с которым будет встреча)")

# выводит пользователей в сети
@bot.message_handler(commands=['knowledge'])
def send_knowledge(message):
    s = ""
    for user in users:
        s += "," + str(user[1])
    bot.reply_to(message, s)


@bot.message_handler(func=(lambda message: (message.from_user.username == "KryoBright")), commands=["all"])
def all_send(message):
    for user in users:
        bot.send_message(user[0], last[0])


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    last[0] = message.text
    bot.reply_to(message, message.text)


bot.polling()