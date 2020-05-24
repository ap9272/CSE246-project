import humans
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

# To plot the humans
# TODO: expand for multiple communities
fig = plt.figure(figsize=(5,5))
ax = plt.axes()
ims=[]

# class for the whole world
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

	# Goes through one day for each community
	def update_world(self, inf_dist, inf_prob, inf_time):
		for c in self.communities:
			c.one_day(inf_dist, inf_prob, inf_time)

	# Start the world, intialize human locations and infect some humans
	def start(self, inf_init, comm_seed):
		comm_idx = np.random.randint(low=0, high=len(self.communities), size=comm_seed)
		for c in comm_idx:
			self.communities[c].initialize_human_locations()
			self.communities[c].infect(int(inf_init/len(comm_idx)))

	# Returns how many humans in which state
	def stats(self):
		SIRs = []
		for c in self.communities:
			SIRs.append(c.stats())
		return SIRs

	# Outputs the humans graph
	def print_graph(self):
		for c in self.communities:
			c.print_graph()

# class for one community
class Community():
	def __init__(self, humans, length, coords, steps_per_day):
		self.humans_S = humans
		self.humans_I = []
		self.humans_R = []
		self.length = length
		self.coords = coords
		self.steps_per_day = steps_per_day

	def __str__(self):
		out = "Susceptibile Humans : ["
		for h in self.humans_S:
			out += str(h)
		out += "]\n"
		out += "Infected Humans : ["
		for h in self.humans_I:
			out += str(h)
		out += "]\n"
		out += "Recovered Humans : ["
		for h in self.humans_R:
			out += str(h)
		out += "]\n"
		out += "Community Box Length : " + str(self.length)
		return out

	# randomly assign human locations in a box
	def initialize_human_locations(self):
		random_coords = np.random.rand(len(self.humans_S), 2)*self.length + self.coords[0][0]
		for i in range(len(self.humans_S)):
			self.humans_S[i].set_location(random_coords[i])

	# return the number of humans in each state
	def stats(self):
		return [len(self.humans_S), len(self.humans_I), len(self.humans_R)]


	# start the infection in the community
	def infect(self, inf_init):
		h_idx = np.random.randint(low=0, high=len(self.humans_S), size=inf_init)

		for i in h_idx:
			self.humans_S[i].state = 'I'
			self.humans_S[i].infected_time = 0
			self.humans_I.append(self.humans_S.pop(i))

	# goes through one day of the community
	def one_day(self, inf_dist, inf_prob, inf_time):

		# humans take multiple steps per day
		for _ in range(self.steps_per_day):
			self.move_humans()
			self.infection_spread(inf_dist, inf_prob)
			self.graph()
		# one day passes for humans (update status)
		self.humans_recover_or_die(inf_time)

	# for graphing of humans
	def graph(self):
		coords = []
		status = []

		for h in self.humans_S:
			coords.append(h.location)
			status.append(0)

		for h in self.humans_I:
			coords.append(h.location)
			status.append(1)

		for h in self.humans_R:
			coords.append(h.location)
			status.append(2)

		coords = np.array(coords)
		status = np.array(status)

		im=[ax.scatter(coords[:,0] ,coords[:,1] ,c=status)]
		ims.append(im)	

	# output the graph (function not required, can be done in world class)
	def print_graph(self):
		ani = animation.ArtistAnimation(fig, ims, interval=20, blit=True,repeat_delay=1000)
		plt.show()

	# move humans randomly (don't move 'R' because they don't matter for infection in current model)
	def move_humans(self):
		for h in self.humans_S:
			h.move(np.random.normal(size=2), self.coords)
		for h in self.humans_I:
			h.move(np.random.normal(size=2), self.coords)

	# spreading infection on each step
	# assumption: if there are multiple people in the same radius and one of them is infected
	# the other people can only be infected by that one person in that time step
	def infection_spread(self, inf_dist, inf_prob):
		indexes = []
		for i in range(len(self.humans_S)):
			for j in range(len(self.humans_I)):
				if (self.humans_S[i].distance(self.humans_I[j].location) < inf_dist):
					if (np.random.uniform(0,1) < inf_prob == True):
						indexes.append(i)

		for i in indexes:
			self.humans_S[i].state = 'I'
			self.humans_S[i].infected_time = 0
			self.humans_I.append(self.humans_S.pop(i))

	def humans_recover_or_die(self, inf_time):
		# Reference: https://www1.nyc.gov/assets/doh/downloads/pdf/imm/covid-19-daily-data-summary-deaths-05132020-1.pdf
		death_prob_by_age = {17: 0.0006, 44: 0.39, 64: 0.224, 74: 0.249, 120: 0.487}  # Death probabilties by age
        # for example 18-44 years old is 0.39

		recovered_indexes = []
		for i in range(len(self.humans_I)):
			self.humans_I[i].infected_time += 1
			if (self.humans_I[i].infected_time) == inf_time:# need to decide recovery or death by age

				if(self.humans_I[i].Age <= 17):
					if(np.random.uniform(0, 1) < death_prob_by_age[17]):
						self.humans_I.pop(i)		# infected person dies
					else:
						recovered_indexes.append(i) # infected person recovers

				elif(self.humans_I[i].Age <= 44):
					if (np.random.uniform(0, 1) < death_prob_by_age[44]):
						self.humans_I.pop(i)
					else:
						recovered_indexes.append(i)

				elif(self.humans_I[i].Age <= 64):
					if (np.random.uniform(0, 1) < death_prob_by_age[64]):
						self.humans_I.pop(i)
					else:
						recovered_indexes.append(i)

				elif(self.humans_I[i].Age <= 74):
					if (np.random.uniform(0, 1) < death_prob_by_age[74]):
						self.humans_I.pop(i)
					else:
						recovered_indexes.append(i)

				else:
					if (np.random.uniform(0, 1) < death_prob_by_age[120]):
						self.humans_I.pop(i)
					else:
						recovered_indexes.append(i)

		for i in recovered_indexes:
			self.humans_I[i].state = 'R'
			self.humans_I[i].infected_time = -1
			self.humans_R.append(self.humans_I.pop(i))

