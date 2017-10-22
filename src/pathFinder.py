
import heapq
from dijkstra import dijkstra, shortest_path
from driver import Driver
from obstacleAvoidance import obstacleAvoidance
from sensors import Sensors
from time import sleep

class pathFinder():
	def __init__(self, IO, OK, origin=None, target=None):
		"""
		Has information of current location using abstract representation.
		Sends abstract commands to Driver, which will convert them to meters.
		"""
		print("Pathfinder module started.")
		self.origin = origin
		self.target = target
		self.IO = IO
		self.OK = OK
		self.obstacleAvoidance = obstacleAvoidance(IO)
		self.driver = Driver(IO, OK)
		self.sensors = Sensors(IO)

	def pointAntenna(self,o,a):
		"""
		o: opposite (height ground to ceiling)
		a: adjacent (distance from location of the robot to the projection of the satellite on the ground)
		
		"""
		calibration = 7
		self.IO.servoSet(0)
		time.sleep(1.0)
		angle = np.arctan(o/a)
		angle = np.rad2deg(angle)
		self.IO.servoSet(int(angle) - calibration)    # bit off because of the gear ratio, maybe -4

	def goHome(self):
		print("goHome")

	def goTo(self, arena, origin, target):
		"""
		Given coordinates, rotate itself to face in that direction.
		Useful for connecting to a satellite.
		:map: matrix of the arena
		:origin: (x,y, thetha) tuple of current pose (in reference to the Arena Coordinate System)
		:target: (x,y) tuple of target position (in reference to the Arena Coordinate System)

		"""

		# check if target is a valid destination (i.e. not 0)
		# Find route from current coordinates to point (x,y).
		# Go in a straight line unless obstacle on the way. Plan in advance for known obstacles.
		# Plan dynamically for unforseen obstacles.
		# Djakista search around obstacles


		x = origin[0]
		y = origin[1]

		print("Going from {0} to {1}".format(origin, target))

		if arena[y][x][0] == 0:
			print("ERROR: Sorry, pick another destination. I can't go inside walls.")
			return False

		around = [(-1,-1),
				(-1,0),
				(-1,1),
				(1,-1),
				(1,0),
				(1,1),
				(0,1),
				(0,-1)]

		graph = {}

		# Create a set of nodes and edges
		# For every node in the ARENA matrix
		for x in range(arena.shape[1]):	# 0 to 29
			for y in range(arena.shape[0]): # 0 to 9
				if arena[y][x][0] == 1: # this constrains node in the graph to represent free space in the real world
					# Find legal surrounding nodes
					neighbors = {}
					for pos in around:
						a = x + pos[0]
						b = y + pos[1]
						if b >= arena.shape[0] or b < 0:		# goes outside bounds of arena
							continue
						if a >= arena.shape[1] or a < 0: 	# goes outside bounds of arena
							continue
						if arena[b][a][0] != 1: 			# neighbor node isn't free space
							continue

						neighbors[(a,b)] = 1

					graph[(x,y)] = neighbors

		dist, pred = dijkstra(graph, start=origin)

		print("Going from {0} to {1}, the shortest path is:".format(origin, target))
		print(shortest_path(graph, origin, target))


	def explore(self, objective=None):
		""" 
		Navigate the space avoiding obstacles.
		Stop on finding reflective tape.
		Adjust satellite.
		Keep going around.
		Currently the method is blind to the pose of the robot.
		"""
		print("He yo! I am on an exploration mission!")


		self.driver.go()

		while self.OK():
			self.sensors.update()
			self.obstacleAvoidance.check(self.sensors, self.driver)

            # If we detect reflective tape
			if self.sensors.light == "silver":
				print("Reflective tape -- stopping!")
				self.driver.stop()
				sleep(3)
				# self.pointAntenna()
				self.driver.go()