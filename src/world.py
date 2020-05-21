import humans

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
	def __init__(self, humans, area):
		self.humans = humans
		self.area = area

	def __str__(self):
		out = "Humans : ["
		for h in self.humans:
			out += str(h)
		out += "]\n"
		out += "Community Area : " + str(self.area)
		return out
		


def build_world(args):

	People = humans.create_humans(args)
	Communities = []

	comm_count = args.community_count
	comm_types = args.community_types
	area = args.community_area
	travel = args.community_travel

	if comm_types == 'uniform':
		comm_density = int(len(People)/comm_count)

		for i in range(int(len(People)/comm_density)):
			Communities.append(Community(People[i*comm_density : (i+1)*comm_density], area))
		return World(Communities, travel)
	elif comm_types == 'real':
		# TODO
		print("Under construction")
		return World()