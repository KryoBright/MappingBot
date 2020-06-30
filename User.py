from string import Template
from datetime import datetime
from Dbinit import session


def chekProp(props, prop):
	isHere = False
	for p in props:
		if(p == prop):
			isHere = True
			break
	return isHere

userProps = ['telegrammUserId', 'telegramUserName', 'latitude', 'longitude']	

def ensureUser(telegrammUserId, telegramUserName):
	query = Template("MERGE (User:USER {telegrammUserId:'$telegrammUserId', telegramUserName:'$telegramUserName'}) return (User)")
	session.run(query.substitute(telegrammUserId=telegrammUserId, telegramUserName=telegramUserName))

def addUser(telegrammUserId, telegramUserName):
	query = Template("CREATE (User:USER {telegrammUserId:'$telegrammUserId', telegramUserName:'$telegramUserName'}) return (User)")
	session.run(query.substitute(telegrammUserId=telegrammUserId, telegramUserName=telegramUserName))

def userPropUpdate(telegrammUserId, prop, value):
	if(chekProp(userProps, prop)):
		query = Template("MATCH (User:USER) where User.telegrammUserId='$telegrammUserId' SET User.$prop = '$value' return (User)")
		session.run(query.substitute(telegrammUserId=telegrammUserId, prop=prop, value=value))

def removeUser(telegrammUserId):
	query = Template("MATCH (User:USER) where User.telegrammUserId='$telegrammUserId' DELETE (User)")
	session.run(query.substitute(telegrammUserId=telegrammUserId))

def getUsers():
	return session.run("MATCH (x:USER) return (x.username) AS username")

