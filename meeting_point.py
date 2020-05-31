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

	print(len(data['elements']))

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


def findMiddlePoint(sponsorСoordinates, usersCoordinates):
	sponsorsMidpoint = toupleMean(sponsorСoordinates)
	usersMidpoint = toupleMean(usersCoordinates)	

	sponsorsWeight = 3
	Midpoint = [
		(sponsorsWeight * sponsorsMidpoint[0] + usersMidpoint[0]) / (sponsorsWeight + 1), 
		(sponsorsWeight * sponsorsMidpoint[1] + usersMidpoint[1]) / (sponsorsWeight + 1)
	]

	print(sponsorsMidpoint)
	print(usersMidpoint)
	print(Midpoint)

	isEmptyPlace = False
	while isEmptyPlace == False:
		delta = 0.0001
		newX = random.uniform(Midpoint[0] - delta, Midpoint[0] + delta)
		newY = random.uniform(Midpoint[1] - delta, Midpoint[1] + delta)
		Midpoint = [newX, newY]
		isEmptyPlace = OCM_buildingСheck(Midpoint)

	return Midpoint


sponsor = [[4,10], [3,5], [8,10]]
users = [[80,10], [10,5], [8,30]]

print(findMiddlePoint(sponsor, users))