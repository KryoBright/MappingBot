from string import Template
from datetime import datetime
from init import session

def chekProp(props, prop):
	isHere = False
	for p in props:
		if(p == prop):
			isHere = True
			break
	return isHere

userProps = ['telegrammUserId', 'telegramUserName', 'latitude', 'longitude']	

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
	return session.run("MATCH (x:USER) return (x)")

def getUser(telegrammUserId):
	query = Template("MATCH (x:USER) where x.telegrammUserId='$telegrammUserId' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId))

# users = getUser(246375635549)
# for user in users:
# 	print(user)




coordinateMessageProps = ['id', 'expiration']

def addCoordinateMessage(expiration, id):
	query = Template("CREATE (x:CoordinateMessage {id:'$id', expiration:'$expiration'})")
	session.run(query.substitute(id=id, expiration=expiration))


def CoordinateMessagePropUpdate(id, prop, value):
	if(chekProp(coordinateMessageProps, prop)):
		query = Template("MATCH (x:CoordinateMessage) where x.id='$id' SET x.$prop = '$value' return (x)")
		session.run(query.substitute(id=id, prop=prop, value=value))

def removeCoordinateMessage(id):
	query = Template("MATCH (x:CoordinateMessage) where x.id='$id' DELETE (x)")
	session.run(query.substitute(id=id))

def getCoordinateMessages():
	return session.run("MATCH (x:CoordinateMessage) return (x)")

def getCoordinateMessage(id):
	query = Template("MATCH (x:CoordinateMessage) where x.id='$id' return (x)")
	return session.run(query.substitute(id=id))

#addCoordinateMessage('qwerty')

users = getCoordinateMessages()
for user in users:
	print(user)



 

#createUserMessageRels = ["Bots", "Users"]

def addUserMessageRelationship(telegrammUserId, messageId, rel):
	if(chekProp(createUserMessageRels, rel)):
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





def addUserRoomRelationship(telegrammUserId, roomId, rel):
	query = Template('MATCH (a:USER), (b:Room) WHERE a.telegrammUserId = "$telegrammUserId" AND b.id = "$roomId" CREATE (a)-[: $rel]->(b) RETURN a,b ')
	return session.run(query.substitute(telegrammUserId=telegrammUserId, roomId=roomId, rel=rel))

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

points = getMeetingPoints()
for p in points:
	print(p)

addRoomMeetingPointsRelationship(43, '2020-06-16 23:58:53.036966')