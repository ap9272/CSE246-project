# CSE246-project

usage:** python3 src/main.py [-h] [--param_file PARAM_FILE] [--sim_time SIM_TIME]
               [--total_population TOTAL_POPULATION]
               [--gender_ratio GENDER_RATIO] [--age_dist {normal,uniform}]
               [--max_age MAX_AGE] [--community_count COMMUNITY_COUNT]
               [--community_types {uniform,real}]
               [--community_box_length COMMUNITY_BOX_LENGTH]
               [--community_travel COMMUNITY_TRAVEL]
               [--steps_per_day STEPS_PER_DAY]
               [--infection_initial INFECTION_INITIAL]
               [--infection_comm_seed INFECTION_COMM_SEED]
               [--infection_radius INFECTION_RADIUS]
               [--infection_prob INFECTION_PROB]
               [--infection_incub INFECTION_INCUB]
               [--symptom_prob SYMPTOM_PROB] [--infection_time INFECTION_TIME]
               [--quarantine] [--app_install_prob APP_INSTALL_PROB]
               output_path


## Parameters
**output_path :** (string,required) location where the output is stored.  
**param_file (file) :** (string) Currently not used.  
**sim_time (time) :** (integer, default=100) How long to run the simulation.  

### Population parameters
**total_population (pop) :** (integer, default=400) How many humans in the simulation.  
**gender_ratio (gr) :** (float, default=0.5) What percentage of the population is female.  
**age_dist (age) :** (string, default='normal') What is age distribution. Only takes 2 choices 'normal' and 'uniform'. 'normal' is based on truncated gaussian distribution with real world parameters. 'uniform' assumes a uniform age distribution.  
**max_age (max_age) :** (integer, default=100) What is the age of the oldest individuals.  
**
### Population distribution parameters
**community_count (coms) :** (integer, default=4) The number of communities in the simulation.  
**community_types (comtypes) :** (string, default='uniform') The process to distribute humans in the communities. Only takes 2 choices 'uniform' and 'real'. 'uniform' is a uniform distribution of humans. 'real' will have communities of varying density randomly. In both cases total number of humans in the world is given by the total_population parameter.  
**community_box_length (bl) :** (integer, default=100) The length of the square which we call a community. Used to limit density.  
**community_travel (travel) :** (float, default=1) The probability of a human travelling from one community to another in a day.  
**steps_per_day (spd) :** (integer, default=10) The number of steps (movements) humans do within their community within a day.  

### Infection spread parameters
**infection_initial (init) :** (integer, default=4) How many humans to infect at the beginning of the simulation.  
**infection_comm_seed (comseed) :** (integer, default=1) How many communities to infect at the beginning. (Note, if infection_initial < infection_comm_seed then no human will be infected)  
**infection_radius (irad) :** (float, default=1) The distance 2 humans need to havefor them to be able to get infected.  
**infection_prob (iprob) :** (float, default=1) The probability of getting infected if in infection_radius of infected individual.  
**infection_incub (incub) :** (integer, default=10) The number of days humans remain asymptomatic when infected.  
**symptom_prob (sprob) :** (float, default=0.8) The probability of showing symptoms after infection_incub days of getting infected.  
**infection_time (itime) :** (integer, default=30) The time after which the human reaches the recovered stage. They either get cured or they die.  

### Infection prevention parameters
**quarantine (q) :** Make use of a quarantine. Infected humans which start showing symptoms are added to the quarantine at the end of the day.  
**app_install_prob (install) :** (float, default=1) For contact tracing. The probability of a person having installed with the contact tracing application. Only humans that install the app can be tracked and they can only detect other humans that have installed the app.  