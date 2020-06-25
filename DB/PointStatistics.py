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