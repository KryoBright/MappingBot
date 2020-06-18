import telebot
import random

bot = telebot.TeleBot("1132979507:AAG92LMX_Wn-a6SrdYcA2pvadQBDvrkJULs")

class SponsorProfile:
    def __init__(self):
        self.userId = -1
        self.name = ""
        self.about = ""
        self.balance = 0
        self.sposorsPoints = {}

class SponsorPoint:
    def __init__(self):
        self.SponsorProfile = None
        self.name = ""
        self.about = ""
        self.latitude = 0
        self.longitude = 0

class SponsorData:
    def __init__(self):
        self.sponsorsList = {}
        
    def getAllSponsors(self):
        return self.sponsorsList
    
    def addNewSponsor(self, sponsorProfileIn):
        self.sponsorsList[sponsorProfileIn.userId] = sponsorProfileIn 
        
    def getSponsorById(self, userId):
        for sponsor in self.sponsorsList.values():
            if(sponsor.userId == userId):
                return sponsor
        return None
    
    def getSponsorByPoint(self, point):
        if(point):
            return point.SponsorProfile
        return None
        
    def getAllPoints(self):
        res = []
        for sponsor in self.sponsorsList:
            for sponsorPoint in sponsor.sposorsPoints:
                res.append(sponsorPoint)
        return res
    
    def addNewPoint(self, UserId, Point):
        Sponsor = self.getSponsorById(userId)
        Sponsor.sposorsPoints[Point.name] = Point
    
    def getPointsBySposorId(self, userId):
        if(self.getSponsorById(userId)):
            return self.getSponsorById(userId).sposorsPoints
        return None
        
    def getPointsBySponsorIdAndName(self, userId, pointName):
        if((self.getSponsorById(userId)) and (pointName in self.getSponsorById(userId).sposorsPoints)):
            return SponsorData.getSponsorById(userId).sposorsPoints[pointName]
        return None

    def delPoint(self, userId, pointName):
        if(self.getPointsBySponsorIdAndName(userId, pointName)):
            del self.getSponsorById(userId).sposorsPoints[pointName]
            return True
        return False
    
SponsorData = SponsorData()

tempRegistarationData = {}

def auth(fn):
    def wrapped(message):
        if(SponsorData.getSponsorById(message.from_user.id)):
            return fn(message)
        else:
            return bot.send_message(message.from_user.id, 'You are not verified')
    return wrapped

    
@bot.message_handler(commands=['get_sponsor'])
def get_sponsor(message):
    bot.send_message(message.from_user.id, "Enter company name:")
    bot.register_next_step_handler(message, get_sponsor_about)

def get_sponsor_about(message):
    name = message.text
    bot.send_message(message.from_user.id, "Enter about company:")
    bot.register_next_step_handler(message, get_reg_sponsor, name)

def get_reg_sponsor(message, name):
    Profile = SponsorProfile()
    Profile.userId = message.from_user.id
    Profile.name = name
    about = message.text
    Profile.about = about
    SponsorData.addNewSponsor(Profile)
    print("Company ", name, " with about", about, " now can use the sponsorship interface")
    bot.send_message(message.from_user.id, 'Ok. I remembered. Now you can use the sponsorship interface')    
    

@bot.message_handler(commands=['add_place'])
@auth
def add_place(message):
    bot.send_message(message.from_user.id, "Enter place name:")
    bot.register_next_step_handler(message, add_place_about)
    
def add_place_about(message):
    name = message.text
    if(SponsorData.getPointsBySponsorIdAndName(message.from_user.id, name)):
        print("Place: ", message.text, " such a place already exists")
        bot.send_message(message.from_user.id, 'You already have a point with that name')
    else:
        bot.send_message(message.from_user.id, "Enter about place:")
        bot.register_next_step_handler(message, get_reg_name, name)

def get_reg_name(message, name):
    global tempRegistarationData
    about = message.text
    Profile = SponsorData.getSponsorById(message.from_user.id)
    tempRegistarationData[message.from_user.id] = (name, about)
    print("Place ", name, "with about", about, " place successfully registered and waiting for sending coordinates")
    bot.send_message(message.from_user.id, 'Ok. I remembered. Now share the location of the point')
        

@bot.message_handler(content_types=['location'])
@auth
def handle_location(message):
    global tempRegistarationData
    if(not(message.from_user.id in tempRegistarationData) or (tempRegistarationData[message.from_user.id] is None)):
        pass
    else:
        Profile = SponsorData.getSponsorById(message.from_user.id)
        Point = SponsorPoint()
        data = tempRegistarationData[message.from_user.id]
        Point.name = data[0]
        Point.about = data[1]
        Point.latitude = message.location.latitude
        Point.longitude = message.location.longitude
        Profile.sposorsPoints[Point.name] = Point
        Point.SponsorProfile = Profile
        tempRegistarationData[message.from_user.id] = None
        print("Coordinates received: Latitude: ", message.location.latitude, " Longitude: ", message.location.longitude)
        bot.send_message(message.from_user.id, 'Good. I remembered')

@bot.message_handler(commands=['del_place'])
@auth
def del_place(message):
    bot.send_message(message.from_user.id, "Enter place name:")
    bot.register_next_step_handler(message, get_del_name)

def get_del_name(message):
    temp = SponsorData.delPoint(message.from_user.id, message.text)
    if(temp):
        print("Place: ", message.text, " removed")
        bot.send_message(message.from_user.id, 'Ok. I remembered')
    else:
        print("Place: ", message.text, " not deleted because it does not exist")
        bot.send_message(message.from_user.id, 'Bad! You have no such place')

@bot.message_handler(commands=['get_place_list'])
@auth
def get_place_list(message):
    try:
        bot.send_message(message.from_user.id, ",".join(SponsorData.getPointsBySposorId(message.from_user.id).keys()))
    except Exception:
        bot.send_message(message.from_user.id, "List empty")

@bot.message_handler(commands=['sponsor_help'])
def sponsor_help(message):
	bot.send_message(message.from_user.id, 
    """
    /get_sponsor - to become sponsor
    /cash_balance - to find out the balance
    /put_money - to put money into the account
    /add_place - to add a sponsorship place
    /del_place - to remove sponsorship place
    /get_place_list - to display all sponsorship places
    If the commands do not work you are not verified.
    """)

@bot.message_handler(commands=['cash_balance'])
@auth
def cash_balance(message):
    bot.send_message(message.from_user.id, "You have " + str(SponsorData.getSponsorById(message.from_user.id).balance))

@bot.message_handler(commands=['put_money'])
@auth
def put_money(message):
    bot.send_message(message.from_user.id, "Enter sum:")
    bot.register_next_step_handler(message, put_money_ver)

def put_money_ver(message):
    if(str(message.text).isdigit()):
        SponsorData.getSponsorById(message.from_user.id).balance += int(message.text)# for test
        print("Payment in amount: ", message.text)
        bot.send_message(message.from_user.id, "Payment in amount " + str(message.text))
    else:
        print("Incorrect payment amount: ", message.text)
        bot.send_message(message.from_user.id, "Bad! You entered is not the amount")

bot.polling()