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
# Yuen Han Chan
import sys, pygame, math, numpy, random, time, copy
from pygame.locals import * 

from constants import *
from utils import *
from core import *
from mycreatepathnetwork import *
from mynavigatorhelpers import *


###############################
### AStarNavigator
###
### Creates a path node network and implements the FloydWarshall all-pairs shortest-path algorithm to create a path to the given destination.
			
public_world = None
class AStarNavigator(NavMeshNavigator):

	def __init__(self):
		NavMeshNavigator.__init__(self)
		
	# public_world = None
	### Create the pathnode network and pre-compute all shortest paths along the network.
	### self: the navigator object
	### world: the world object
	def createPathNetwork(self, world):
		self.pathnodes, self.pathnetwork, self.navmesh = myCreatePathNetwork(world, self.agent)
		public_world = world
		return None
		
	### Finds the shortest path from the source to the destination using A*.
	### self: the navigator object
	### source: the place the agent is starting from (i.e., it's q_node location)
	### dest: the place the agent is told to go to
	def computePath(self, source, dest):
		### Make sure the next and dist matricies exist
		# print "computing"
		if self.agent != None and self.world != None: 
			self.source = source
			self.destination = dest
			### Step 1: If the agent has a clear path from the source to dest, then go straight there.
			###   Determine if there are no obstacles between source and destination (hint: cast rays against world.getLines(), check for clearance).
			###   Tell the agent to move to dest
			### Step 2: If there is an obstacle, create the path that will move around the obstacles.
			###   Find the pathnodes closest to source and destination.
			###   Create the path by traversing the self.next matrix until the pathnode closes to the destination is reached
			###   Store the path by calling self.setPath()
			###   Tell the agent to move to the first node in the path (and pop the first node off the path)
			# print "original dest: ", dest
			if clearShot(source, dest, self.world.getLines(), self.world.getPoints(), self.agent):
				# print "in clearShots"
				self.agent.moveToTarget(dest)
				# drawCross(public_world.debug, dest)
			else:

				# print "in a star"
				start = findClosestUnobstructed(source, self.pathnodes, self.world.getLinesWithoutBorders())
				end = findClosestUnobstructed(dest, self.pathnodes, self.world.getLinesWithoutBorders())
				# drawCross(public_world.debug, dest, color = (200, 0, 0))
				# drawCross(public_world.debug, start, color = (200, 0, 0))
				if start != None and end != None:
					# print len(self.pathnetwork)
					newnetwork = unobstructedNetwork(self.pathnetwork, self.world.getGates())
					# print len(newnetwork)
					closedlist = []
					path, closedlist = astar(start, end, newnetwork)
					# print "path: ", path , " start: ", start , " dest: ", dest
					# prin
					if path is not None and len(path) > 0:
						path = shortcutPath(source, dest, path, self.world, self.agent)
						self.setPath(path)
						if self.path is not None and len(self.path) > 0:
							first = self.path.pop(0)
							self.agent.moveToTarget(first)
		return None
		
	### Called when the agent gets to a node in the path.
	### self: the navigator object
	def checkpoint(self):
		myCheckpoint(self)
		return None

	### This function gets called by the agent to figure out if some shortcutes can be taken when traversing the path.
	### This function should update the path and return True if the path was updated.
	def smooth(self):
		return mySmooth(self)

	def update(self, delta):
		myUpdate(self, delta)


def unobstructedNetwork(network, worldLines):
	newnetwork = []
	for l in network:
		hit = rayTraceWorld(l[0], l[1], worldLines)
		if hit == None:
			newnetwork.append(l)
	return newnetwork




