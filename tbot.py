import telebot

bot = telebot.TeleBot("1132979507:AAG92LMX_Wn-a6SrdYcA2pvadQBDvrkJULs")

usrs=[]
last=["ls"]

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Howdy, how are you doing?")
	us=message.from_user.id
	found=False
	for i in usrs:
		if (i[0]==us):
			found=True
	if (not found):
		usrs.append([us,message.from_user.username])

@bot.message_handler(commands=['erika'])
def send_welcome(message):
	bot.reply_to(message, "<VERY GOOD>")



@bot.message_handler(commands=['knowlege'])
def send_welcome(message):
	s=""
	for i in usrs:
		s=s+","
		s=s+str(i[1])
	bot.reply_to(message, s)


@bot.message_handler(func=(lambda message:(message.from_user.username=="KryoBright")),commands=["all"])
def all_send(message):
	for i in usrs:
		bot.send_message(i[0],last[0])
		

@bot.message_handler(func=lambda message: True)
def echo_all(message):
	last[0]=message.text
	bot.reply_to(message, message.text)


bot.polling()