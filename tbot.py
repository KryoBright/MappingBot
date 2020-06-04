import telebot
import re
from threading import Timer,Thread,Event


class perpetualTimer():

   def __init__(self,t,hFunction):
      self.t=t
      self.hFunction = hFunction
      self.thread = Timer(self.t,self.handle_function)

   def handle_function(self):
      self.hFunction()
      self.thread = Timer(self.t,self.handle_function)
      self.thread.start()

   def start(self):
      self.thread.start()

   def cancel(self):
      self.thread.cancel()

import meeting_point

# средняя точка, формулы в соседнем файле
sponsor = [[12,10], [3,5], [8,10]]
users = [[80,10], [10,5], [8,30]]
print(meeting_point.findMiddlePoint(sponsor, users))


bot = telebot.TeleBot("1132979507:AAG92LMX_Wn-a6SrdYcA2pvadQBDvrkJULs")

users = []
last = ["ls"]
rooms = []
room_id=[0]
users_messages={}
i_tmp=[0]
rooms_running=[]

####### auth модуль
admins = ['KryoBright','Egor_Pashkow','Mark_Kislov']
def auth(fn):
    def wrapped(message):
        print(message.from_user.username)
        if(message.from_user.username in admins):
            return fn(message)
        else:
            return bot.send_message(message.from_user.id, 'Need admin rights')
    return wrapped
#######

#PLACEHOLDER.Not used.Feel free to remove
def get_location():
	i_tmp[0]+=1
	return [i_tmp[0],i_tmp[0]]

cords = {}

#OLD.Needs rework
help_commans_keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
help_commans_keyboard.row('/help', '/create_room', '/join_room', '/leave_room', '/meeting')
@bot.message_handler(commands=['commands', 'c'])
def help_commands_menu(message):
	bot.send_message(message.chat.id, 'Available commands:', reply_markup=help_commans_keyboard)

#OK
@bot.message_handler(commands=['start'])
def send_welcome(message):
	bot.reply_to(message, "Hi, I am ready to help you")
	userId = message.from_user.id
	print(f'User {message.from_user.username} started using bot!')
	isFound = False
	for user in users:
		if (user[0] == userId):
			isFound = True
	if (not isFound):
		users.append([userId, message.from_user.username,-1])
		print("User added to list of users")

#OK
@bot.message_handler(regexp="\/create_room .+")
def room_create(message):
	nick=re.search(r".+",message.text[13::]).group(0)
	userId = message.from_user.id
	isFound = False
	for user in users:
		if (user[0] == userId):
			isFound = True
	if (not isFound):
		users.append([userId, message.from_user.username,-1])
		print("User added to list of users")
	rooms.append([room_id[0]])
	print(f'User {message.from_user.username} created room {room_id[0]} as {nick}')
	joinRoom(room_id[0],userId,nick)
	room_id[0]+=1

#OK
def joinRoom(room_id,userId,nick):
	for user in users:
			if (user[0] == userId):
				if not(user[2] == -1):
					leaveRoom(userId,user[2])
	for i in rooms:
		if (i[0] == room_id):
			i.append(userId)
			i.append(nick)
	for user in users:
		if (user[0] == userId):
			user[2]=room_id
			text="You joined the room "+str(room_id)+" as "+nick
			print(f'User with id {userId} joined room {room_id} as {nick}')
			bot.send_message(user[0],text)

#OK
def leaveRoom(userId,room_id):
	for i in rooms:
		if (i[0] == room_id):
			for ind,u in enumerate(i[1::2]):
				if (u == userId):
					i.pop(ind*2+1)
					i.pop(ind*2+1)
					text="You left room "+str(room_id)
					bot.send_message(userId,text)
					print(f'User with id {userId} left room {room_id}')
                    
@bot.message_handler(regexp="\/leave_room .+")
def leaveRoomCom(message):
    res = re.search(r"(.+)",message.text[12::])
    room_id = res.group(1)
    leaveRoom(message.from_user.id,room_id)
    
#OK
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
		users.append([userId, message.from_user.username,-1])
	roomFound=False
	for r in rooms:
		if (str(r[0])==roomId):
			roomFound=True
	if not(roomFound):
		bot.send_message(userId,"Wrong room ID")
	else:
		joinRoom(int(roomId),userId,nick)

#DEPRECATED. Check for safe delete
#@bot.message_handler(regexp="\/say_room .+")
def room_say(message):
	text=re.search(r".+",message.text[10::]).group(0)
	userId = message.from_user.id
	roomId=-1
	for u in users:
		if (u[0] == userId):
			roomId=u[2]
	if (roomId==-1):
		bot.send_message(userId,"You should be in room to execute this command")
	else:
		rc=[]
		for r in rooms:
			if (r[0]==roomId):
				rc=r
		un=""
		for i,t in enumerate(rc):
			if (t==userId):
				un=rc[i+1]
		text1=un+" says: "+text
		for tmpu in rc[1::2]:
			if not(tmpu==userId):
				bot.send_message(tmpu,text1)

#ADMIN COMMAND.Expend admins list
@bot.message_handler(commands=["rooms"])
@auth
def all_send(message):
	for r in rooms:
		text=""
		for t in r:
			text=text+str(t)
			text=text+","
		bot.send_message(message.from_user.id,text)

#Handles base location.Need to expand.Check wiki/bugs for more info
@bot.message_handler(content_types=['location'])
def handle_location(message):
    cords[message.from_user.id] = [message.location.latitude, message.location.longitude,message.message_id,message.from_user.id]
    print(cords)

