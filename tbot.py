import telebot
import re
from threading import Timer,Thread,Event
import hashlib
import time
import Dbinit
import User
import Sponsor
import sponsors


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


#bot = telebot.TeleBot("1132979507:AAG92LMX_Wn-a6SrdYcA2pvadQBDvrkJULs")
bot=sponsors.bot

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
	User.ensureUser(userId,message.from_user.username)

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
		r=User.getUserRoom(userId)
		time.sleep(0.1)
		if (len(r)>0):
			User.RoomPropUpdate(r[0].id, 'password',hashlib.md5(passwd.encode('utf-8')).hexdigest())


#OK
@bot.message_handler(regexp="\/create_room .+")
def room_create(message):
	message.text = ' '.join(message.text.split())
	nick=re.search(r".+",message.text[13::]).group(0)
	userId = message.from_user.id
	User.ensureUser(userId,message.from_user.username)
	new_id=list(User.getMaxId())+[]
	time.sleep(0.1)
	pure_id=new_id[0]["id"]+1
	User.addRoom(pure_id,"0")
	print(f'User {message.from_user.username} created room {room_id[0]} as {nick}')
	joinRoom(pure_id,userId,nick)
	pure_id+=1

#OK
def joinRoom(room_id,userId,nick):
	leaveRoom(userId)
	User.addUserRoomRelationship(userId, room_id, "IsInRoom",nick)
	text="You joined the room "+str(room_id)+" as "+nick
	print(f'User with id {userId} joined room {room_id} as {nick}')
	bot.send_message(userId,text)

#OK
def leaveRoom(userId):
	r=list(User.removeAllUserRooms(userId))+[]
	time.sleep(0.1)
	print(r)
	if (len(r)>0):
		print(f'User with id {userId} left room {r[0]["id"]}')
		bot.send_message(userId,"You left the room")
                    
@bot.message_handler(regexp="\/leave_room")
def leaveRoomCom(message):
	userId=message.from_user.id
	leaveRoom(userId)
    
	
@bot.message_handler(regexp="\/join_room [0-9]+:[0-9a-zA-Z]+ .+")
def room_join(message):
	message.text = ' '.join(message.text.split())
	res=re.search(r"([0-9]+):([0-9a-zA-Z]+) (.+)",message.text[11::])
	roomId=res.group(1)
	pswd_dg=hashlib.md5(res.group(2).encode('utf-8')).hexdigest()
	nick=res.group(3)
	userId = message.from_user.id
	r=User.roomPassCheck(roomId,pswd_dg)
	time.sleep(0.1)
	if (len(r)>0):
		joinRoom(int(roomId),userId,nick)
	else:
		bot.send_message(userId,"Password is incorrect or room does not exist")
	
#OK
@bot.message_handler(regexp="\/join_room [0-9]+ .+")
def room_join(message):
	message.text = ' '.join(message.text.split())
	res=re.search(r"([0-9]+) (.+)",message.text[11::])
	roomId=res.group(1)
	nick=res.group(2)
	print(roomId)
	print(nick)
	userId = message.from_user.id
	r=list(User.roomPassCheck(roomId,"0"))	
	time.sleep(0.1)
	if (len(r)==0):
		bot.send_message(userId,"Room protected by password or does not exist")
	else:
		User.ensureUser(userId,message.from_user.username)
		joinRoom(int(roomId),userId,nick)

#DEPRECATED. Check for safe delete
#@bot.message_handler(regexp="\/say_room .+")
def room_say(message):
	text=re.search(r".+",message.text[10::]).group(0)
	userId = message.from_user.id
	r=User.getUserRoom(userId)
	if (len(r)==0):
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
	message_lp=15*60+time.time()-100
	
	new_id=list(User.getMaxId())+[]
	time.sleep(0.1)
	pure_id=new_id[0]["id"]+1
	
	q=User.addCoordinateMessage(message_lp,pure_id,message.message_id)
	time.sleep(0.1)
	print(q)
	User.CoordinateMessagePropUpdate(pure_id, "lat", message.location.latitude)
	User.CoordinateMessagePropUpdate(pure_id, "long", message.location.longitude)
	User.addUserMessageRelationship(message.from_user.id,pure_id, "from_User")
	pure_id+=1

