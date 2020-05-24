import argparse
from world import build_world
from infection import infect_world


parser = argparse.ArgumentParser()

parser.add_argument("output_path", help='location where the output is stored')
parser.add_argument("--param_file", "-file", type=str)

parser.add_argument("--sim_time", "-time", type=int, default=100)

parser.add_argument("--total_population", "-pop", type=int, default=100)
parser.add_argument("--gender_ratio", "-gr", type=float, default=0.5)
parser.add_argument("--age_dist", "-age", type=str, default='normal', choices=['normal', 'uniform'])
parser.add_argument("--max_age", "-max_age", type=int, default=100)


parser.add_argument("--community_count", "-coms", type=int, default=1)
parser.add_argument("--community_types", "-comtypes", type=str, default='uniform', choices=['uniform', 'real'])
parser.add_argument("--community_box_length", "-bl", type=int, default=100)
parser.add_argument("--community_travel", "-travel", type=float, default=0.1)
parser.add_argument("--steps_per_day", "-spd", type=int, default=10)


parser.add_argument("--infection_initial", "-init", type=int, default=1)
parser.add_argument("--infection_comm_seed", "-comseed", type=int, default=1)
parser.add_argument("--infection_radius", "-irad", type=float, default=1)
parser.add_argument("--infection_prob", "-iprob", type=float, default=1)
parser.add_argument("--infection_incub", "-incub", type=int, default=1)
parser.add_argument("--symptom_prob", "-sprob", type=float, default=0.8)
parser.add_argument("--infection_time", "-itime", type=int, default=20)




args = parser.parse_args()

world = build_world(args)
# print(world)
infect_world(args, world)