#OK.Need to expand.Check wiki/bugs for more info
#@bot.message_handler(commands=["updateLoc"])
def upd_locations():
	for c in cords:
		msg=bot.forward_message(users[0][0],cords[c][3],disable_notification=True,message_id=cords[c][2])
		print(msg.location.latitude)
		print(msg.location.longitude)
		cords[c][0]=msg.location.latitude
		cords[c][1]=msg.location.longitude
		bot.delete_message(users[0][0],msg.message_id)

#Overall OK.Needs fix.Check wiki/bugs for more info
#@bot.message_handler(commands=['send_loc'])
def update_loc(user_tg_id,meetpoint):
	loc=meetpoint
	ind=-1
	for c in users_messages:
		if (c == user_tg_id):
			ind=users_messages[c]
	res=False
	if (ind!=-1):
		res=bot.edit_message_live_location(chat_id=user_tg_id,message_id=ind,latitude=loc[0],longitude=loc[1])
		print(f'Updated location for user with id {user_tg_id}')
	if (res==True)or(ind == -1):
		msg=bot.send_location(user_tg_id,loc[0],loc[1],live_period=86400)
		users_messages[user_tg_id]=msg.message_id
		print(f'Resend location for user with id {user_tg_id}')

#DEPRECATED. Check for safe delete
#@bot.message_handler(commands=['cont_upd'])
def cont_upd(message):
	t = perpetualTimer(1,update_loc)
	t.start()

#OK.Arranges meetings.Needs counter command and logging
@bot.message_handler(commands=['meeting'])
def meeting_process(message):
	userId=message.from_user.id
	roomId=-1
	for u in users:
		if (u[0] == userId):
			roomId=u[2]
	if (roomId==-1):
		bot.send_message(userId,"You should be in room to execute this command")
	else:
		r_exec=False
		for tmp in rooms_running:
			r_exec=(tmp==roomId)
		if (r_exec):
			bot.send_message(userId,"Meeting point is already being calculated for your room. You can request new map message with /resend_map")
		else:
			rooms_running.append(roomId)
			bot.send_message(userId,"Your room added to list of executing rooms")
			for roomTmp in rooms:
				if (roomTmp[0]==roomId):
					for uids in roomTmp[1::2]:
						bot.send_message(uids,"Please, share LiveLocation if you want to be included to room meeting point calculations. Do not delete any messages send by you or bot from this point!")
	
#OK
@bot.message_handler(commands=['help'])
def send_help(message):
	help_text="""Commands,which can be used anytime:
	
				 /help - returns this message
				 /start - returns standart greeting
				 /sponsor_help - reterns sponsor-specific help
				 /create_room [name] - creates new room.You will have nick [name] in it
				 /join_room [room_id] [name] - used to join room with correspondig id as [name]
				 
				 Commands which require you to be in the room:
				 
				 /meeting - arranges the meeting between users
				 [Any text] - Sends this text in chat using your room nickname
				 
				 Sending unspecified text ouside the room will result in bot resending same text back
				 Sending location is possible at any time,bot will try to remember it anyway
				 Sending anything other than that is not supported at the moment.Be careful!
				 
				"""
	bot.reply_to(message, help_text)
	
###DEPRECATED. Check for safe delete

# заглушки из таска в ПМ.
@bot.message_handler(commands=['send_my_geo'])
def send_help(message):
	bot.reply_to(message, "Bot got geodata")

@bot.message_handler(commands=['create_room'])
def send_help(message):
	bot.reply_to(message, "Room created")

@bot.message_handler(commands=['show_map'])
def send_help(message):
	bot.reply_to(message, "Map shown")

@bot.message_handler(commands=['create_rout'])
def send_help(message):
	bot.reply_to(message, "Map route built")

###

#ADMIN COMMAND.Fix only admin access
@bot.message_handler(commands=['knowledge'])
@auth
def send_knowledge(message):
	s = ""
	for user in users:
		s += "," + str(user[1])
	bot.reply_to(message, s)

#ADMIN COMMAND.Expend admins list
@bot.message_handler(commands=["all"])
@auth
def all_send(message):
	for user in users:
		bot.send_message(user[0], last[0])

#OK
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	last[0] = message.text
	text=message.text
	userId = message.from_user.id
	roomId=-1
	for u in users:
		if (u[0] == userId):
			roomId=u[2]
	if (roomId==-1):
		bot.reply_to(message, message.text)
	else:
		rc=[]
		for r in rooms:
			if (r[0]==roomId):
				rc=r
		un=""
		for i,t in enumerate(rc):
			if (t==userId):
				un=rc[i+1]
		text1=un+" says: "+text
		ptint(f'Room {roomId} : {text1}')
		for tmpu in rc[1::2]:
			if not(tmpu==userId):
				bot.send_message(tmpu,text1)

#Overall OK.Needs check for optimization
def main_process():
	upd_locations()
	for tgt in rooms_running:
		for tmp in rooms:
			cords_room=[]
			if (tgt==tmp[0]):
				room_cap=0
				for uids in tmp[1::2]:
					for c in cords:
						if (c==uids):
							cords_room.append(cords[c][0:2:])
							room_cap=room_cap+1
				if (room_cap>0):
					point=meeting_point.findMiddlePoint(sponsor, cords_room)
					for uids in tmp[1::2]:
						update_loc(uids,point)
						##Can result in overposting,add sleep functions!

t = perpetualTimer(2,main_process)
t.start()
bot.polling() 