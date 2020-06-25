import requests
import json
import random
from string import Template
import sys
sys.path.append("./DB/")
from init import session


def OCM_buildingСheck(Midpoint):
	X = Midpoint[0]
	Y = Midpoint[1]

	delta = 0.0001

	overpass_url = "http://overpass-api.de/api/interpreter"
	overpass_query = f"""	
		[out:json];
		node({X - delta},{Y - delta},{X + delta},{Y + delta}); 
		out;
	"""
	response = requests.get(overpass_url, params={'data': overpass_query})
	data = response.json()

	#print(len(data['elements']))

	if(len(data['elements']) == 0):
		return True
	else:
		return False
	

def toupleMean(list):
	meanNumberX = None 
	meanNumberY = None
	for i, touple in enumerate(list):
		if(i == 0):
			meanNumberX = touple[0]
			meanNumberY = touple[1]
		else:
			meanNumberX += touple[0]
			meanNumberY += touple[1]			
	return [meanNumberX / len(list), meanNumberY / len(list)]


def sponsorСoordinatesIntoUsersCoordinates(sponsorСoordinates, usersCoordinates):
	minUserX = 1000000000
	minUserY = 1000000000
	maxUserX = -1000000000
	maxUserY = -1000000000

	for user in usersCoordinates:
		if(user[0] < minUserX):
			minUserX = user[0]
		if(user[0] > maxUserX):
			maxUserX = user[0]
		if(user[1] < minUserY):
			minUserY = user[1]
		if(user[1] > maxUserY):
			maxUserY = user[1]

	filterSponsorСoordinates = []
	for sponsor in sponsorСoordinates:
		if (sponsor[0] >= minUserX and sponsor[0] <= maxUserX and sponsor[1] >= minUserY and sponsor[1] <= maxUserY):
			filterSponsorСoordinates.append(sponsor)

	return filterSponsorСoordinates

def calcilateDistansesArrayFromPoint(array, point):
	result = []
	for item in array:
		x = item[0] - point[0]
		y = item[1] - point[1]
		distanse = (x ** 2 + y ** 2) ** 0.5
		result.append([item[0], item[1], distanse])
	return result


def filterImpotentCoords(coords, midPoint):
	if(len(coords) <= 1):
		return coords
	coords.sort(key=lambda x: x[2])

	result = []
	for i in range(int(len(coords) / 2)):
		result.append([coords[i][0], coords[i][1]])
	return result
	

def exactToupleMeans(sponsorСoordinates, usersCoordinates, sponsorsMidpoint, usersMidpoint):
	sponsorСoordinates = calcilateDistansesArrayFromPoint(sponsorСoordinates, sponsorsMidpoint)
	usersCoordinates = calcilateDistansesArrayFromPoint(usersCoordinates, usersMidpoint)
	return [toupleMean(filterImpotentCoords(sponsorСoordinates, sponsorsMidpoint)), toupleMean(filterImpotentCoords(usersCoordinates, sponsorsMidpoint))]


def isGoodArea(Midpoint):
	radius = 0.001

	left = Midpoint[0] - radius
	right = Midpoint[0] + radius
	down = Midpoint[1] - radius
	up = Midpoint[1] + radius		
	
	query = Template("MATCH (x:RatedPoint) where x.latitude > '$left' and x.latitude < '$right' and  x.longitude > '$down' and x.longitude < '$up'  return x.latitude as latitude, x.longitude as longitude, x.mark as mark")
	points = session.run(query.substitute(left=left, right=right, down=down, up=up))

	normalizePoints = []
	for p in points:
		normalizePoints.append([p['latitude'], p['longitude'], p['mark']])
	
	isGoodPoint = 0
	for p in normalizePoints:
		if(p[2] == 'good'):
			isGoodPoint = isGoodPoint + 1
		if(p[2] == 'bad'):
			isGoodPoint = isGoodPoint - 1

	# если область рядом с вычисленной точкой "нормальная"
	if isGoodPoint >= 0:
		return True
	else:
		return False


