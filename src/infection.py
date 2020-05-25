

class Infection():
	def __init__(self, world, inf_init, comm_seed, inf_rad, inf_prob, inf_incub, sym_prob, inf_time):
		self.world = world
		self.inf_init = inf_init
		self.comm_seed = comm_seed
		self.inf_rad = inf_rad
		self.inf_prob = inf_prob
		self.inf_incub = inf_incub
		self.sym_prob = sym_prob
		self.inf_time = inf_time

	# Initialize the infection with world (could add lag if required)
	def start_infection(self):
		self.world.start(self.inf_init, self.comm_seed)

	# Proceed with a daya
	def one_day(self):
		self.world.update_world(self.inf_rad, self.inf_prob, self.inf_time, self.inf_incub, self.sym_prob)
		stats = self.world.stats()

		return stats

	# Get the graph for humans
	def graph(self):
		self.world.print_graph()

# Add an infection to the world
def infect_world(args, world):
	
	inf_init = args.infection_initial
	comm_seed = args.infection_comm_seed
	inf_rad = args.infection_radius
	inf_prob = args.infection_prob
	inf_incub = args.infection_incub
	sym_prob = args.symptom_prob
	inf_time = args.infection_time

	sim_time = args.sim_time


	infection = Infection(world, inf_init, comm_seed, inf_rad, inf_prob, inf_incub, sym_prob, inf_time)

	print(infection.world.stats())
	infection.start_infection()

	for _ in range(sim_time):
		print(infection.one_day())

	infection.graph()