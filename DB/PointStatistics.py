from string import Template
from init import session

def addUserRatedPoint(latitude, longitude, mark):
	query = Template("CREATE (x:RatedPoint {latitude:'$latitude', longitude:'$longitude', mark:'$mark'}) return (x)")
	session.run(query.substitute(latitude=latitude, longitude=longitude, mark=mark))

def removeUserRatedPoint(latitude, longitude):
	query = Template("MATCH (x:RatedPoint) WHERE x.latitude='$latitude' AND x.longitude='$longitude' DELETE (x)")
	session.run(query.substitute(latitude=latitude, longitude=longitude))


def addStockPoint(latitude, longitude):
	query = Template("CREATE (x:StockPoint {latitude:'$latitude', longitude:'$longitude'}) return (x)")
	session.run(query.substitute(latitude=latitude, longitude=longitude))

def removeStockPoint(latitude, longitude):
	query = Template("MATCH (x:StockPoint) WHERE x.latitude='$latitude' AND x.longitude='$longitude' DELETE (x)")
	session.run(query.substitute(latitude=latitude, longitude=longitude))


def removeStockPoint(latitude, longitude):
	query = Template("MATCH (x:StockPoint) WHERE x.latitude='$latitude' AND x.longitude='$longitude' DELETE (x)")
	session.run(query.substitute(latitude=latitude, longitude=longitude))



class SponsorPoint:
	def __init__(self):
		self.SponsorProfile = None
		self.name = ""
		self.about = ""
		self.image = None
		self.latitude = 0
		self.longitude = 0


def getNearestSponsorPoint(point):
	sponsorPoints = []
	arr = session.run("MATCH (x:SPONSOR_POINT) return x.SponsorProfile AS SponsorProfile, x.about AS about, x.name AS name, x.latitude AS latitude, x.longitude as longitude")
	for p in arr:
		sponsorPoint = SponsorPoint()
		sponsorPoint.SponsorProfile = p['SponsorProfile']
		sponsorPoint.name = p['name']
		sponsorPoint.about = p['about']
		sponsorPoint.image = p['image']
		sponsorPoint.latitude = p['latitude']
		sponsorPoint.longitude = p['longitude']

		sponsorPoints.append(sponsorPoint)

	if(len(sponsorPoints) == 0):
		return 'no'

	S = 1000000000
	res = sponsorPoints[0]
	for p in sponsorPoints:
		s = ((p.latitude - point.latitude) ** 2) + ((p.latitude - point.latitude) ** 2)
		if(s < S):
			S = s
			res = p

	return p


point = SponsorPoint()
point.latitude = 47
point.longitude = 82
print(getNearestSponsorPoint(point))