#OK.Need to expand.Check wiki/bugs for more info
#@bot.message_handler(commands=["updateLoc"])
def upd_locations():
	cs=list(User.getCoordinateMessagesId())+[]
	time.sleep(0.5)
	cf=list(User.getCoordinateMessages())+[]
	time.sleep(0.1)
	for c,cu in zip(cs,cf):		
		print(c['id'])
		us=list(User.getMessageUser(c['id']))+[]
		time.sleep(0.1)
		print(us[0]['telegrammUserId'])
		print(c['id'])
		msg=bot.forward_message(1008435394,us[0]['telegrammUserId'],disable_notification=True,message_id=cu['id'])
		print(msg.location.latitude)
		print(msg.location.longitude)
		User.CoordinateMessagePropUpdate(c['id'], "lat", msg.location.latitude)
		User.CoordinateMessagePropUpdate(c['id'], "long", msg.location.longitude)
		bot.delete_message(1008435394,msg.message_id)

#Overall OK.Needs fix.Check wiki/bugs for more info
#@bot.message_handler(commands=['send_loc'])
def update_loc(user_tg_id,meetpoint):
	loc=meetpoint
	msg=list(User.getUserBotMessage(user_tg_id))+[]
	res=False
	if (len(msg)>0):
		if ((str(msg[0]['lat'])!=str(loc[0]))or(str(msg[0]['long'])!=str(loc[1]))):
			res=bot.edit_message_live_location(chat_id=user_tg_id,message_id=msg[0]['tg_id'],latitude=round(loc[0],5),longitude=round(loc[1],5))
			print(f'Updated location for user with id {user_tg_id}')
			User.CoordinateMessagePropUpdate(msg[0]['id'], "lat", round(loc[0],5))
			User.CoordinateMessagePropUpdate(msg[0]['id'], "long", round(loc[1],5))
			return 0
	if (res==True)or(len(msg)==0):
	
		new_id=list(User.getMaxId())+[]
		time.sleep(0.1)
		pure_id=new_id[0]["id"]+1
		msg=bot.send_location(user_tg_id,loc[0],loc[1],live_period=86400)
		q=User.addCoordinateMessage(85000+time.time(),pure_id, msg.message_id)
		User.CoordinateMessagePropUpdate(pure_id, "lat", loc[0])
		User.CoordinateMessagePropUpdate(pure_id, "long", loc[1])
		print(User.addUserMessageRelationship(user_tg_id,pure_id, "from_Bot"))
		print(f'Resend location for user with id {user_tg_id}')

#OK.Arranges meetings.Needs counter command and logging
@bot.message_handler(commands=['meeting'])
def meeting_process(message):
	userId=message.from_user.id
	r=list(User.getUserRoom(userId))
	if (len(r)==0):
		bot.send_message(userId,"You should be in room to execute this command")
	else:
		print(r[0])
		roomId=r[0]['id']
		r_exec=False
		for tmp in rooms_running:
			r_exec=(tmp==roomId)
		if (r_exec):
			bot.send_message(userId,"Meeting point is already being calculated for your room. You can request new map message with /resend_map")
		else:
			rooms_running.append(roomId)
			bot.send_message(userId,"Your room added to list of executing rooms")
			usrs=list(User.getRoomUsers(roomId))+[]
			print(usrs)
			for uids in usrs:
				print(uids['id'])
				bot.send_message(uids['id'],"Please, share LiveLocation if you want to be included to room meeting point calculations. Do not delete any messages send by you or bot from this point!")
	
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
	u = list(User.getUsers())+[]
	s=""
	for y in u:
		s=s+", "+y['username']
	bot.reply_to(message, s)

#ADMIN COMMAND.Expend admins list
@bot.message_handler(commands=["all"])
@auth
def all_send(message):
	for user in users:
		bot.send_message(user[0], last[0])
		
@bot.message_handler(regexp="\/invite .+")
def invite(message):
	userId=message.from_user.id
	s_name=message.from_user.username
	r=list(User.getUserRoom(userId))
	if (len(r)==0):
		bot.send_message(userId,"You should be in room to execute this command")
	else:
		print(r[0])
		roomId=r[0]['id']
		res=re.search(r" +@?(.+)",message.text[7::])
		user_n=res.group(1)
		print(user_n)
		ind=list(User.getUserByUsername(user_n))+[]
		print(ind)
		if (len(ind)==0):
			bot.send_message(userId,"This user does not use this bot! Tell them to do it ASAP!")
		else:
			markup=telebot.types.InlineKeyboardMarkup(row_width=1)
			button1=telebot.types.InlineKeyboardButton(text="Accept",callback_data="j_room "+str(roomId)+" "+str(ind[0]['id']))
			
			button2=telebot.types.InlineKeyboardButton(text="Decline",callback_data="declined "+str(userId)+" "+str(user_n))
			
			button3=telebot.types.InlineKeyboardButton(text="Mark as spam",callback_data="spam "+str(userId))
			
			markup.add(button1)
			markup.add(button2)
			markup.add(button3)
			
			bot.send_message(ind[0]['id'],"User "+s_name+" invites you to join his room",reply_markup=markup)
			
