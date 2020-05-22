import humans
import numpy as np

class World():
	def __init__(self, communities, travel):
		self.communities = communities
		self.travel = travel

	def __str__(self):
		out = "Communities : ["
		for c in self.communities:
			out += str(c)
		out += "]\n"
		out += "Travel Probability : " + str(self.travel)
		return out


class Community():
	def __init__(self, humans, length, coords):
		self.humans = humans
		self.length = length
		self.coords = coords

	def __str__(self):
		out = "Humans : ["
		for h in self.humans:
			out += str(h)
		out += "]\n"
		out += "Community Box Length : " + str(self.length)
		return out

	def move_humans(self):
		for h in self.humans:
			h.move(np.random.uniform(size(2)), self.coords)

		


def build_world(args):

	People = humans.create_humans(args)
	Communities = []

	comm_count = args.community_count
	comm_types = args.community_types
	length = args.community_box_length
	travel = args.community_travel

	if comm_types == 'uniform':
		comm_density = int(len(People)/comm_count)

		for i in range(int(len(People)/comm_density)):
			coords = np.array([[i*length, i*length], [(i+1)*length, (i+1)*length]])
			Communities.append(Community(People[i*comm_density : (i+1)*comm_density], length, coords))
		return World(Communities, travel)
	elif comm_types == 'real':
		# TODO
		print("Under construction")
		return World()