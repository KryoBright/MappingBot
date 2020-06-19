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


class SponsorProfile:
    def __init__(self):
        self.userId = -1
        self.name = ""
        self.about = ""
        self.balance = 0
        self.sposorsPoints = {}

class SponsorPoint:
    def __init__(self):
        self.SponsorProfile = None
        self.name = ""
        self.about = ""
        self.latitude = 0
        self.longitude = 0

def getSponsors():
	sponsors = []
	responseSponsors = session.run("MATCH (x:SPONSOR) return x.userId AS userId, x.about AS about, x.name AS name, x.balance AS balance")
	for item in responseSponsors:
		sponsor = SponsorProfile()
		sponsor.userId = item['userId']
		sponsor.name = item['name']
		sponsor.about = item['about']
		sponsor.balance = item['balance']

		points = []
		query = Template("MATCH (x:SponsorPoint) WHERE x.SponsorProfile='$SponsorProfile' return x.SponsorProfile AS SponsorProfile, x.about AS about, x.name AS name, x.latitude AS latitude, x.longitude as longitude")
		responsePoints = session.run(query.substitute(SponsorProfile=item['userId']))

		for p in responsePoints:
			point = SponsorPoint()
			point.SponsorProfile = p['SponsorProfile']
			point.name = p['name']
			point.about = p['about']
			point.latitude = p['latitude']
			point.longitude = p['longitude']

			points.append(point)

		sponsors.append(sponsor)

	return sponsors

def getSponsor(telegrammUserId):
	query = Template("MATCH (x:SPONSOR) WHERE x.telegrammUserId='$telegrammUserId' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId))

def getSponsorPoints(telegrammUserId):
	query = Template("MATCH (x:SPONSOR_POINT) WHERE x.telegrammUserId='$telegrammUserId' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId))

def getSponsorPointsWithDate(telegrammUserId, dateNow):
	query = Template("MATCH (x:SPONSOR_POINT) WHERE x.telegrammUserId='$telegrammUserId' and x.rentalEndDate > '$dateNow' return (x)")
	return session.run(query.substitute(telegrammUserId=telegrammUserId, dateNow=dateNow))

# users = getSponsorPointsWithDate(246375635543, '1')
# for user in users:
# 	print(user)

# query = Template("CREATE (x:SPONSOR {userId:'73', name:'name', about:'about', balance:'balance', longitude:'longitude', sposorsPoints:'sposorsPoints'})")
# session.run(query.substitute())

res = getSponsors()
print(res)