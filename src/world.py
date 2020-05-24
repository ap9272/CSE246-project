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

	def update_world(self, inf_dist, inf_prob, inf_time):
		for c in self.communities:
			c.one_day(inf_dist, inf_prob, inf_time)

	def start(self, inf_init, comm_seed):
		comm_idx = np.random.randint(low=0, high=len(self.communities), size=comm_seed)
		for c in comm_idx:
			self.communities[c].initialize_human_locations()
			self.communities[c].infect(int(inf_init/len(comm_idx)))

	def stats(self):
		SIRs = []
		for c in self.communities:
			SIRs.append(c.stats())
		return SIRs


class Community():
	def __init__(self, humans, length, coords, steps_per_day):
		self.humans_S = humans			# susceptible people
		self.humans_I = []				# infected people - can have 3 states: I, SYM, or ASYM
		self.humans_R = []				# recovered people
		self.humans_D = []				# dead patients
		self.length = length			# side length of the square representing community
		self.coords = coords			# coordinates of the square(community)
		self.steps_per_day = steps_per_day
		self.death_toll = 0

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
		out += "Died Humans : ["
		for h in self.humans_D:
			out += str(h)
		out += "]\n"
		out += "Community Box Length : " + str(self.length)
		return out

	def initialize_human_locations(self):
		random_coords = np.random.rand(len(self.humans_S), 2)*self.length + self.coords[0][0]
		for i in range(len(self.humans_S)):
			self.humans_S[i].set_location(random_coords[i])


	def stats(self):
		return [len(self.humans_S), len(self.humans_I), len(self.humans_R), len(self.humans_D)]


	def infect(self, inf_init):
		h_idx = np.random.randint(low=0, high=len(self.humans_S), size=inf_init)

		for i in h_idx:
			self.humans_S[i].state = 'I'
			self.humans_S[i].infected_time = 0
			self.humans_I.append(self.humans_S.pop(i))

	def one_day(self, inf_dist, inf_prob, inf_time, incub_time, sympt_prob):

		for _ in range(self.steps_per_day):
			self.move_humans()
			self.infection_spread(inf_dist, inf_prob)
		self.humans_progress(inf_time, incub_time, sympt_prob)


	def move_humans(self):
		for h in self.humans_S:
			h.move(np.random.uniform(size=2), self.coords)
		for h in self.humans_I:
			h.move(np.random.uniform(size=2), self.coords)

	def infection_spread(self, inf_dist, inf_prob):
		indexes = []
		for i in range(len(self.humans_S)):
			for j in range(len(self.humans_I)):
				if (self.humans_S[i].distance(self.humans_I[j].location) < inf_dist):
					if (np.random.uniform(0,1) < inf_prob == True):		# decide whether to infect a person or not
						indexes.append(i)

		for i in indexes:
			self.humans_S[i].state = 'I'
			self.humans_S[i].infected_time = 0
			self.humans_I.append(self.humans_S.pop(i))


	def humans_progress(self, inf_time, incub_time, sympt_prob):
		recovered_indexes = []
		died_indexes = []
		# Advance the infection for each human
		for i in range(len(self.humans_I)):
			self.humans_I[i].infected_time += 1

			# Decide symptomatic or asymptomatic
			if (self.humans_I[i].infected_time == incub_time):
				self.decide_symptoms(i, sympt_prob)

			# Decide death or recovery of a symptomatic or asymptomatic infected person
			if (self.humans_I[i].infected_time == inf_time):
				recover_indx = self.decide_death(i)
				if recover_indx != -1:	# if patient survives death
					recovered_indexes.append(recover_indx)

		for i in recovered_indexes:
			self.humans_I[i].state = 'R'
			self.humans_I[i].infected_time = -1
			self.humans_R.append(self.humans_I.pop(i))


	def decide_symptoms(self, human_index, sympt_prob):
		if np.random.uniform(0, 1) < sympt_prob: # patient is symptomatic
			self.humans_I[human_index].state = 'SYM'
		else:
			self.humans_I[human_index].state = 'ASYM'


	def decide_death(self, human_index):
		# Reference: https://www1.nyc.gov/assets/doh/downloads/pdf/imm/covid-19-daily-data-summary-deaths-05132020-1.pdf
		death_prob_by_age = {17: 0.0006, 44: 0.39, 64: 0.224, 74: 0.249, 120: 0.487}  # Death probabilties by age
		# for example 18-44 years old is 0.39
		if (self.humans_I[human_index].Age <= 17):
			if (np.random.uniform(0, 1) < death_prob_by_age[17]):
				self.humans_I[human_index].state = 'D'  # infected person dies
				self.humans_D.append(self.humans_I.pop(human_index))
				self.death_toll += 1
			else:
				return human_index  # infected person recovers

		elif (self.humans_I[human_index].Age <= 44):
			if (np.random.uniform(0, 1) < death_prob_by_age[44]):
				self.humans_I[human_index].state = 'D'  # infected person dies
				self.humans_D.append(self.humans_I.pop(human_index))
				self.death_toll += 1
			else:
				return human_index

		elif (self.humans_I[human_index].Age <= 64):
			if (np.random.uniform(0, 1) < death_prob_by_age[64]):
				self.humans_I[human_index].state = 'D'  # infected person dies
				self.humans_D.append(self.humans_I.pop(human_index))
				self.death_toll += 1
			else:
				return human_index

		elif (self.humans_I[human_index].Age <= 74):
			if (np.random.uniform(0, 1) < death_prob_by_age[74]):
				self.humans_I[human_index].state = 'D'  # infected person dies
				self.humans_D.append(self.humans_I.pop(human_index))
				self.death_toll += 1
			else:
				return human_index

		else:
			if (np.random.uniform(0, 1) < death_prob_by_age[120]):
				self.humans_I[human_index].state = 'D'  # infected person dies
				self.humans_D.append(self.humans_I.pop(human_index))
				self.death_toll += 1
			else:
				return human_index

		return -1


def build_world(args):

	People = humans.create_humans(args)
	Communities = []

	comm_count = args.community_count
	comm_types = args.community_types
	length = args.community_box_length
	travel = args.community_travel
	spd = args.steps_per_day

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