from string import Template
from init import session

class User:
	telegrammUserId = None
	roomName = None
	roomId = None
	lat = None
	lon = None

	balance = 0


class SponsorPoint:
	telegrammUserId = None
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

#addUser(user)


def userPropUpdate(telegrammUserId, prop, value):
	query = Template("MATCH (x:USER) where x.telegrammUserId='$telegrammUserId' SET x.$prop = '$value'  return (x)")
	session.run(query.substitute(telegrammUserId=telegrammUserId, prop=prop, value=value))

#userPropUpdate(246375635543, 'roomName', 'mark')


def addSponsor(telegrammUserId):
	query = Template("MATCH (x:USER) where x.telegrammUserId='$telegrammUserId' SET x: SPONSOR SET x.balance=0 return (x)")
	session.run(query.substitute(telegrammUserId=telegrammUserId))


def addSonsorPoint(telegrammUserId, lat, lon):
	query = Template("MATCH (SPONSOR:SPONSOR) WHERE SPONSOR.telegrammUserId='$telegrammUserId' CREATE (x:SPONSOR_POINT {telegrammUserId:'$telegrammUserId', lat:'$lat', lon:'$lon'}) CREATE (SPONSOR_POINT)-[r:Принадлежит]->(SPONSOR)")
	session.run(query.substitute(telegrammUserId=user.telegrammUserId,lat=user.lat, lon=user.lon))

addSonsorPoint(246375635543, 23, 365)
#addSponsor(246375635543)

def getUsers():
	return session.run("MATCH (x:USER) return (x)")

def getSponsors():
	return session.run("MATCH (x:SPONSOR) return (x)")


users = getSponsors()
for user in users:
	print(user)