import numpy as np
import DSL as sd
import lgsvl
from DSL.RuleChecker import AgainstRules

class ObjectiveBehavior(object):
    def __init__(self) -> None:
        self.WhetherToBrake = "unmentioned"
        self.Direction = ""
        self.VehicleAction = "unmentioned"
        self.TravelSpeed = "between 2-17 kmph"
        self.is_against_rules = "unmentioned"
        self.AttemptedAvoidanceManeuvers = "unmentioned"
        self.AttemptedLaneCrossing = "unmentioned"

    def set_all(self, agent, ImpactSide):
        self.TravelSpeed = sd._simHistory.get_speed_list(agent)[-1]
        self.WhetherToBrake = sd._simHistory.is_brake(agent)
            
        self.Direction = self.rotation2direction_txt(agent.state.transform.rotation.y)
        self.set_vehicle_action_and_avoidance(agent, ImpactSide)
        self.AttemptedLaneCrossing = self.lane_crossing(agent.state)
        self.set_is_against_rule(agent)
        
    
    def set_vehicle_action_and_avoidance(self, agent, ImpactSide):
        direct_action = ''
        speed_action = ''
        changing_line_action = ''
        # Firstly, check if there is a lane change. 
        # If it is, determine whether it is on the changing line or merging based on the relationship between the previous and current roads
        changing_dir = sd._simHistory.get_agent_changing_line_dir(agent)
        if changing_dir == 'left':
            changing_line_action = ',left lane change'
        elif changing_dir == 'right':
            changing_line_action = ',right lane change'
        else:
            pass
        angular_v = agent.state.angular_velocity.y
        if np.abs(angular_v) <= 0.5:
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
        speed_change = sd._simHistory.speed_change_action(agent)
        if speed_change == 0:
            speed_action = ',constant speed'
        elif speed_change < 0:
            speed_action = ',deceleration'
        elif speed_change > 0:
            speed_action = ',acceleration'
        if(sd._simHistory.get_speed_list(agent)[-1] < 0.1):
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
        
        

    def rotation2direction_txt(self, rotation):
        angle = 5
        if rotation < angle or rotation >= 360-angle:
            return 'east'
        elif rotation >= angle and rotation < 90-angle:
            return 'southeast'
        elif rotation >= 90-angle and rotation < 90+angle:
            return 'south'
        elif rotation >= 90+angle and rotation < 180-angle:
            return 'southwest'
        elif rotation >= 180-angle and rotation < 180+angle:
            return 'west'
        elif rotation >= 180+angle and rotation < 270-angle:
            return 'northwest'
        elif rotation >= 270-angle and rotation < 270+angle:
            return 'north'
        elif rotation >= 270+angle and rotation < 360-angle:
            return 'northeast'
        
    def lane_crossing(self,state):
        cross_limit = 0.4 
        lane,road = sd.get_lane_road_by_state(state)
        agent_x, agent_y = sd.LGSVL2MapPos(state.transform)
        agent_point = np.array([agent_x, agent_y])
        min_dis = 100
        if lane.left_boundary is not None:
            points = lane.left_boundary.curve.segment[0].line_segment.point
            for idx in range(len(points)-1):
                l1 = sd.lane_point_2_numpy(points[idx])
                l2 = sd.lane_point_2_numpy(points[idx+1])
                res = sd.point_to_line_distance(agent_point,l1,l2)
                if min_dis > res:
                    min_dis = res
        if lane.right_boundary is not None:
            points = lane.right_boundary.curve.segment[0].line_segment.point
            for idx in range(len(points)-1):
                l1 = sd.lane_point_2_numpy(points[idx])
                l2 = sd.lane_point_2_numpy(points[idx+1])
                res = sd.point_to_line_distance(agent_point,l1,l2)
                if min_dis > res:
                    min_dis = res
        if min_dis < cross_limit:
            return 'yes'
        else:
            return 'no'
        
    def set_is_against_rule(self, agent):
        againstRules = AgainstRules(agent.state)
        rules = againstRules.check()
        if len(rules) <= 0:
            self.is_against_rules = 'unmentioned'
        else:
            self.is_against_rules = ';'.join(rules)
        