def getUser(telegrammUserId):
	query = Template("MATCH (x:USER) where x.telegrammUserId='$telegrammUserId' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId))

# users = getUser(246375635549)
# for user in users:
# 	print(user)




coordinateMessageProps = ['id', 'expiration']

def addCoordinateMessage(expiration, id, tg_id):
	query = Template("CREATE (x:CoordinateMessage {id:'$id',tg_id:'$tg_id',expiration:'$expiration'}) RETURN (x)")
	session.run(query.substitute(id=id, expiration=expiration,tg_id=tg_id))


def CoordinateMessagePropUpdate(id, prop, value):
	query = Template("MATCH (x:CoordinateMessage) where x.id='$id' SET x.$prop = '$value' return (x)")
	session.run(query.substitute(id=id, prop=prop, value=value))

def removeCoordinateMessage(id):
	query = Template("MATCH (x:CoordinateMessage) where x.id='$id' DELETE (x)")
	session.run(query.substitute(id=id))

def getCoordinateMessages():
	return session.run("MATCH (x:CoordinateMessage)-[r:from_User]-(b:USER) return x.tg_id AS id")
	
	
def getCoordinateMessagesId():
	return session.run("MATCH (x:CoordinateMessage)-[r:from_User]-(b:USER) return x.id AS id")

def getCoordinateMessage(id):
	query = Template("MATCH (x:CoordinateMessage) where x.id='$id' return (x)")
	return session.run(query.substitute(id=id))
	
def getMessageUser(id):
	query = Template("MATCH (x:CoordinateMessage)-[r:from_User]-(b) where x.id='$id' return b.telegrammUserId AS telegrammUserId")
	return session.run(query.substitute(id=id))

#addCoordinateMessage('qwerty')

users = getCoordinateMessages()
for user in users:
	print(user)



 

#createUserMessageRels = ["Bots", "Users"]

def addUserMessageRelationship(telegrammUserId, messageId, rel):
	query = Template('MATCH (a:USER), (b:CoordinateMessage) WHERE a.telegrammUserId = "$telegrammUserId" AND b.id = "$messageId" CREATE (a)-[: $rel]->(b) RETURN a,b ')
	return session.run(query.substitute(telegrammUserId=telegrammUserId, messageId=messageId, rel=rel))


def removeUserMessageRelationship(telegrammUserId, messageId, rel):
	if(chekProp(createUserMessageRels, rel)):
		query = Template("MATCH (n)-[rel: $rel]->(r) WHERE n.telegrammUserId='$telegrammUserId' AND r.id='$messageId' DELETE rel")
		return session.run(query.substitute(telegrammUserId=telegrammUserId, messageId=messageId, rel=rel))

#removeUserMessageRelationship(246375635549, '2020-06-16 22:25:52.829937', 'Users')
#addUserMessageRelationship(246375635549, '2020-06-16 22:25:52.829937', "Bots")






roomProps = ['id', 'meeting', 'password']

def addRoom(id, password):
	query = Template("CREATE (x:Room {id:'$id', password:'$password'})")
	session.run(query.substitute(id=id, password=password))

def RoomPropUpdate(id, prop, value):
	if(chekProp(roomProps, prop)):
		query = Template("MATCH (x:Room) where x.id='$id' SET x.$prop = '$value' return (x)")
		session.run(query.substitute(id=id, prop=prop, value=value))

def removeRoom(id):
	query = Template("MATCH (x:Room) where x.id='$id' DELETE (x)")
	session.run(query.substitute(id=id))

def getRooms():
	return session.run("MATCH (x:Room) return (x)")

def getRoom(id):
	query = Template("MATCH (x:Room) where x.id='$id' return (x)")
	return session.run(query.substitute(id=id))

#addRoom(43, 'secret_pas')





def addUserRoomRelationship(telegrammUserId, roomId, rel, loc_name):
	query = Template('MATCH (a:USER), (b:Room) WHERE a.telegrammUserId = "$telegrammUserId" AND b.id = "$roomId" CREATE (a)-[: $rel {local_name:"$loc_name"}]->(b) RETURN a,b ')
	return session.run(query.substitute(telegrammUserId=telegrammUserId, roomId=roomId, rel=rel,loc_name=loc_name))

def removeUserRoomRelationship(telegrammUserId, roomId, rel):
	query = Template("MATCH (n)-[rel: $rel]->(r) WHERE n.telegrammUserId='$telegrammUserId' AND r.id='$roomId' DELETE rel")
	return session.run(query.substitute(telegrammUserId=telegrammUserId, roomId=roomId, rel=rel))

#addUserRoomRelationship(246375635549, 43, 'user')




meetingPointProps = ['id', 'expiration', 'latitude', 'longitude']

def addMeetingPoint(expiration, latitude, longitude):
	id = id = str(datetime.now())
	query = Template("CREATE (x:MeetingPoint {expiration:'$expiration', latitude:'$latitude', longitude:'$longitude', id:'$id'})")
	session.run(query.substitute(expiration=expiration, latitude=latitude, longitude=longitude, id=id))

def MeetingPointUpdate(id, prop, value):
	if(chekProp(meetingPointProps, prop)):
		query = Template("MATCH (x:MeetingPoint) where x.id='$id' SET x.$prop = '$value' return (x)")
		session.run(query.substitute(id=id, prop=prop, value=value))

def removeMeetingPoint(id):
	query = Template("MATCH (x:MeetingPoint) where x.id='$id' DELETE (x)")
	session.run(query.substitute(id=id))

def getMeetingPoints():
	return session.run("MATCH (x:MeetingPoint) return (x)")

def getMeetingPoint(id):
	query = Template("MATCH (x:MeetingPoint) where x.id='$id' return (x)")
	return session.run(query.substitute(id=id))





def addRoomMeetingPointsRelationship(roomId, meetingPointId):
	query = Template('MATCH (a:Room), (b:MeetingPoint) WHERE a.id = "$roomId" AND b.id = "$meetingPointId" CREATE (a)-[: has]->(b) RETURN a,b ')
	return session.run(query.substitute(roomId=roomId, meetingPointId=meetingPointId))

def removeRoomMeetingPointsRelationship(roomId, meetingPointId):
	query = Template("MATCH (n)-[rel: has]->(r) WHERE n.id='$roomId' AND r.id='$meetingPointId' DELETE rel")
	return session.run(query.substitute(roomId=roomId, meetingPointId=meetingPointId))

#addMeetingPoint('12312312', 34,23)

def getUserRoom(telegrammUserId):
	query = Template('MATCH (a:USER)-[]-(b:Room) WHERE a.telegrammUserId = "$telegrammUserId" RETURN b.id AS id ')
	return session.run(query.substitute(telegrammUserId=telegrammUserId))

	
	
def removeAllUserRooms(telegrammUserId):
	query = Template("MATCH (n)-[rel]->(r:Room) WHERE n.telegrammUserId='$telegrammUserId' DELETE rel RETURN r.id AS id")
	return session.run(query.substitute(telegrammUserId=telegrammUserId))
	
def roomPassCheck(roomId,password):
	query = Template("MATCH (r) WHERE r.id='$roomId' AND (r.password='$password' OR r.password='0') RETURN r")
	return session.run(query.substitute(roomId=roomId,password=password))

def getRoomUsers(roomId):
	query = Template('MATCH (a:USER)-[]-(b:Room) WHERE b.id = "$roomId" RETURN a.telegrammUserId AS id ')
	return session.run(query.substitute(roomId=roomId))
	
def getRoomCords(roomId):
	query = Template('MATCH (a:Room{id:"$roomId"})-[]-(b:USER)-[:from_User]-(c) RETURN c.lat AS lt,c.long AS lg')
	return session.run(query.substitute(roomId=roomId))
	
def deleteEmpty():
	return session.run('MATCH (a:Room) WHERE NOT (a)-[]-(:USER) DELETE a')
	
def deleteExpired(time):
	query = Template('MATCH (a:CoordinateMessage)-[r]-(b:USER) WHERE a.expiration<"$time" DELETE r,a')
	return session.run(query.substitute(time=time))
	
def getConnectedUsers(id):
	query = Template('MATCH (a:USER{telegrammUserId:"$id"})-[*]-(c:USER) RETURN c.telegrammUserId AS id')
	return session.run(query.substitute(id=id))
	
def getUserRoomName(id):
	query = Template('MATCH (a:USER{telegrammUserId:"$id"})-[r]-(c:Room) RETURN r.local_name AS l_name')
	return session.run(query.substitute(id=id))
	
def getUserBotMessage(id):
	query = Template('MATCH (a:USER{telegrammUserId:"$id"})-[r:from_Bot]-(b) RETURN b.lat as lat,b.long as long,b.id as id,b.tg_id as tg_id')
	return session.run(query.substitute(id=id))
	
def getUserByUsername(username):
	query = Template('MATCH (a:USER{telegramUserName:"$username"}) RETURN a.telegrammUserId AS id ')
	return session.run(query.substitute(username=username))
	
def getUsernameByUser(id):
	query = Template('MATCH (a:USER{telegrammUserId:"$id"}) RETURN a.telegramUserName AS username ')
	return session.run(query.substitute(id=id))
	
def getMaxId():
	return session.run('MATCH (a) RETURN max(toInteger(a.id)) AS id ')

def getAllIds():
	return session.run('MATCH (a:USER) RETURN a.telegrammUserId AS id ')
	
points = getMeetingPoints()
for p in points:
	print(p)

addRoomMeetingPointsRelationship(43, '2020-06-16 23:58:53.036966')