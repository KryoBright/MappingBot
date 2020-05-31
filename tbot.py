import re
import telebot
import meeting_point

# средняя точка, формулы в соседнем файле
#sponsor = [[12,10], [3,5], [8,10]]
#users = [[80,10], [10,5], [8,30]]
#print(meeting_point.findMiddlePoint(sponsor, users))

class UserCoordinates:
    def __init__(self):
        self.latitude = 0
        self.longitude = 0
        self.user_id = 0
        self.message_id = 0

bot = telebot.TeleBot("1132979507:AAG92LMX_Wn-a6SrdYcA2pvadQBDvrkJULs")

users = []
lastComand = ["ls"]
rooms = []
room_id = [0]
cords = {}

help_commans_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
help_commans_keyboard.row('/start', '/help', '/knowledge', '/send_my_geo', '/create_room', '/show_map', '/create_rout')#!!!

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
		users.append([userId, message.from_user.username, -1])

def joinRoom(room_id,userId,nick):
	for user in users:
			if (user[0] == userId):
				if not(user[2] == -1):
					leaveRoom(userId, user[2])
	for i in rooms:
		if (i[0] == room_id):
			i.append(userId)
			i.append(nick)
	for user in users:
		if (user[0] == userId):
			user[2] = room_id
			text = "You joined the room " + str(room_id) + " as " + nick
			bot.send_message(user[0],text)

def leaveRoom(userId,room_id):
	for i in rooms:
		if (i[0] == room_id):
			for ind, u in enumerate(i[1::2]):
				if (u == userId):
					i.pop(ind*2+1)
					i.pop(ind*2+1)
					text = "You left room " + str(room_id)
					bot.send_message(userId,text)

@bot.message_handler(regexp="\/create_room .+")
def room_create(message):
	nick = re.search(r".+",message.text[13::]).group(0)
	userId = message.from_user.id
	isFound = False
	for user in users:
		if (user[0] == userId):
			isFound = True
	if (not isFound):
		users.append([userId, message.from_user.username,-1])
	rooms.append([room_id[0]])
	joinRoom(room_id[0], userId, nick)
	room_id[0] += 1
    
@bot.message_handler(regexp="\/join_room .+ .+")
def room_join(message):
	res=re.search(r"(.+) (.+)",message.text[11::])
	roomId=res.group(1)
	nick=res.group(2)
	print(roomId)
	print(nick)
	userId = message.from_user.id
	isFound = False
	for user in users:
		if (user[0] == userId):
			isFound = True
	if (not isFound):
		users.append([userId, message.from_user.username, -1])
	roomFound = False
	for r in rooms:
		if (str(r[0]) == roomId):
			roomFound = True
	if not(roomFound):
		bot.send_message(userId,"Wrong room ID")
	else:
		joinRoom(int(roomId),userId,nick)

@bot.message_handler(regexp="\/say_room .+")
def room_create(message):
	text = re.search(r".+",message.text[10::]).group(0)
	userId = message.from_user.id
	roomId=-1
	for u in users:
		if (u[0] == userId):
			roomId = u[2]
	if (roomId == -1):
		bot.send_message(userId,"You are not currently in the room")
	else:
		rc = []
		for r in rooms:
			if (r[0] == roomId):
				rc = r
		un = ""
		for i, t in enumerate(rc):
			if(t == userId):
				un = rc[i+1]
		text1 = un + " says: " + text
		for tmpu in rc[1::2]:
			if not(tmpu == userId):
				bot.send_message(tmpu, text1)

@bot.message_handler(func=(lambda message: (message.from_user.username == "KryoBright")), commands=["rooms"])
def all_send(message):
	for r in rooms:
		text = ""
		for t in r:
			text = text + str(t) + ","
		bot.send_message(message.from_user.id,text)

#############
@bot.message_handler(content_types=['location'])
def handle_location(message):
    cord = UserCoordinates()
    cord.latitude = message.location.latitude
    cord.longitude = message.location.longitude
    cord.user_id = message.from_user.id
    cord.message_id = message.message_id
    cords[message.from_user.id] = cord
    #[message.location.latitude, message.location.longitude, message.message_id, message.from_user.id]
    print(cords)
				
@bot.message_handler(commands=["updateLoc"])
def all_send(message):
	for c in cords:
		msg = bot.forward_message(users[0][0], cords[c].user_id, disable_notification=True, message_id=cords[c].message_id)
		print(msg.location.latitude)
		print(msg.location.longitude)
		cords[c].latitude = msg.location.latitude
		cords[c].longitude = msg.location.longitude
		bot.delete_message(users[0][0], msg.message_id)
#############

@bot.message_handler(commands=['help'])
def send_help(message):
	bot.reply_to(message, "Вы можите посмотреть доступные команды /c")

# выводит пользователей в сети
@bot.message_handler(commands=['knowledge'])
def send_knowledge(message):
	bot.reply_to(message, ', '.join([str(x[1]) for x in users]))

@bot.message_handler(func=(lambda message: (message.from_user.username == "KryoBright")), commands=["all"])
def all_send(message):
	for user in users:
		bot.send_message(user[0], lastComand[0])

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	lastComand[0] = message.text
	bot.reply_to(message, message.text)

bot.polling()