from environs import Env
import lgsvl

env = Env()

########### set port
SIMULATOR_HOST = env.str("LGSVL__SIMULATOR_HOST", "127.0.0.1")
SIMULATOR_PORT = env.int("LGSVL__SIMULATOR_PORT", 8181)
BRIDGE_HOST = env.str("LGSVL__AUTOPILOT_0_HOST", "localhost")#192.168.93.135 10.177.21.62
BRIDGE_PORT = env.int("LGSVL__AUTOPILOT_0_PORT", 9090)

########### select map
#LGSVL__AUTOPILOT_HD_MAP = env.str("LGSVL__AUTOPILOT_HD_MAP", "san_francisco")
LGSVL__AUTOPILOT_HD_MAP = env.str("LGSVL__AUTOPILOT_HD_MAP", "borregas_ave")
LGSVL__AUTOPILOT_0_VEHICLE_CONFIG = env.str("LGSVL__AUTOPILOT_0_VEHICLE_CONFIG", 'Lincoln2017MKZ_LGSVL') 


########### select map and vehicle in lgsvl.Used in simulation.py/loadMap，simulation.py/initEV
map_name = env.str("LGSVL__MAP", lgsvl.wise.DefaultAssets.map_borregasave)
#map_name = env.str("LGSVL__MAP", lgsvl.wise.DefaultAssets.map_sanfrancisco)
vehicle_conf = env.str("LGSVL__VEHICLE_0", lgsvl.wise.DefaultAssets.ego_lincoln2017mkz_apollo5_modular)

########### path of base_map.bin
map_filename = 'data/maps/borregas_ave/base_map.bin'

########### destination and init position
destination = {
    'x':1640.6, 
    'z':-608.9
}
initEvPos = lgsvl.Vector(-50.3399963378906, -1.03600025177002, -9.03000640869141)
#initEvPos = lgsvl.Vector(100.3399963378906, -1.03600025177002, -100.03000640869141)
#initEvPos = lgsvl.Vector(1699, 88.38, -607.9)
#initEvPos = lgsvl.Vector(20,10,-40)
###########


# simulation time
totalSimTime = 15
# time slice length
timeSliceLength = 0.25
