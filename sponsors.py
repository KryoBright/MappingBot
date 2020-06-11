import telebot
import random

bot = telebot.TeleBot("1132979507:AAG92LMX_Wn-a6SrdYcA2pvadQBDvrkJULs")

class SponsorProfile:
    def __init__(self):
        self.userId = -1
        self.name = ""
        self.balance = 0
        self.sposorsPoints = {}

class SponsorPoint:
    def __init__(self):
        self.SponsorProfile = None
        self.name = ""
        self.latitude = 0
        self.longitude = 0

sponsorsList = {}
verifiedSponsors = []

global last

def auth(fn):
    def wrapped(message):
        if(message.from_user.id in verifiedSponsors):
            return fn(message)
        else:
            return bot.send_message(message.from_user.id, 'You are not verified.')
    return wrapped

    
@bot.message_handler(commands=['get_sponsor'])
def get_sponsor(message):
    bot.send_message(message.from_user.id, "Enter company name:")
    bot.register_next_step_handler(message, get_reg_sponsor)

def get_reg_sponsor(message):
    Profile = SponsorProfile()
    Profile.userId = message.from_user.id
    Profile.name = message.text
    sponsorsList[Profile.userId] = Profile
    verifiedSponsors.append(message.from_user.id)
    bot.send_message(message.from_user.id, 'Ok. I remembered. Now you can use the sponsorship interface.')    
    

@bot.message_handler(commands=['add_place'])
@auth
def add_place(message):
    bot.send_message(message.from_user.id, "Enter place name:")
    bot.register_next_step_handler(message, get_reg_name)

def get_reg_name(message):
    global last
    Point = SponsorPoint()
    Profile = sponsorsList[message.from_user.id] 
    Point.name = message.text
    Profile.sposorsPoints[Point.name] = Point
    Point.SponsorProfile = Profile
    
    last = SponsorPoint
    bot.send_message(message.from_user.id, 'Ok. I remembered. Now share the location of the point.')

@bot.message_handler(content_types=['location'])
@auth
def handle_location(message):
    global last
    last.latitude = message.location.latitude
    last.longitude = message.location.longitude
    bot.send_message(message.from_user.id, 'Good. I remembered.')

@bot.message_handler(commands=['del_place'])
@auth
def del_place(message):
    bot.send_message(message.from_user.id, "Enter place name:")
    bot.register_next_step_handler(message, get_del_name)

def get_del_name(message):
    try:
        del sponsorsList[message.from_user.id].sposorsPoints[message.text]
        bot.send_message(message.from_user.id, 'Ok. I remembered.')
    except KeyError:
        bot.send_message(message.from_user.id, 'Bad! You have no such place.')

@bot.message_handler(commands=['get_place_list'])
@auth
def get_place_list(message):
    try:
        bot.send_message(message.from_user.id, ",".join(sponsorsList[message.from_user.id].sposorsPoints.keys()))
    except Exception:
        bot.send_message(message.from_user.id, "List empty")

@bot.message_handler(commands=['sponsor_help'])
def sponsor_help(message):
	bot.reply_to(message, 
    """
    /get_sponsor - to become sponsor
    /cash_balance - to find out the balance
    /put_money - to put money into the account
    /add_place - to add a sponsorship place
    /del_place - to remove sponsorship place
    /get_place_list - to display all sponsorship places
    If the teams do not work you are not verified.
    """)

@bot.message_handler(commands=['cash_balance'])
@auth
def cash_balance(message):
    bot.send_message(message.from_user.id, "You have " + str(sponsorsList[message.from_user.id].balance))

@bot.message_handler(commands=['put_money'])
@auth
def put_money(message):
    bot.send_message(message.from_user.id, "Enter sum:")
    bot.register_next_step_handler(message, put_money_ver)

def put_money_ver(message):
    sponsorsList[message.from_user.id].balance += 1000# for test
    bot.send_message(message.from_user.id, "Payment in amount " + str(message.text))

bot.polling()