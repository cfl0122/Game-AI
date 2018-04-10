'''
 * Copyright (c) 2014, 2015 Entertainment Intelligence Lab, Georgia Institute of Technology.
 * Originally developed by Mark Riedl.
 * Last edited by Mark Riedl 05/2015
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
'''

import sys, pygame, math, numpy, random, time, copy
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates a grid as a 2D array of True/False values (True =  traversable). Also returns the dimensions of the grid as a (columns, rows) list.
def myCreateGrid(world, cellsize):
	grid = None
	dimensions = (0, 0)
	### YOUR CODE GOES BELOW HERE ###
	# matrix = [[False] * cellsize for i in range(5)]
	p = world.getPoints()
	width,height = p[2]

	dimensions = (int(width / cellsize), int(height / cellsize))
	matrix = numpy.ones(dimensions)
	line = []
	polygon = []
	for obstacle in world.getObstacles():
		polygon.append(obstacle.getLines())
		for o in obstacle.getLines():
			line.append(o)

	for x in range(dimensions[0]):
		for y in range(dimensions[1]):
			topLeft = (int(x*cellsize),int(y*cellsize))
			topRight = (int(x*cellsize+cellsize),int(y*cellsize))
			bottomLeft = (int(x*cellsize),int(y*cellsize+cellsize))
			bottomRight = (int(x*cellsize+cellsize),int(y*cellsize+cellsize))

			for l1,l2 in line:
				# print l1, l2
				pointsBetween1 = calculateIntersectPoint(topLeft, topRight, l1, l2);
				pointsBetween2 = calculateIntersectPoint(topLeft, bottomLeft, l1, l2);
				pointsBetween3 = calculateIntersectPoint(bottomLeft, bottomRight, l1, l2);
				pointsBetween4 = calculateIntersectPoint(topRight, bottomRight, l1, l2);

				# if(pointsBetween1!=None) and (l1[0]!=0) and (l1[1]!=0) and (l2[0]!=0) and (l2[1]!=0):
				# 	# print pointsBetween1
				# 	matrix[x][y] = 0
				if(pointsBetween1!=None) or (pointsBetween2!=None) or (pointsBetween3!=None) or (pointsBetween4!=None):
					matrix[x][y] = 0
					continue
				# if(point)
				for poly in polygon:
					# print "poly: ", poly
					# if pointInsidePolygonLines(topLeft,poly) or pointInsidePolygonLines(topRight,poly) or pointInsidePolygonLines(bottomLeft,poly) or pointInsidePolygonLines(bottomRight,poly):
					if pointInsidePolygonLines(topLeft, poly):
						# point
						matrix[x][y] = 0
						# print "hi"

			# pointsBetween = getIntersectPoint(topLeft, topRight, bottomLeft, bottomRight)
			# for obstacle in world.getObstacles():
				# for x1 in range(topLeft[0],topRight[0]):
				# 	for y1 in range(topLeft[1],bottomLeft[1]):
				# 		if obstacle.pointInside((x1,y1)):
				# 			matrix[x][y]=0
				# 			break

				# if obstacle.pointInside(topLeft) or obstacle.pointInside(topRight) or obstacle.pointInside(bottomLeft) or obstacle.pointInside(bottomRight):
				# 	matrix[x][y] = 0
				# for x1 in range(topLeft[0],topRight[0]):
				# 	if obstacle.pointInside((x1,topLeft[1])):
				# 		matrix[x][y] = 0
				# 		print("hit1 at: ", x1,topLeft[1])
				# 		continue
				# for x2 in range(bottomLeft[0],bottomRight[0]):
				# 	if obstacle.pointInside((x2, bottomLeft[1])):
				# 		matrix[x][y] = 0
				# 		print("hit2 at: ", x2, bottomLeft[1])
				# 		continue
				# for y1 in range(topLeft[1], bottomLeft[1]):
				# 	if obstacle.pointInside((topLeft[0], y1)):
				# 		matrix[x][y] = 0
				# 		print("hit3 at: ", topLeft[0], y1)
				# 		continue
				# for y2 in range(topRight[1], bottomRight[1]):
				# 	if obstacle.pointInside((topRight[0], y2)):
				# 		matrix[x][y] = 0
				# 		print("hit4 at: ", topRight[0], y2)
				# 		continue

			# print pointsBetween
				# for point in pointsBetween:
				# 	if point is not None:
				# 		print point
					# if obstacle.pointInside(point):
					# 	matrix[x][y] = 0

	print len(matrix[0]),len(matrix)   ### 26,20
	### YOUR CODE GOES ABOVE HERE ###
	grid = matrix
	#dimensions = ((matrix[0]),len(matrix))
	# dimensions = (int(math.round(width/cellsize)),int(math.round(height/cellsize)))
	return grid, dimensions

