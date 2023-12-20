from typing import Any
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

class VehicleReport(object):
    def __init__(self) -> None:
        self.ImpactSide = "unmentioned"
        self.MovingOnWhichWay = "unmentioned"
        self.LocationAfterCrash = "unmentioned"
        self.ObjectiveBehavior = sd.ObjectiveBehavior()
        self.id = None
        self.state = None

    def set_all(self,id):
        self.id = id
        self.state = sd._state.get_state_by_id(id)
        self.set_MovingOnWhichWay() 
        self.set_LocationAfterCrash()
        self.set_ImpactSide()
        self.ObjectiveBehavior.set_all(id, self.ImpactSide)

    def set_MovingOnWhichWay(self):
        client_map = sd.get_map()
        waypoint = sd.get_waypoint_by_transform(sd.get_last_n_transforms(self.state, num = 1)[0])
        direction_angle = waypoint.transform.rotation.yaw
        self.MovingOnWhichWay = self.angle2directiontxt(direction_angle)

    def set_LocationAfterCrash(self):
        waypoint = sd.get_waypoint_by_transform(sd.get_last_n_transforms(self.state, num = 1)[0])
        self.LocationAfterCrash = waypoint.lane_id

    def set_ImpactSide(self):
        my_pos = sd.get_last_n_transforms(self.state, 1)[0]
        other_pos = sd.get_last_n_transforms(sd.get_other_state(self.id),1)[0]
        my_loc = my_pos.location
        other_loc = other_pos.location
        my_yaw = my_pos.rotation.yaw
        x, y = my_loc.x - other_loc.x, my_loc.y - other_loc.y
        crash_angle = sd.get_angle(x, y)
        rotation = crash_angle - my_yaw
        self.ImpactSide = '{} side collided by {}'.format(self.rotation2ImpactSide(rotation), sd._vehicleDict.name(sd.get_other_id(self.id)))

    def rotation2ImpactSide(self, rotation):
        angle = 10 
        if rotation < 0:
            rotation += 360
        if rotation < angle or rotation >= 360-angle:
            return 'rear'
        elif rotation >= angle and rotation < 90-angle:
            return 'left rear'
        elif rotation >= 90-angle and rotation < 90+angle:
            return 'left'
        elif rotation >= 90+angle and rotation < 180-angle:
            return 'left front'
        elif rotation >= 180-angle and rotation < 180+angle:
            return 'front'
        elif rotation >= 180+angle and rotation < 270-angle:
            return 'right front'
        elif rotation >= 270-angle and rotation < 270+angle:
            return 'right'
        elif rotation >= 270+angle and rotation < 360-angle:
            return 'right rear'

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
