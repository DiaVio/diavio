import DSL as sd
import numpy as np

import config
config.set_carla_api_path()
try:
    import carla
except ModuleNotFoundError as e:
    print("[-] Carla module not found. Make sure you have built Carla.")
    proj_root = config.get_proj_root()
    print("    Try `cd {}/carla && make PythonAPI' if not.".format(proj_root))
    exit(-1)

class AgainstRules(object):
    def __init__(self, state) -> None:
        self.rules = []
        self.state = state
    
    def check(self, index=None):
        if index == None:
            index = len(self.state.transforms)-1
        self.check_illegal_lane_change(index)
        self.check_run_red_light(index)
        return self.rules
    
    def check_run_red_light(self, index):
        if index in self.state.red_violation_record:
            self.rules.append('run red light')
    

    def check_illegal_lane_change(self, index):
        crossing_direction, lane_marking = sd.check_changing_lane(self.state, index)
        if self.is_crossing_lane_illegal(lane_marking, crossing_direction):
            self.rules.append("cross line illegally")

    def is_crossing_lane_illegal(self, lane_marking, crossing_direction):
        if lane_marking is None:
            return False
        lane_marking_type = lane_marking.type
        allowed_combinations = {
            carla.LaneMarkingType.Broken: ['left', 'right'],
            carla.LaneMarkingType.Solid: [],
            carla.LaneMarkingType.SolidSolid: [],
            carla.LaneMarkingType.SolidBroken: ['right'],
            carla.LaneMarkingType.BrokenSolid: ['left'],
            carla.LaneMarkingType.Other: ['left', 'right'],
        }

        if lane_marking_type in allowed_combinations:
            return not(crossing_direction in allowed_combinations[lane_marking_type])
        else:
            return False