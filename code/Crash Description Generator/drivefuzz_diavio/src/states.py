""" Global States """
from collections import defaultdict

class State:
    """
    A state object stores raw data and events captured from the simulator,
    including vehicular states.
    Pass a reference to this object to TestScenario.run_test() as a parameter.
    """
    def __init__(self):
        self.ego_id = 0

        # exec states
        self.loop = 0
        self.mutation = 0
        self.first_frame_id = 0
        self.first_sim_elapsed_time = 0
        self.sim_start_time = 0
        self.num_frames = 0
        self.elapsed_time = 0

        # failure states
        self.spawn_failed = False
        self.spawn_failed_object = None

        # error states
        self.crashed = False
        self.collision_event = None
        self.stuck = False
        self.stuck_duration = 0
        self.laneinvaded = False
        self.laneinvasion_event = []
        self.speeding = False
        self.angular_velocity = list()
        self.transforms = []
        self.speed = []
        self.speed_lim = [] 
        self.on_red = False
        self.on_red_speed = []
        self.red_violation = False
        self.red_violation_record = []

        self.weather = {}

        # other error states, e.g., segfault
        self.other_error = False
        self.other_error_val = 0
        self.signal = 0

        # control states
        self.cont_throttle = []
        self.cont_brake = []
        self.cont_steer = []

        self.steer_angle_list = []
        self.yaw_list = []
        self.yaw_rate_list = []
        self.lat_speed_list = []
        self.lon_speed_list = []

        self.min_dist = 99999

        # score
        self.deductions = {}

        # debug info
        self.autoware_cmd = ""
        self.autoware_goal = ""

        self.npc_id = list()
        self.npc_state = defaultdict(lambda: State())

    def sig_handler(self, signum, frame):
        print("[-] something happened: {}".format(signal.signum.name))
        self.other = True
        self.signal = signum
    
    def set_npc_state(self, id, speed, transform, angular_velocity, speed_lim=50):
        self.npc_state[id].speed.append(speed)
        self.npc_state[id].transforms.append(transform)
        self.npc_state[id].speed_lim.append(speed_lim)
        self.npc_state[id].angular_velocity.append(angular_velocity)

    def get_npc_state(self, id):
        return self.npc_state[id]
    
    def get_state_by_id(self, id):
        if id == self.ego_id:
            return self
        else:
            return self.get_npc_state(id)

