import humans
import random as rd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
import matplotlib.patches as patches

# To plot the humans
# TODO: expand for multiple communities
fig = plt.figure(figsize=(10,10))
ax = plt.axes()
ims=[]

# class for the whole world
class World():
	def __init__(self, communities, travel, quarantine, q_bool, file):
		self.communities = communities
		self.travel = travel
		self.quarantine = quarantine
		self.q_bool = q_bool
		self.humans_notified = 0
		self.file = file

	def __str__(self):
		out = "Communities : ["
		for c in self.communities:
			out += str(c)
		out += "]\n"
		out += "Quarantine : ["
		for c in self.quarantine:
			out += str(c)
		out += "]\n"
		out += "Travel Probability : " + str(self.travel)
		return out

	# Goes through one day for each community
	def update_world(self, inf_dist, inf_prob, inf_time, incub_time, sympt_prob):
		coords = []
		status = []
		ct_uploads = []
		for c in self.communities:
			co, s, contact_tracing_upload = c.one_day(inf_dist, inf_prob, inf_time, incub_time, sympt_prob)

			# If there are contact tracing updates then only add to the list
			if contact_tracing_upload != []:
				ct_uploads.append(contact_tracing_upload)

			if coords == []:
				coords = co
				status = s
			else:
				if co.shape[0] != 0:
					coords = np.append(coords, co, axis = 1)
					status = np.append(status, s, axis = 1)

			quarantine_indices = []
			for index in range(len(c.humans_I)):
				if c.humans_I[index].state == 'SYM':
					quarantine_indices.append(index)

			if self.q_bool:
				for i in sorted(quarantine_indices, reverse=True):
					self.quarantine.humans_I.append(c.humans_I.pop(i))  #Adding symptomatic patients to quarantine community
					self.quarantine.set_human('I', len(self.quarantine.humans_I)-1)

		# inter community travel
		self.community_travel()

		# Contact tracing notification
		self.notify_contact_tracing(ct_uploads)

		# Plot the quarantine community
		# Only move them once per day
		self.quarantine.move_humans()
		co, s = self.quarantine.positions()
		if (co != []):
			co = np.expand_dims(co, axis=0)
			s = np.expand_dims(s, axis=0)
			q_co = np.copy(co)
			q_s = np.copy(s)
			for i in range(1, coords.shape[0]):
				q_co = np.append(q_co, co, axis = 0)
				q_s = np.append(q_s, s, axis = 0)

			coords = np.append(coords, q_co, axis=1)
			status = np.append(status, q_s, axis=1)

		for i in range(coords.shape[0]):
			im=[ax.scatter(coords[i,:,0] ,coords[i,:,1] ,c=status[i,:], marker='o', linewidths=0)]
			ims.append(im)


	# This function moves humans who have come in contact with infected humans into quarantine
	def notify_contact_tracing(self, ct_uploads):
		# Since humans can move between communities this code becomes unoptimal
		# Part 1, get all human IDs that have to be notified
		notify_humans = set()
		# ct_uploads is list of communities, list of uploads per community, list of size incub_time
		# followed by a set of people in contact
		for ct in ct_uploads:
			for report in ct:
				for day in report:
					notify_humans.update(day)
		if len(notify_humans) == 0:
			return

		self.humans_notified += len(notify_humans)
		print('%d humans were notified.' % len(notify_humans))
		# Now we know all human ids to update we remove them from there communities
		# Right now this code adds them to our quarantine community. It should be okay because we
		# do not call the infection spread function on our quarantine community. This can be changed
		# if required
		for c in self.communities:
			# Iterate over the different human lists
			move_humans_idx = []
			for i in range(len(c.humans_S)):
				if c.humans_S[i].h_id in notify_humans:
					move_humans_idx.append(i)

			for idx in sorted(move_humans_idx, reverse=True):
				# quarantine human
				self.quarantine.humans_S.append(c.humans_S.pop(idx))
				self.quarantine.set_human('S', len(self.quarantine.humans_S)-1)


			move_humans_idx = []
			for i in range(len(c.humans_I)):
				if c.humans_I[i].h_id in notify_humans:
					move_humans_idx.append(i)

			for idx in sorted(move_humans_idx, reverse=True):
				# quarantine human
				self.quarantine.humans_I.append(c.humans_I.pop(idx))
				self.quarantine.set_human('I', len(self.quarantine.humans_I)-1)


			# Not necessary to do but why not
			move_humans_idx = []
			for i in range(len(c.humans_R)):
				if c.humans_R[i].h_id in notify_humans:
					move_humans_idx.append(i)

			for idx in sorted(move_humans_idx, reverse=True):
				# quarantine human
				self.quarantine.humans_R.append(c.humans_R.pop(i))
				self.quarantine.set_human('R', len(self.quarantine.humans_R)-1)



	# Start the world, intialize human locations and infect some humans
	def start(self, inf_init, comm_seed):

		# Intialize Human locations
		for c in self.communities:
			c.initialize_human_locations()

		# Excluding the quarantine community to start the infection
		comm_idx = np.random.randint(low=0, high=len(self.communities), size=comm_seed)
		for c in comm_idx:
			self.communities[c].infect(int(inf_init/len(comm_idx)))

	# Returns how many humans in which state
	def stats(self):
		SIRs = []
		for c in self.communities:
			SIRs.append(c.stats())
		return SIRs, self.quarantine.stats()

	# Outputs the humans graph
	def print_graph(self):
		Writer = animation.writers['ffmpeg']
		writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)

		print("Total Humans notified : %d" % self.humans_notified)
		for c in self.communities:
			rect = patches.Rectangle(c.coords[0],c.length,c.length,linewidth=2,edgecolor='black',facecolor='none')
			ax.add_patch(rect)
		rect = patches.Rectangle(self.quarantine.coords[0],self.quarantine.length,self.quarantine.length,linewidth=2,edgecolor='red',facecolor='none')
		ax.add_patch(rect)

		S_human = patches.Patch(color='blue', label='Susceptible')
		I_human = patches.Patch(color='green', label='Infected')
		SYM_human = patches.Patch(color='cyan', label='Symptomatic')
		ASYM_human = patches.Patch(color='pink', label='Asymptomatic')
		R_human = patches.Patch(color='red', label='Recovered')
		ani = animation.ArtistAnimation(fig, ims, interval=20, repeat_delay=1000)
		ax.legend(handles=[S_human, I_human, SYM_human, ASYM_human, R_human], loc='upper right')
		ani.save(self.file + '/simulation.mp4', writer=writer)

	# Moving a person from one community to the other
	def community_travel(self):
		# Will travel happen
		if np.random.uniform(0, 1) < self.travel:
			# Source, Destination
			comm_idx = np.random.randint(low=0, high=len(self.communities), size=2)
			
			status = ''
			if len(self.communities[comm_idx[0]].humans_I) == 0 and \
					len(self.communities[comm_idx[0]].humans_S) > 0: # only S persons
				status = 'S'
			elif len(self.communities[comm_idx[0]].humans_I) > 0 and \
					len(self.communities[comm_idx[0]].humans_S) == 0: # only I persons
				status = 'I'
			elif len(self.communities[comm_idx[0]].humans_I) == 0 and \
					len(self.communities[comm_idx[0]].humans_S) == 0: # no viable person to transfer
				return
			else: # Could be either S or I
				if np.random.uniform(0, 1) < 0.5: # choose between an S or I person
					status = 'S'
				else:
					status = 'I'

			if status == 'S':
				# choose a person
				h_idx = np.random.randint(low=0, high=len(self.communities[comm_idx[0]].humans_S))
				# transfer the person
				self.communities[comm_idx[1]].humans_S.append(self.communities[comm_idx[0]].humans_S.pop(h_idx))  
				self.communities[comm_idx[1]].set_human('S', len(self.communities[comm_idx[1]].humans_S)-1)
			elif status == 'I':
				# choose a person
				h_idx = np.random.randint(low=0, high=len(self.communities[comm_idx[0]].humans_I))
				# transfer the person
				self.communities[comm_idx[1]].humans_I.append(self.communities[comm_idx[0]].humans_I.pop(h_idx))  
				self.communities[comm_idx[1]].set_human('I', len(self.communities[comm_idx[1]].humans_I)-1)

