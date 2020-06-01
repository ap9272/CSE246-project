import matplotlib.pyplot as plt

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

	# Returns world stats after one day passed
	def one_day(self):
		self.world.update_world(self.inf_rad, self.inf_prob, self.inf_time, self.inf_incub, self.sym_prob)

		return self.world.stats()

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
	file = args.output_path

	sim_time = args.sim_time


	infection = Infection(world, inf_init, comm_seed, inf_rad, inf_prob, inf_incub, sym_prob, inf_time)

	print(infection.world.stats())
	infection.start_infection()

	S_in_world = []
	I_in_world = []
	R_in_world = []

	logs = ""
	# Get stats for each day of simulation
	for _ in range(sim_time):
		all_stats = infection.one_day()
		print(all_stats)
		logs += str(all_stats) + '\n'

		s_total = 0
		i_total = 0
		r_total = 0
		# Get total numbers for each status group
		for comm_stat in all_stats[0]:
			s_total += comm_stat[0]
			i_total += comm_stat[1]
			r_total += comm_stat[2]

		S_in_world.append(s_total)
		I_in_world.append(i_total)
		R_in_world.append(r_total)

	logs += "Total Humans notified : " + str(infection.world.humans_notified)
	open(file + '/logs', 'w').write(logs)
	# Show infection animation
	infection.graph()

	# Show SIR plot of the infection
	fig = plt.figure(figsize=(5, 5))
	x_title = "Days"
	plt.xlabel(x_title)
	y_title = "Count"
	plt.ylabel(y_title)
	plt.plot(range(sim_time), S_in_world, color='b', label='Susceptible')
	plt.plot(range(sim_time), I_in_world, color='r', label='Infected')
	plt.plot(range(sim_time), R_in_world, color='g', label='Recovered')
	plt.legend()
	plt.savefig(file + '/SIR-graph.png')