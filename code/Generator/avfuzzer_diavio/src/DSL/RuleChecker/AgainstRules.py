import DSL as sd
import numpy as np

class AgainstRules(object):
    def __init__(self,state) -> None:
        self.rules = []
        self.state = state
        self.lane,self.road = sd.get_lane_road_by_state(state)
    
    def check(self, time=None):
        self.check_run_red_light(time=time)
        self.check_illegal_lane_change()
        return self.rules

    def check_run_red_light(self, time=None):
        if time is None:
            if sd._signalMap.check_run_red_light(self.lane.id.id) is True:
                self.rules.append('run red light')
        else:
            if sd._signalMap.check_run_red_light_by_time(self.lane.id.id, time) is True:
                self.rules.append('run red light')

    def check_illegal_lane_change(self):
        '''
        Except for the dashed white and yellow lines, no other lines can be crossed.
        '''
        cross_limit = 0.4
        lane,road = sd.get_lane_road_by_state(self.state)
        agent_x, agent_y = sd.LGSVL2MapPos(self.state.transform)
        agent_point = np.array([agent_x, agent_y])
        for boundary in [lane.left_boundary,lane.right_boundary]:
            if boundary is not None and boundary.boundary_type[0].types[0] in [0,3,4,5,6]:
                points = boundary.curve.segment[0].line_segment.point
                for idx in range(len(points)-1):
                    l1 = sd.lane_point_2_numpy(points[idx])
                    l2 = sd.lane_point_2_numpy(points[idx+1])
                    res = sd.point_to_line_distance(agent_point,l1,l2)
                    if res < cross_limit:
                        match boundary.boundary_type[0].types[0]:
                            case 3:
                                self.rules.append('cross solid yellow line')
                            case 4:
                                self.rules.append('cross solid white line')
                            case 5:
                                self.rules.append('cross double yellow line')

