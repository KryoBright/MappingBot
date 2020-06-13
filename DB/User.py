from string import Template
from init import session

class User:
	telegrammUserId = None
	roomName = None
	roomId = None
	lat = None
	lon = None

def addUser(user):
	query = Template("CREATE (N:USER {telegrammUserId:'$telegrammUserId',roomId:'$roomId', roomName:'$roomName', lat:'$lat', lon:'$lon'})")
	session.run(query.substitute(telegrammUserId=user.telegrammUserId, roomId=user.roomId, roomName=user.roomName, lat=user.lat, lon=user.lon))

user = User()
user.telegrammUserId = 246375635543
user.roomId = 34
user.roomName = 'Ivan'
user.lat = 324.3243
user.lon = -43.342

addUser(user)


def userPropUpdate(telegrammUserId, prop, value):
	query = Template("MATCH (x:USER) where x.telegrammUserId='$telegrammUserId' SET x.$prop = '$value'  return (x)")
	session.run(query.substitute(telegrammUserId=telegrammUserId, prop=prop, value=value))

userPropUpdate(246375635543, 'roomName', 'mark')

def getUsers():
	return session.run("MATCH (x:USER) return (x)")


users = getUsers()
for user in users:
	print(user)