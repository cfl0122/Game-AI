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

import sys, pygame, math, numpy, random, time, copy, operator
from pygame.locals import *

from constants import *
from utils import *
from core import *

# Creates the pathnetwork as a list of lines between all pathnodes that are traversable by the agent.
def myBuildPathNetwork(pathnodes, world, agent = None):
	lines = [];
	lineSet = set();
	obstacleLine = []
	polygon = []
	polygonPoint = []
	thinLines = set();
	radius =agent.getMaxRadius();
	print "radius", agent.getRadius();
	for obstacle in world.getObstacles():
		polygon.append(obstacle.getLines())
		for o in obstacle.getLines():
			obstacleLine.append(o)
		for p in obstacle.getPoints():
			polygonPoint.append(p)

	for u in pathnodes:
		for v in pathnodes:
			if u==v:
				continue
			pointsBetween = rayTraceWorld(u, v, obstacleLine);
			if(pointsBetween==None):
				for points in polygonPoint:
					if (minimumDistance((u,v), points) < radius):
						thinLines.add((u,v))
				lineSet.add((u,v))

	for tl in thinLines:
		if tl in lineSet:
			lineSet.remove(tl);
		if((tl[1],tl[0])) in lineSet:
			lineSet.remove((tl[1],tl[0]));
	for r in lineSet:
		lines.append(r);
	return lines