# class for one community
class Community():
	def __init__(self, humans, length, coords, steps_per_day):
		self.humans_S = humans			# susceptible people
		self.humans_I = []			# infected people - can have 3 states: I, SYM, or ASYM
		self.humans_R = []			# recovered people
		self.humans_D = []			# dead patients
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

	# randomly assign human locations in a box
	def initialize_human_locations(self):
		random_coords = np.random.rand(len(self.humans_S), 2)*self.length + self.coords[0]
		for i in range(len(self.humans_S)):
			self.humans_S[i].set_location(random_coords[i])

	# return the number of humans in each state
	def stats(self):
		return [len(self.humans_S), len(self.humans_I), len(self.humans_R), len(self.humans_D)]




	# start the infection in the community
	def infect(self, inf_init):
		
		# Spreading infection in communities except quarantine community
		if(len(self.humans_S) > 0):
			h_idx = np.random.randint(low=0, high=len(self.humans_S), size=inf_init)

			for i in h_idx:
				self.humans_S[i].state = 'I'
				self.humans_S[i].infected_time = 0

			for h in self.humans_S:
				if h.state == 'I':
					self.humans_I.append(h)
					self.humans_S.remove(h)

	# goes through one day of the community
	def one_day(self, inf_dist, inf_prob, inf_time, incub_time, sympt_prob):
		coords = []
		status = []
		# humans take multiple steps per day
		for _ in range(self.steps_per_day):
			self.move_humans()
			self.infection_spread(inf_dist, inf_prob)
			c,s = self.positions()
			coords.append(c)
			status.append(s)
		# one day passes for humans (update status)
		contact_tracing_upload = self.humans_progress(inf_time, incub_time, sympt_prob)

		if (len(coords) != self.steps_per_day):
			print(coords)
		coords = np.array(coords)
		status = np.array(status)
		return coords,status, contact_tracing_upload

	# for graphing of humans
	def positions(self):
		coords = []
		status = []

		for h in self.humans_S:
			coords.append(h.location)
			status.append('blue')

		for h in self.humans_I:
			coords.append(h.location)
			if h.state == 'SYM':
				status.append('cyan')
			elif h.state == 'ASYM':
				status.append('pink')
			else:
				status.append('green')

		for h in self.humans_R:
			coords.append(h.location)
			status.append('red')

		return coords, status

	# move humans randomly (don't move 'R' because they don't matter for infection in current model)
	def move_humans(self):
		for h in self.humans_S:
			h.move(np.random.normal(size=2), self.coords)
		for h in self.humans_I:
			h.move(np.random.normal(size=2), self.coords)

	def set_human(self, list_type, idx):
		if list_type == 'S':
			self.humans_S[idx].set_location([c + self.length/2 for c in self.coords[0]])
		elif list_type == 'I':
			self.humans_I[idx].set_location([c + self.length/2 for c in self.coords[0]])
		elif list_type == 'R':
			self.humans_R[idx].set_location([c + self.length/2 for c in self.coords[0]])

	# spreading infection on each step
	# assumption: if there are multiple people in the same radius and one of them is infected
	# the other people can only be infected by that one person in that time step
	def infection_spread(self, inf_dist, inf_prob):
		# print(inf_prob)
		indexes = []
		for i in range(len(self.humans_S)):
			for j in range(len(self.humans_I)):
				if (self.humans_S[i].distance(self.humans_I[j].location) < inf_dist):
					c = np.random.uniform(0,1)
					print(c, c < inf_prob)
					if (c < inf_prob):		# decide whether to infect a person or not
						indexes.append(i)

		for i in sorted(list(set(indexes)), reverse=True):
			self.humans_S[i].state = 'I'
			self.humans_S[i].infected_time = 0
			self.humans_I.append(self.humans_S.pop(i))


		# Add all humans that come in contact with other humans
		# Optimization (not added) - outer loop can be only infected humans since incubation period is required
		# for checking that the people have come in contact. The apps don't work in this way because
		# people don't know when they were infected till they start showing symptoms
		All_humans = self.humans_S + self.humans_I
		for i in range(len(All_humans)):
			# If app not installed, not tracked
			if All_humans[i].app_install == False:
				continue
			for j in range(i+1, len(All_humans)):
				# If app not installed, not tracked
				if All_humans[j].app_install == False:
					continue

				if (All_humans[i].distance(All_humans[j].location) < inf_dist):
					All_humans[i].add_contact(All_humans[j].h_id)
					All_humans[j].add_contact(All_humans[i].h_id)

	def humans_progress(self, inf_time, incub_time, sympt_prob):

		recovered_indexes = []
		# died_indexes = []
		# This is similar to the upload humans have to do for BlueTrace when they
		# become symptomatic
		contact_tracing_upload = []
		# Advance the infection for each human
		for i in range(len(self.humans_I)):
			self.humans_I[i].infected_time += 1

			# Decide symptomatic or asymptomatic
			if (self.humans_I[i].infected_time == incub_time):
				self.decide_symptoms(i, sympt_prob)

			# Decide death or recovery of a symptomatic or asymptomatic infected person
			if (self.humans_I[i].infected_time == inf_time):
				state = self.decide_death(i)
				
				if state == 'R':	# if patient survives death
					recovered_indexes.append((i,'R'))
				if state == 'D':
					recovered_indexes.append((i,'D'))

		for h in self.humans_I:
			# Started showing symptoms and app installed
			# Assumption - there is a quarantine and symptomatic infected humans
			# are in only the quarantine community
			if h.state == 'SYM' and h.app_install == True:
				contact_tracing_upload.append(h.upload_contacts())

		# update the contact tracing buffer for all humans
		# Optimization (not added, only works if optimization done in infection_spread) -
		# only update for humans_I
		All_humans = self.humans_S + self.humans_I
		for h in All_humans:
			h.update_contact_day()


		for i,s in sorted(recovered_indexes, reverse=True):
			self.humans_I[i].state = s
			self.humans_I[i].infected_time = -1
			if s == 'R':
				self.humans_R.append(self.humans_I.pop(i))
			else:
				self.humans_D.append(self.humans_I.pop(i))
				self.death_toll += 1

		# for i in sorted(died_indexes, reverse=True):
		# 	self.humans_I[i].state = 'D'
		# 	self.humans_D.append(self.humans_I.pop(i))
		# 	self.death_toll += 1

		# get all the contact tracing uploads for the day
		return contact_tracing_upload

      
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
				decision_state = 'D' # infected person dies
			else:
				decision_state = 'R'  # infected person recovers

		elif (self.humans_I[human_index].Age <= 44):
			if (np.random.uniform(0, 1) < death_prob_by_age[44]):
				decision_state = 'D' # infected person dies
			else:
				decision_state = 'R'  # infected person recovers

		elif (self.humans_I[human_index].Age <= 64):
			if (np.random.uniform(0, 1) < death_prob_by_age[64]):
				decision_state = 'D' # infected person dies
			else:
				decision_state = 'R'  # infected person recovers

		elif (self.humans_I[human_index].Age <= 74):
			if (np.random.uniform(0, 1) < death_prob_by_age[74]):
				decision_state = 'D' # infected person dies
			else:
				decision_state = 'R'  # infected person recovers

		else:
			if (np.random.uniform(0, 1) < death_prob_by_age[120]):
				decision_state = 'D' # infected person dies
			else:
				decision_state = 'R'  # infected person recovers

		return decision_state


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
	q_bool = args.quarantine
	file = args.output_path


	# Adding a quarantine community
	q_len = length/5
	Quarantine = Community(list(), q_len, [[-5-q_len,0],[-5,q_len]], 0)

	comm_no_length = int((comm_count+1)/2)
	comm_no_height = int(comm_count/2)

	# All communities have equal number of people
	if comm_types == 'uniform':
		comm_density = int(len(People)/comm_count)

		l = 0
		b = 0
		for i in range(comm_count):
			# 10 added for bounding box buffer
			coords = np.array([[l*(length+10), b*(length+10)], [(l+1)*length + l*10, (b+1)*length + b*10]])
			if l == comm_no_length-1:
				l = 0
				b = b+1
			else:
				l = l+1

			Communities.append(Community(People[i*comm_density : (i+1)*comm_density], length, coords, spd))
		return World(Communities, travel, Quarantine, q_bool, file)
	elif comm_types == 'real':
		# A simple way to generate communities
		people_copy = np.array(People)  # create a copy of people list
		l = 0
		b = 0
		for i in range(comm_count - 1):
			# 10 added for bounding box buffer
			coords = np.array([[l*(length+10), b*(length+10)], [(l+1)*length + l*10, (b+1)*length + b*10]])
			if l == comm_no_length-1:
				l = 0
				b = b+1
			else:
				l = l+1

			min_people = int(0.25 * people_copy.shape[0])  # min number of people in a community
			max_people = int(0.75 * people_copy.shape[0])  # max number of people to put in a community
			num_people = np.random.randint(min_people, max_people)
			people_indices = np.random.choice(people_copy.shape[0], size=num_people, replace=False)
			sub_comm = [people_copy[i] for i in people_indices]
			Communities.append(Community(sub_comm, length, coords, spd))
			people_copy = np.delete(people_copy, people_indices, axis = 0)

		# Fill in the last community
		# 10 added for bounding box buffer
		coords = np.array([[l*(length+10), b*(length+10)], [(l+1)*length + l*10, (b+1)*length + b*10]])
		Communities.append(Community(people_copy.tolist(), length, coords, spd))

		rd.shuffle(Communities)
		return World(Communities, travel, Quarantine, q_bool, file)
