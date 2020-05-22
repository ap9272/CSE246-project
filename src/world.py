import humans
import random as rd
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
		# A simple way to generate communities
		people_copy = np.array(People)  # create a copy of people list
		for i in range(comm_count - 1):
			min_people = int(0.25 * people_copy.shape[0])  # min number of people in a community
			max_people = int(0.75 * people_copy.shape[0])  # max number of people to put in a community
			num_people = np.random.randint(min_people, max_people)
			people_indices = np.random.randint(0, people_copy.shape[0], num_people)
			sub_comm = [people_copy[i] for i in people_indices]
			Communities.append(Community(sub_comm, area))
			people_copy = np.delete(people_copy, people_indices)

		Communities.append(Community(people_copy.tolist(), area))  # Fill in the last community
		rd.shuffle(Communities)
		return World(Communities, travel)