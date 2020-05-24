import numpy as np
from scipy.stats import truncnorm

def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd)

class Human():
	# TODO: add other parameters of a human like location
	def __init__(self, age, gender):
		self.Age = age
		self.Gender = gender
		self.location = np.array([0.0,0.0])
		self.state = 'S'    # modified SIR model: (S)usceptible, (I)nfected, (R)ecovered, (SYM)ptomatic, (ASYM)ptomatic
		self.infected_time = -1  # time steps since infected
		self.incubation_time = -1

	def __str__(self):
		return "(" + str(self.Age) + ", " + self.Gender + ") "
	# TODO: add other functions of humans like movement

	def set_location(self, coords):
		self.location = coords

	def distance(self, coord):
		return np.sqrt((self.location[0] - coord[0])**2 + (self.location[1] - coord[1])**2)

	def move(self, direction, bounding_coords): # check for Box containment
		new_loc = self.location + direction
		if (new_loc[0] < bounding_coords[0][0] or new_loc[0] > bounding_coords[1][0]):
			direction[0] = -direction[0]
		if (new_loc[1] < bounding_coords[0][1] or new_loc[1] > bounding_coords[1][1]):
			direction[1] = -direction[1]
		self.location = self.location + direction



def create_humans(args):
	total_pop = args.total_population
	gender_ratio = args.gender_ratio
	age_dist_func = args.age_dist
	max_age = args.max_age

	Ages = []
	if age_dist_func == 'normal':
		X = get_truncated_normal(mean=29.6, sd=15, low=0, upp=max_age)
		Ages = X.rvs(total_pop)
		Ages = np.around(Ages)
		Ages = Ages.astype(int)
	elif age_dist_func == 'uniform':
		Ages = np.random.randint(low=0, high=max_age, size=total_pop)
	else:
		print("Unknown age distribution function given.")

	Genders = np.random.uniform(size=total_pop) > gender_ratio

	Population = []
	for i in range(Ages.shape[0]):
		if Genders[i] == True:
			Population.append(Human(Ages[i],'Male'))
		else:
			Population.append(Human(Ages[i],'Female'))

	return Population
