from string import Template
from init import session

class User:
	telegrammUserId = None
	roomName = None
	roomId = None
	lat = None
	lon = None

	coordinatesBotMessageId = None
	coordinatesBotMessageExpiration = None
	coordinatesSelfMessageId = None
	coordinatesSelfMessageExpiration = None

	balance = 0
	password = None



def addUser(telegrammUserId):
	query = Template("CREATE (N:USER {telegrammUserId:'$telegrammUserId'})")
	session.run(query.substitute(telegrammUserId=telegrammUserId))

user = User()
user.telegrammUserId = 246375635543
user.roomId = 34
user.roomName = 'Ivan'
user.lat = 324.3243
user.lon = -43.342

#addUser(user)


def userPropUpdate(telegrammUserId, prop, value):
	query = Template("MATCH (x:USER) where x.telegrammUserId='$telegrammUserId' SET x.$prop = '$value'  return (x)")
	session.run(query.substitute(telegrammUserId=telegrammUserId, prop=prop, value=value))

#userPropUpdate(246375635543, 'roomName', 'mark')


def getUsers():
	return session.run("MATCH (x:USER) return (x)")


def getUser(telegrammUserId):
	query = Template("MATCH (x:USER) WHERE x.telegrammUserId='$telegrammUserId' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId))

users = getUsers()
for user in users:
	print(user)