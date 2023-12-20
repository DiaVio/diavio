import numpy as np
import DSL as sd
from DSL.RuleChecker import AgainstRules

import config
config.set_carla_api_path()
try:
    import carla
except ModuleNotFoundError as e:
    print("[-] Carla module not found. Make sure you have built Carla.")
    proj_root = config.get_proj_root()
    print("    Try `cd {}/carla && make PythonAPI' if not.".format(proj_root))
    exit(-1)

class ObjectiveBehavior(object):
    def __init__(self) -> None:
        self.WhetherToBrake = "unmentioned"
        self.Direction = ""
        self.VehicleAction = "unmentioned"
        self.TravelSpeed = "unmentioned"
        self.is_against_rules = "unmentioned"
        self.AttemptedAvoidanceManeuvers = "unmentioned"
        self.AttemptedLaneCrossing = "unmentioned"
        self.id = None
        self.state = None

    def set_all(self, id, ImpactSide):
        self.id = id
        self.state = sd._state.get_state_by_id(id)
        self.TravelSpeed = self.state.speed[-1]
        self.set_WhetherToBrake()
        self.Direction = self.angle2directiontxt(self.state.transforms[-1].rotation.yaw)
        self.set_AttemptedLaneCrossing()
        self.set_VehicleAction_and_AttemptedAvoidanceManeuvers(ImpactSide)
        self.set_is_against_rule()

    def set_WhetherToBrake(self):
        speeds = self.state.speed
        if len(speeds) < 2:
            self.WhetherToBrake = 'no'
        elif speeds[-1] - speeds[-2] < -0.3:
            self.WhetherToBrake = 'yes'
        else:
            self.WhetherToBrake = 'no'

    def set_AttemptedLaneCrossing(self):
        res, _ = sd.check_changing_lane(self.state, len(self.state.transforms)-1)
        if res == 'no':
            self.AttemptedLaneCrossing = 'no'
        else:
            self.AttemptedLaneCrossing = 'change lane from {}'.format(res)

    def set_VehicleAction_and_AttemptedAvoidanceManeuvers(self, ImpactSide):
        direct_action = ''
        speed_action = ''
        changing_line_action = ''
        changing_dir = sd.check_changing_lane(self.state, len(self.state.transforms)-1)
        if changing_dir == 'left':
            changing_line_action = ',left lane change'
        elif changing_dir == 'right':
            changing_line_action = ',right lane change'
        else:
            pass
        angular_v = self.state.angular_velocity[-1].y
        if np.abs(angular_v) <= 0.05: 
            direct_action = 'go straight'
        elif angular_v < 0:
            direct_action = 'turn left'
            if changing_dir == 'left':
                direct_action += ' for changing lane'
            elif changing_dir == 'right':
                direct_action += ' for merging'
        elif angular_v > 0:
            direct_action = 'turn right'
            if changing_dir == 'right':
                direct_action += ' for changing lane'
            elif changing_dir == 'left':
                direct_action += ' for merging'
        if len(self.state.speed) < 2:
            speed_change = 0
        else:
            speed_change = self.state.speed[-1] - self.state.speed[-2]
        if speed_change == 0:
            speed_action = ',constant speed'
        elif speed_change < 0:
            speed_action = ',deceleration'
        elif speed_change > 0:
            speed_action = ',acceleration'
        if (len(self.state.speed) < 1 or self.state.speed[-1] < 0.1):
            self.VehicleAction = 'parking'
        else:
            self.VehicleAction = '{}{}{}'.format(direct_action, speed_action, changing_line_action)
        if 'rear' in ImpactSide:
            self.AttemptedAvoidanceManeuvers = 'unmentioned'
        else:
            avoidance = []
            for direction in ['left','right']:
                if direction in direct_action and direction not in ImpactSide:
                    avoidance.append(direct_action)
            if speed_change < 0:
                avoidance.append("decelerate")
            if len(avoidance) <= 0:
                self.AttemptedAvoidanceManeuvers = 'no'
            else:
                self.AttemptedAvoidanceManeuvers = '{} to avoid collision'.format(','.join(avoidance))

    def set_is_against_rule(self):
        againstRules = AgainstRules(self.state)
        rules = againstRules.check()
        if len(rules) <= 0:
            self.is_against_rules = 'unmentioned'
        else:
            self.is_against_rules = ';'.join(rules)

    def angle2directiontxt(self, rotation):
        angle = 10
        if rotation < 0:
            rotation += 360
        if rotation < angle or rotation >= 360-angle:
            return 'north'
        elif rotation >= angle and rotation < 90-angle:
            return 'northeast'
        elif rotation >= 90-angle and rotation < 90+angle:
            return 'east'
        elif rotation >= 90+angle and rotation < 180-angle:
            return 'southeast'
        elif rotation >= 180-angle and rotation < 180+angle:
            return 'south'
        elif rotation >= 180+angle and rotation < 270-angle:
            return 'southwest'
        elif rotation >= 270-angle and rotation < 270+angle:
            return 'west'
        elif rotation >= 270+angle and rotation < 360-angle:
            return 'northwest'

    def get_dict(self):
        res_dict = self.__dict__
        res_dict.pop('state',0)
        res_dict.pop('id',0)
        return res_dict
        
    
    