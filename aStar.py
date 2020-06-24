import requests
import json


def push_OCM_coord_to_grid(X, Y, grid):
	overpass_url = "http://overpass-api.de/api/interpreter"
	overpass_query = f"""	
		[out:json];
		node({X[0]},{Y[0]},{X[1]},{Y[1]}); 
		out;
	"""
	response = requests.get(overpass_url, params={'data': overpass_query})
	data = response.json()
	elements = data['elements']

	buildingCoords = []

	for element in elements:
		buildingCoords.append([round(element['lat'], 5), round(element['lon'], 5)])
		grid[int(round(element['lat'] - X[0], 5) * 100000)][int(round(element['lon'] - Y[0], 5) * 100000)] = 1

	
	for i in range(int(round((X[1] - X[0]),5) * 100000)):
		for j in range(int(round((Y[1] - Y[0]), 5) * 100000)):
			if(grid[i][j] == 1):
				print(1)

	#print(grid)
	return grid



def generate_empty_grid(X, Y):
	delta = 0.00001
	print(delta)
	grid = []

	deltaY = Y[0]
	while(deltaY <= Y[1]):
		row = []
		deltaX = X[0]
		while(deltaX <= X[1]):
			row.append(0)
			deltaX += delta		
		deltaY +=delta
		grid.append(row)
	return grid


def a_star(userCoord, midPoint):
	gridX = [userCoord[0], midPoint[0]] if (userCoord[0] < midPoint[0]) else [midPoint[0], userCoord[0]] # [minX, maxX]
	gridY = [userCoord[1], midPoint[1]] if (userCoord[1] < midPoint[1]) else [midPoint[1], userCoord[1]] # [minY, maxY]

	grid = generate_empty_grid(gridX, gridY)
	grid = push_OCM_coord_to_grid(gridX, gridY, grid)



target = [12.3, -13.8]
#coord = [12.25, -13.75]
coord = [12.29, -13.79]

a_star(coord, target)	