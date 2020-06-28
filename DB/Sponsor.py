from string import Template
from init import session

class SponsorPoint:
	telegrammUserId = None
	lat = None
	lon = None

	rentalBeginDate = None
	rentalEndDate = None



def addSponsor(telegrammUserId, password):
	query = Template("MATCH (x:USER) where x.telegrammUserId='$telegrammUserId' SET x: SPONSOR SET x.balance=0 SET x.password='$password' return (x)")
	session.run(query.substitute(telegrammUserId=telegrammUserId, password=password))


def addSonsorPoint(telegrammUserId, lat, lon, rentalBeginDate, rentalEndDate):
	query = Template("MATCH (SPONSOR:SPONSOR) WHERE SPONSOR.telegrammUserId='$telegrammUserId' CREATE (x:SPONSOR_POINT {telegrammUserId:'$telegrammUserId', lat:'$lat', lon:'$lon', rentalBeginDate: '$rentalBeginDate', rentalEndDate:'$rentalEndDate'}) CREATE (SPONSOR_POINT)-[r:Принадлежит]->(SPONSOR)")
	session.run(query.substitute(telegrammUserId=telegrammUserId, lat=lat, lon=lon, rentalBeginDate=rentalBeginDate, rentalEndDate=rentalEndDate))

addSonsorPoint(246375635543, 23, 365, '12.02.34', '14.02.34')
addSponsor(246375635543, 'secret_password')

def getSponsors():
	return session.run("MATCH (x:SPONSOR) return (x)")

def getSponsor(telegrammUserId):
	query = Template("MATCH (x:SPONSOR) WHERE x.telegrammUserId='$telegrammUserId' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId))

def getSponsorPoints(telegrammUserId):
	query = Template("MATCH (x:SPONSOR_POINT) WHERE x.telegrammUserId='$telegrammUserId' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId))

def getSponsorPointsWithDate(telegrammUserId, dateNow):
	query = Template("MATCH (x:SPONSOR_POINT) WHERE x.telegrammUserId='$telegrammUserId' and x.rentalEndDate > '$dateNow' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId, dateNow=dateNow))

users = getSponsorPointsWithDate(246375635543, '1')
for user in users:
	print(user)