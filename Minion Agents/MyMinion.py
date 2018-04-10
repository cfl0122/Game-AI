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
from moba import *

# Yuen Han Chan
class MyMinion(Minion):
	
	def __init__(self, position, orientation, world, image = NPC, speed = SPEED, viewangle = 360, hitpoints = HITPOINTS, firerate = FIRERATE, bulletclass = SmallBullet):
		Minion.__init__(self, position, orientation, world, image, speed, viewangle, hitpoints, firerate, bulletclass)
		self.states = [Idle, AttackTarget, Shoot]

	def start(self):
		Minion.start(self)
		self.changeState(Idle)

	def update(self, delta):
		Minion.update(self, delta)


############################
### Idle
###
### This is the default state of MyMinion. The main purpose of the Idle state is to figure out what state to change to and do that immediately.

class Idle(State):
	
	def enter(self, oldstate):
		State.enter(self, oldstate)
		# stop moving
		self.agent.stopMoving()
	
	def execute(self, delta = 0):
		State.execute(self, delta)
		### YOUR CODE GOES BELOW HERE ###
		team = self.agent.getTeam()

		towers = self.agent.world.getEnemyTowers(team)
		base = self.agent.world.getEnemyBases(team)
		enemies = self.agent.world.getEnemyNPCs(team)
		enemyInRange = closestEnemyInRange(self.agent)
		teamBase = self.agent.world.getBaseForTeam(team)
		if(enemyInRange!=None):
			# print "enemyInRange"
			self.agent.changeState(Shoot,enemyInRange)
		elif(len(towers)>0):
			# print "tower Attack"
			self.agent.changeState(AttackTarget,towers[0])
		# elif ((self.agent.getHitpoints()<=5) and (len(teamBase)>0)):
		# 	print "Recharge"
		# 	self.agent.changeState(Recharge)
		elif len(base)>0:
			# print "base Attack"
			self.agent.changeState(AttackTarget,base[0])
		else:
			# print "hit Enemy"
			hit_Enemy = closestEnemy(enemies,self.agent)
			if(hit_Enemy!=None):
				self.agent.changeState(AttackTarget,hit_Enemy)
			else:
				return None;
		return None

##############################
### Taunt
###
### This is a state given as an example of how to pass arbitrary parameters into a State.
### To taunt someome, Agent.changeState(Taunt, enemyagent)

class Taunt(State):

	def parseArgs(self, args):
		self.victim = args[0]

	def execute(self, delta = 0):
		if self.victim is not None:
			print "Hey " + str(self.victim) + ", I don't like you!"
		self.agent.changeState(Idle)

##############################
### YOUR STATES GO HERE:

class AttackTarget(State):
	def parseArgs(self, args):
		self.target = args[0]

	def enter(self, oldstate):
		State.enter(self, oldstate)
		if(self.target==None):
			self.agent.changeState(Idle)
		targetLocation = self.target.getLocation()
		self.agent.navigateTo(targetLocation)

	def execute(self, delta = 0):
		State.execute(self, delta)
		agentLocation = self.agent.getLocation()
		targetLocation = self.target.getLocation()
		if not self.target.alive:
			self.agent.changeState(Idle)
		distanceBetween = distance(agentLocation, targetLocation)
		if(distanceBetween<=BULLETRANGE):
			close_teammate = closetTeammate(self.agent)
			if(close_teammate!=None):
				if(distance(close_teammate.getLocation(), agentLocation) > 30):
					self.agent.stopMoving()

		canFire = self.agent.canFire
		if canFire:
			if(distanceBetween<BULLETRANGE):
				self.agent.turnToFace(targetLocation)
				self.agent.shoot()

		if((not self.agent.isMoving) and (distanceBetween>BULLETRANGE)):
			self.agent.changeState(Idle)

class Recharge(State):
	def enter(self, oldstate):
		State.enter(self, oldstate)
		baseLocation = self.agent.world.getBaseForTeam(team).getLocation()
		if(baseLocation!=None):
			self.agent.navigateTo(targetLocation)

	def execute(self, delta = 0):
		State.execute(self, delta)
		if(self.agent.getHitpoints()>5):
			self.agent.changeState(Idle)

class Shoot(State):
	def parseArgs(self, args):
		self.target = args[0]

	def execute(self, delta = 0):
		State.execute(self, delta)
		canFire = self.agent.canFire
		if canFire:
			targetLocation = self.target.getLocation()
			distanceBetween = distance(self.agent.getLocation(),targetLocation)
			if(distanceBetween<BULLETRANGE):
				self.agent.turnToFace(targetLocation)
				self.agent.shoot()
		self.agent.changeState(Idle)


def closetTeammate(agent):
	team = agent.getTeam()
	sameTeamMembers = agent.world.getNPCsForTeam(team)
	returnTeammate = None;
	agentLocation = agent.getLocation()
	filterList = []
	for members in sameTeamMembers:
		if not members.isMoving():
			filterList.append(members)
	if len(filterList) > 0:
		return min(filterList, key=lambda teammate: distance(teammate.getLocation(), agentLocation))
	return returnTeammate

def closestEnemy(enemies,agent):
	close_enemy = None
	if(enemies!=None):
		minDistance = float("inf")
		agentLocation = agent.getLocation()
		for members in enemies:
			teammate_location = members.getLocation()
			distanceBetweenTwo = (distance(agentLocation, teammate_location)<minDistance)
			if(distanceBetweenTwo<minDistance):
				minDistance = distanceBetweenTwo
				close_enemy = members
	return close_enemy

def closestEnemyInRange(agent):
	enemies = agent.world.getEnemyNPCs(agent.getTeam())
	if(enemies!=None):
		if(len(enemies)>0):
			agentLocation = agent.getLocation()
			temp_enem = min(enemies, key=lambda enemy: distance(enemy.getLocation(), agentLocation))
			if(distance(temp_enem.getLocation(),agent.getLocation())<BULLETRANGE):
				return temp_enem
			else:
				return None
	return None
