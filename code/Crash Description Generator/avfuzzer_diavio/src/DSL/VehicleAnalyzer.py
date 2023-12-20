from typing import Any
import DSL as sd
import numpy as np

class VehicleReport(object):
    def __init__(self) -> None:
        self.ImpactSide = "unmentioned"
        self.MovingOnWhichWay = "unmentioned"
        self.LocationAfterCrash = "unmentioned"
        self.ObjectiveBehavior = sd.ObjectiveBehavior()

    def set_all(self, agent, agent2):
        self.set_moving_way(agent)
        self.set_locationAfterCrash(agent)
        self.set_ImpactSide(agent,agent2)
        self.ObjectiveBehavior.set_all(agent, self.ImpactSide)

    def set_moving_way(self, agent):
        lane, road = sd.get_lane_road_by_state(agent.state)
        points = lane.central_curve.segment[0].line_segment.point
        start = points[0]
        end = points[-1]
        d_east = end.x - start.x
        d_north = end.y - start.y
        de_txt = 'west' if d_east < 0 else 'east'
        dn_txt = 'south' if d_north < 0 else 'north'
        if np.abs(d_north / d_east) > 10:
            self.MovingOnWhichWay = dn_txt
        elif np.abs(d_north / d_east) < 0.1:
            self.MovingOnWhichWay = de_txt
        else:
            self.MovingOnWhichWay = '{}{}'.format(dn_txt,de_txt)

    def set_locationAfterCrash(self,agent):
        lane, road = sd.get_lane_road_by_state(agent.state)
        self.LocationAfterCrash = lane.id.id

    def set_ImpactSide(self, agent, agent2):
        x1, y1 = sd.LGSVL2MapPos(agent.state.transform)
        x2, y2 = sd.LGSVL2MapPos(agent2.state.transform)
        x, y = x1 - x2, y1 - y2
        crash_angle = sd.get_angle(x, y)
        rotation = crash_angle - agent.state.transform.rotation.y
        name2 = sd._vehicleDict.name(agent2)
        self.ImpactSide = '{} side collided by {}'.format(self.rotation2ImpactSide(rotation), name2)
        
        
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
        
            