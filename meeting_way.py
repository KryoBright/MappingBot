import requests 

def getRoute(From, To):
	# alternatives=true - параметр для получения нескольких возможных путей
	response = requests.get(f"https://routing.openstreetmap.de/routed-bike/route/v1/driving/{From[0]},{From[1]};{To[0]},{To[1]}?steps=true")
	data = response.json()

	steps = []
	lengthSteps = len(data['routes'][0]['legs'][0]['steps'])
	for i in range(lengthSteps):
		step = data['routes'][0]['legs'][0]['steps'][i]['maneuver']['location']
		steps.append(step)

	return steps


def getRoutePatch(From, To):
	return f"https://ru.distance.to/{From[0]},{From[1]}/{To[0]},{To[1]}"



print(getRoutePatch([49.97998046875,50.72507306341435], [48.6,50.72167742756552]))