# Creates the world
def build_world(args):

	# Get all the humans
	People = humans.create_humans(args)
	Communities = []

	comm_count = args.community_count
	comm_types = args.community_types
	length = args.community_box_length
	travel = args.community_travel
	spd = args.steps_per_day

	# All communities have equal number of people
	if comm_types == 'uniform':
		comm_density = int(len(People)/comm_count)

		for i in range(int(len(People)/comm_density)):
			coords = np.array([[i*length, i*length], [(i+1)*length, (i+1)*length]])
			Communities.append(Community(People[i*comm_density : (i+1)*comm_density], length, coords, spd))
		return World(Communities, travel)
	elif comm_types == 'real':
		# A simple way to generate communities
		people_copy = np.array(People)  # create a copy of people list
		for i in range(comm_count - 1):
			coords = np.array([[i * length, i * length], [(i + 1) * length, (i + 1) * length]])

			min_people = int(0.25 * people_copy.shape[0])  # min number of people in a community
			max_people = int(0.75 * people_copy.shape[0])  # max number of people to put in a community
			num_people = np.random.randint(min_people, max_people)
			people_indices = np.random.randint(0, people_copy.shape[0], num_people)
			sub_comm = [people_copy[i] for i in people_indices]
			Communities.append(Community(sub_comm, length, coords, spd))
			people_copy = np.delete(people_copy, people_indices)

		# Fill in the last community
		coords = np.array([[(comm_count-1)*length, (comm_count-1)*length], [comm_count*length, comm_count*length]])
		Communities.append(Community(people_copy.tolist(), length, coords, spd))

		rd.shuffle(Communities)
		return World(Communities, travel)