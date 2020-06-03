import requests
import json
import random


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


def findMiddlePoint(sponsorСoordinates, usersCoordinates):
	sponsorСoordinates = sponsorСoordinatesIntoUsersCoordinates(sponsorСoordinates, usersCoordinates)

	sponsorsMidpoint = toupleMean(sponsorСoordinates)
	usersMidpoint = toupleMean(usersCoordinates)	

	[sponsorsMidpoint, usersMidpoint] = exactToupleMeans(sponsorСoordinates, usersCoordinates, sponsorsMidpoint, usersMidpoint)
	sponsorsWeight = 2
	Midpoint = [
		(sponsorsWeight * sponsorsMidpoint[0] + usersMidpoint[0]) / (sponsorsWeight + 1), 
		(sponsorsWeight * sponsorsMidpoint[1] + usersMidpoint[1]) / (sponsorsWeight + 1)
	]

	#print(sponsorsMidpoint)
	#print(usersMidpoint)
	#print(Midpoint)

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