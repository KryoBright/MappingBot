import telebot
import random

bot = telebot.TeleBot("1132979507:AAG92LMX_Wn-a6SrdYcA2pvadQBDvrkJULs")

class Sponsor:
    def __init__(self):
        self.userId = -1
        self.name = ""
        self.latitude = 0
        self.longitude = 0

verifiedSponsors = []
sponsorsList = {}
global last

def auth(fn):
    def wrapped(message):
        print(message.from_user.id)
        if(message.from_user.id in verifiedSponsors):
            return fn(message)
        else:
            return bot.send_message(message.from_user.id, 'You are not verified.')
    return wrapped

@bot.message_handler(commands=['get_sponsor'])
def get_sponsor(message):
    verifiedSponsors.append(message.from_user.id)
    bot.send_message(message.from_user.id, "Ok. You became a sponsor.")

@bot.message_handler(commands=['add_place'])
@auth
def add_place(message):
    bot.send_message(message.from_user.id, "Enter place name:")
    bot.register_next_step_handler(message, get_reg_name)

def get_reg_name(message):
    global last
    sponsor = Sponsor()
    sponsor.userId = message.from_user.id
    sponsor.name = message.text
    sponsorsList[sponsor.name] = sponsor
    last = sponsor.name 
    bot.send_message(message.from_user.id, 'Ok. I remembered. Now share the location of the point.')

@bot.message_handler(content_types=['location'])
@auth
def handle_location(message):
    global last
    sponsor = sponsorsList[last]
    sponsor.latitude = message.location.latitude
    sponsor.longitude = message.location.longitude
    bot.send_message(message.from_user.id, 'Good. I remembered.')

@bot.message_handler(commands=['del_place'])
@auth
def del_place(message):
    bot.send_message(message.from_user.id, "Enter place name:")
    bot.register_next_step_handler(message, get_del_name)

def get_del_name(message):
    if(sponsorsList[message.text].userId == message.from_user.id):
        del sponsorsList[message.text]
        bot.send_message(message.from_user.id, 'Ok. I remembered.')
    else:
        bot.send_message(message.from_user.id, 'Bad! You have no such place.')

@bot.message_handler(commands=['get_place_list'])
@auth
def get_place_list(message):
    try:
        bot.send_message(message.from_user.id, ",".join(sponsorsList.keys()))
    except Exception:
        bot.send_message(message.from_user.id, "List empty")

@bot.message_handler(commands=['sponsor_help'])
def sponsor_help(message):
	bot.reply_to(message, 
    """
    /add_place - to add a sponsorship place
    /del_place - to remove sponsorship place
    /get_place_list - to display all sponsorship places
    If the teams do not work you are not verified.
    """)

@bot.message_handler(commands=['cash_balance'])
@auth
def cash_balance(message):
    bot.send_message(message.from_user.id, str(random.randint(0, 1000)))

@bot.message_handler(commands=['put_money_into_cash'])
@auth
def put_money_into_cash(message):
    bot.send_message(message.from_user.id, "Номер для донатов 89113321"+str(random.randint(1000, 9999)))

bot.polling()