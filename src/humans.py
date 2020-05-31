import numpy as np
from scipy.stats import truncnorm

# get values from a truncated normal distribution for age sampling
def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

# class for human
class Human():
	# TODO: add other parameters of a human like location
	def __init__(self, age, gender, human_hash, incub_time, app_install):
		self.Age = age
		self.Gender = gender
		self.location = np.array([0.0,0.0])
		self.state = 'S'  # SIRD model: (S)usceptible, {(I)nfected, (SYM)ptomatic, (ASYM)ptomatic} , (R)ecovered, (D)ead
		self.infected_time = -1  # time steps since infected
		self.incubation_time = -1

		self.app_install = app_install
		self.h_id = human_hash
		self.contacted_humans = [set()]
		self.contacted_buff = incub_time


	def __str__(self):
		return "(" + str(self.Age) + ", " + self.Gender + ") "
	# TODO: add other functions of humans like movement

	# set the humans location (also on graph)
	def set_location(self, coords):
		self.location = coords

	# distance from another human
	def distance(self, coord):
		return np.sqrt((self.location[0] - coord[0])**2 + (self.location[1] - coord[1])**2)

	# To find new location of a human (can be changed)
	def move(self, direction, bounding_coords):
		new_loc = self.location + direction
		# checking for boc containment
		if (new_loc[0] < bounding_coords[0][0] or new_loc[0] > bounding_coords[1][0]):
			direction[0] = -direction[0]
		if (new_loc[1] < bounding_coords[0][1] or new_loc[1] > bounding_coords[1][1]):
			direction[1] = -direction[1]

		self.location = self.location + direction

	def add_contact(self, h_idx):
		if self.app_install == False:
			return
		self.contacted_humans[-1].add(h_idx)

	def update_contact_day(self):
		if self.app_install == False:
			return
		self.contacted_humans.append(set())
		if len(self.contacted_humans) >= self.contacted_buff:
			self.contacted_humans.pop(0)

	def upload_contacts(self):
		return self.contacted_humans



def create_humans(args):
	total_pop = args.total_population
	gender_ratio = args.gender_ratio
	age_dist_func = args.age_dist
	max_age = args.max_age
	incub_time = args.infection_incub
	app_install = args.app_install_prob

	Ages = []
	# assumes normal distribution with values choden from the internet
	if age_dist_func == 'normal':
		X = get_truncated_normal(mean=29.6, sd=15, low=0, upp=max_age)
		Ages = X.rvs(total_pop)
		Ages = np.around(Ages)
		Ages = Ages.astype(int)
	# assumes equally distributed by age
	elif age_dist_func == 'uniform':
		Ages = np.random.randint(low=0, high=max_age, size=total_pop)
	else:
		print("Unknown age distribution function given.")

	# Get genders for the humans
	Genders = np.random.uniform(size=total_pop) > gender_ratio

	# Get the humans who install the app
	Apps = np.random.uniform(size=total_pop) < app_install

	Population = []
	for i in range(Ages.shape[0]):
		if Genders[i] == True:
			Population.append(Human(Ages[i],'Male', i, incub_time, Apps[i]))
		else:
			Population.append(Human(Ages[i],'Female', i, incub_time, Apps[i]))

	return Population