def takeAllUserAndStockPoints():
	userPoints = session.run("MATCH (x:RatedPoint) return x.latitude as latitude, x.longitude as longitude, x.mark as mark")
	normalizeUserPoints = []
	for p in userPoints:
		normalizeUserPoints.append([p['latitude'], p['longitude'], p['mark']])

	stockPoints = session.run("MATCH (x:StockPoint) return x.latitude as latitude, x.longitude as longitude")
	normalizeStockPoints = []
	for p in stockPoints:
		normalizeStockPoints.append([p['latitude'], p['longitude']])

	return [normalizeUserPoints, normalizeStockPoints]



def isGoodForUsers(Midpoint):
	[userPoints, stockPoints]= takeAllUserAndStockPoints()
	isGoodPoint = isGoodArea(Midpoint)

	# if(isGoodPoint == True): 
	# 	return Midpoint

	while (isGoodPoint == False):
		toX = 0
		toY = 0

		for p in stockPoints:
			if(p[0] > Midpoint[0]):
				toX = toX + 1
			else:
				toX = toX - 1
			if(p[1] > Midpoint[1]):
				toY = toY + 1
			else:
				toY = toY - 1


		for p in userPoints:
			if(p[0] > Midpoint[0]):
				if(p[2] == 'good'):
					toX = toX + 1
				else:
					toX = toX - 1
			else:
				if(p[2] == 'bad'):
					toX = toX + 1
				else:
					toX = toX - 1
			if(p[1] > Midpoint[1]):
				if(p[2] == 'good'):
					toY = toY + 1
				else:
					toY = toY - 1
			else:
				if(p[2] == 'bad'):
					toY = toY + 1
				else:
					toY = toY - 1

		deltaX = 0.001
		if(toX < 0):
			deltaX = deltaX * (-1)

		deltaY = 0.001
		if(toY < 0):
			deltaY = deltaY * (-1)

		Midpoint[0] = Midpoint[0] + deltaX
		Midpoint[1] = Midpoint[1] + deltaY

		isGoodPoint = isGoodArea(Midpoint)
		

	return Midpoint


def findMiddlePoint(sponsorСoordinates, usersCoordinates):
	sponsorСoordinates = sponsorСoordinatesIntoUsersCoordinates(sponsorСoordinates, usersCoordinates)
	usersMidpoint = toupleMean(usersCoordinates)
	Midpoint=[0,0]
	if len(sponsorСoordinates) > 0:
		sponsorsMidpoint = toupleMean(sponsorСoordinates)
		[sponsorsMidpoint, usersMidpoint] = exactToupleMeans(sponsorСoordinates, usersCoordinates, sponsorsMidpoint, usersMidpoint)
		sponsorsWeight = len(sponsorСoordinates) * 2
		usersWeight = len(usersCoordinates)
		Midpoint = [
			((sponsorsWeight * sponsorsMidpoint[0]) + (usersWeight * usersMidpoint[0])) / (sponsorsWeight + usersWeight), 
			((sponsorsWeight * sponsorsMidpoint[1]) + (usersWeight * usersMidpoint[1])) / (sponsorsWeight + usersWeight)
		]
	else:
		Midpoint = [usersMidpoint[0], usersMidpoint[1]]

	#print(sponsorsMidpoint)
	#print(usersMidpoint)
	#print(Midpoint)

	Midpoint = isGoodForUsers(Midpoint)

	isEmptyPlace = False
	while isEmptyPlace == False:
		delta = 0.0001
		newX = random.uniform(Midpoint[0] - delta, Midpoint[0] + delta)
		newY = random.uniform(Midpoint[1] - delta, Midpoint[1] + delta)
		Midpoint = [newX, newY]
		isEmptyPlace = OCM_buildingСheck(Midpoint)

	return Midpoint


sponsor = [[9,10], [9,11], [9,10], [9,10]]
users = [[9,10], [8,10], [8,11]]

print(findMiddlePoint(sponsor, users))