@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
	c_data=call.data.split()
	if (c_data[0]=="j_room"):
		t_name=(list(User.getUsernameByUser(int(c_data[2])))+[])[0]
		joinRoom(int(c_data[1]),int(c_data[2]),t_name['username'])
		bot.delete_message(call.message.chat.id,call.message.message_id)
	if (c_data[0]=="declined"):
		bot.send_message(int(c_data[1]),"User "+c_data[2]+" declined your request")
		bot.delete_message(call.message.chat.id,call.message.message_id)
	if (c_data[0]=="spam"):
		print("spam")
		bot.delete_message(call.message.chat.id,call.message.message_id)
	if (c_data[0]=="j_room_nd"):
		joinRoom(int(c_data[1]),call.from_user.id,call.from_user.username)

##DEPRECATED
##Somebody,pls,think about other solution
#@bot.message_handler(regexp="\/invite_link")
def invite(message):
	userId=message.from_user.id
	s_name=""
	roomId=-1
	for u in users:
		if (u[0] == userId):
			roomId=u[2]
			s_name=u[1]
	if (roomId==-1):
		bot.send_message(userId,"You should be in room to execute this command")
	else:
		markup=telebot.types.InlineKeyboardMarkup(row_width=1)
		button1=telebot.types.InlineKeyboardButton(text="Click here to join",callback_data="j_room_nd "+str(roomId))
		markup.add(button1)
		bot.send_message(userId,"Share this message to invite users into this room",reply_markup=markup)

@bot.message_handler(commands=['give_point'])
def fake_func(message):
	ch_id=message.from_user.id
	bot.send_photo(ch_id,'https://avatars.mds.yandex.net/get-altay/2813737/2a00000171afab371a16d21aa2efd1fc7632/XXL')
	bot.send_message(ch_id,"""Добро пожаловать в «Мама, я дома!» — уютное место для ваших встреч.
⠀
	Если вы бывали в Грузии, то, наверняка, запомнили гостеприимство этой страны и радушие её жителей, а если нет, то точно наслышаны об этом. В нашем ресторане мы постарались воссоздать эту тёплую атмосферу и позаботиться о том, чтобы здесь вам было действительно хорошо.
	⠀
	В «Мама, я дома!» вы можете познакомиться с самыми популярными представителями грузинской кухни, а также насладиться уже привычными блюдами классического европейского меню.
	⠀
	Обед с коллегами, ужин с друзьями или важное семейное событие — мы поддержим любой вариант вашего отдыха!

	С нетерпением ждём новых встреч в «Мама, я дома!»
	⠀
	г. Томск, проспект Ленина, 1в, 3 этаж

	 

	Режим работы ресторана

	Работаем в режиме самовывоза и доставки
	ПН-ЧТ, ВС 10:00-22:00

	ПТ, СБ 10:00-23:00

	Режим работы доставки

	ПН-ЧТ, ВС 10:00-22:00

	ПТ, СБ 10:00-23:00

	
	Закажи онлайн на https://mama-ya-doma.ru/""")
	
#OK
@bot.message_handler(func=lambda message: True)
def echo_all(message):
	last[0] = message.text
	text=message.text
	userId = message.from_user.id
	un=list(User.getUserRoomName(userId))
	time.sleep(0.1)
	if (len(un)>0):
		usrs=list(User.getConnectedUsers(userId))+[]
		time.sleep(0.1)
		for u in usrs:
			text1=un[0]['l_name']+" says: "+text
			bot.send_message(u['id'],text1)
	else:
		bot.reply_to(message, message.text)
	

#Overall OK.Needs check for optimization
def main_process():
	upd_locations()
	if ((time.time()-last_clear[0])>10):
		all_clean()
		last_clear[0]=time.time()
	for tgt in rooms_running:
		cords_room=list(User.getRoomCords(tgt))+[]	
		time.sleep(0.1)
		print(cords_room,tgt)
		if (len(cords_room)>0):
			c_r=[]
			for c in cords_room:
				c_r.append((float(c['lt']),float(c['lg'])))
			print(c_r)
			point=meeting_point.findMiddlePoint(sponsor, c_r)
			u=User.getRoomUsers(tgt)
			time.sleep(0.1)
			for urs in u:
				update_loc(urs['id'],point)
	

time.sleep(0.1)
	
def all_clean():
	User.deleteExpired(time.time())
	time.sleep(0.1)
	User.deleteEmpty()
	
last_clear[0]=0
t = perpetualTimer(2,main_process)
t.start()
bot.polling() 