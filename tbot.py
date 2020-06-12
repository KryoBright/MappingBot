import telebot
import re
from threading import Timer,Thread,Event
import hashlib
import time

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
rooms_pass={}
last_clear=[0]

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
@bot.message_handler(regexp="\/set_pass .+")
def room_create(message):
	message.text = ' '.join(message.text.split())
	passwd=re.search(r".+",message.text[10::]).group(0)
	passwd_n=re.search(r"[0-9a-zA-Z]+",message.text[10::]).group(0)
	userId = message.from_user.id
	if (passwd!=passwd_n):
		bot.send_message(userId,"Your password seems to be unrecognized. Perhaps, you used not allowed symbol?")
	else:
		for user in users:
			if (user[0] == userId):
				if (user[2] == -1):
					bot.send_message(userId,"You can only use this command in room!")
				else:
					rooms_pass[int(user[2])]=hashlib.md5(passwd.encode('utf-8')).hexdigest()


#OK
@bot.message_handler(regexp="\/create_room .+")
def room_create(message):
	message.text = ' '.join(message.text.split())
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
                    
@bot.message_handler(regexp="\/leave_room")
def leaveRoomCom(message):
	userId=message.from_user.id
	room_id=-1
	for user in users:
		if (user[0] == userId):
			room_id=user[2]
	if (room_id==-1):
		bot.send_message(userId,"You are currently not in the room")
	else:
		leaveRoom(userId,room_id)
    
	
@bot.message_handler(regexp="\/join_room [0-9]+:[0-9a-zA-Z]+ .+")
def room_join(message):
	message.text = ' '.join(message.text.split())
	res=re.search(r"([0-9]+):([0-9a-zA-Z]+) (.+)",message.text[11::])
	roomId=res.group(1)
	pswd_dg=hashlib.md5(res.group(2).encode('utf-8')).hexdigest()
	nick=res.group(3)
	userId = message.from_user.id
	happen=False
	for r_tm in rooms_pass:
		if (r_tm==int(roomId))and(rooms_pass[r_tm]==pswd_dg):
			happen=True
			print(roomId)
			print(nick)
			isFound = False
			for user in users:
				if (user[0] == userId):
					isFound = True
			if (not isFound):
				users.append([userId, message.from_user.username,-1])
			roomFound=False
			for r in rooms:
				if (r[0]==int(roomId)):
					roomFound=True
			if not(roomFound):
				bot.send_message(userId,"Wrong room ID")
			else:
				joinRoom(int(roomId),userId,nick)
	if not(happen):
		bot.send_message(userId,"This room is not protected by password or it is incorrect")
	
#OK
@bot.message_handler(regexp="\/join_room [0-9]+ .+")
def room_join(message):
	message.text = ' '.join(message.text.split())
	res=re.search(r"([0-9]+) (.+)",message.text[11::])
	roomId=res.group(1)
	nick=res.group(2)
	print(roomId)
	print(nick)
	room_prot=False
	for r in rooms_pass:
		if (r==int(roomId)):
			room_prot=True
	userId = message.from_user.id
	if (room_prot):
		bot.send_message(userId,"Room protected by password")
	else:
		isFound = False
		for user in users:
			if (user[0] == userId):
				isFound = True
		if (not isFound):
			users.append([userId, message.from_user.username,-1])
		roomFound=False
		for r in rooms:
			if (r[0]==int(roomId)):
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
		print(f'Room {roomId} : {text1}')
		for tmpu in rc[1::2]:
			if not(tmpu==userId):
				bot.send_message(tmpu,text1)

#Overall OK.Needs check for optimization
def main_process():
	upd_locations()
	if ((time.time()-last_clear[0])>10):
		rooms_clean()
		last_clear[0]=time.time()
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

def rooms_clean():
	k=[]
	for r in rooms:
		if (len(r))>1:
			k.append(r)
	rooms[:]=k
	
last_clear[0]=0
t = perpetualTimer(2,main_process)
t.start()
bot.polling() 