def astar(init, goal, network):
	path = []
	open = []
	closed = []

	open.append(init)

	g = {}
	h = {}
	f = {}
	parent = {}
	g[init]=0
	h[init]=distance(init,goal)
	f[init]=h[init]

	while open:
		q_node = leastF(f,open)
		if q_node == goal:
			path.append(q_node)
			while q_node in parent:
				q_node = parent[q_node]
				path.append(q_node)
			path = list(reversed(path))
			return path, closed
			break

		open.remove(q_node)
		closed.append(q_node)
		children = find_q_child(q_node,network)
		for child in children:
			child_g = g[q_node] + distance(q_node,child)
			child_h = distance(child,goal)
			child_f = child_g + child_h
			if child in open:
				if f[child]<child_f:
					continue
			if child in closed:
				continue
			else:
				parent[child] = q_node
				g[child] = child_g
				h[child] = child_h
				f[child] = child_f
				if child not in open:
					open.append(child)
	# path = list(reversed(path))
	return path, closed

def find_q_child(q,network):
	childList = []
	for lines in network:
		p1 = lines[0]
		p2 = lines[1]
		if(q==p1):
			childList.append(p2)
		if(q==p2):
			childList.append(p1)
	return childList

def leastF(f,open):
	q_node = open[0]
	for open_node in open:
		if(f[open_node]<f[q_node]):
			q_node = open_node
	return q_node

def myUpdate(nav, delta):
	# path = nav.getPath()
	# gate = nav.world.getGates();
	# # print "path: ", path
	# pathLines = []
	# if(path!=None):
	# 	for x in range(len(path)-1):
	# 		pathLines.append((path[x],path[x+1]))
	# 	# print "pathLines: ", pathLines
	# 	# gateLines = gate.getGates();
	# 	for gateLine in gate:
	# 		# for pathLine in path:
	# 		# print "gateLine: ", gateLine
	# 		if rayTraceWorldNoEndPoints(gateLine[0], gateLine[1], pathLines)!=None:
	# 			nav.agent.stopMoving()
	# 			nav.setPath(None)
	# 			print ("new Destination in update: ", nav.getDestination())
	# 			nav.computePath(nav.agent.getLocation(), nav.getDestination())
	# 			print "repath needed"


	currentLocation = nav.agent.getLocation()
	dest = nav.destination
	nextLocation = nav.agent.getMoveTarget()
	gatesLines = nav.world.getLinesWithoutBorders();

	# print "nextLocation: ", nextLocation;
	if rayTraceWorldNoEndPoints(currentLocation,nextLocation,gatesLines):
	    nav.agent.stopMoving()
	    nav.setPath(None)
	    nav.computePath(currentLocation,dest)
	return None




def myCheckpoint(nav):
	### YOUR CODE GOES BELOW HERE ###
	# print "at myCheckpoint"
	# path = nav.getPath()
	# gate = nav.world.getGates();
	# print "path: ", path
	# pathLines = []
	# for x in range(len(path)-1):
	# 	pathLines.append((path[x],path[x+1]))
	# print "pathLines: ", pathLines
	# # gateLines = gate.getGates();
	# for gateLine in gate:
	# 	# for pathLine in path:
	# 	print "gateLine: ", gateLine
	# 	if rayTraceWorldNoEndPoints(gateLine[0], gateLine[1], pathLines)!=None:
	# 		nav.agent.stopMoving()
	# 		nav.setPath(None)
	# 		nav.computePath(nav.agent.getLocation(), nav.getDestination())
	# 		print "repath needed"
	### YOUR CODE GOES ABOVE HERE ###
	return None


### Returns true if the agent can get from p1 to p2 directly without running into an obstacle.
### p1: the q_node location of the agent
### p2: the destination of the agent
### worldLines: all the lines in the world
### agent: the Agent object
def clearShot(p1, p2, worldLines, worldPoints, agent):
	### YOUR CODE GOES BELOW HERE ###
	hitYet = False;
	for lines in worldLines:
		hit = rayTraceNoEndpoints(p1, p2, lines)
		if(hit!=None):
			hitYet = True
	if(hitYet):
		return False
	radius = agent.getMaxRadius()*1.5;
	line = (p1,p2);
	for points in worldPoints:
		if (minimumDistance(line,points)<radius):
			return False
	return True