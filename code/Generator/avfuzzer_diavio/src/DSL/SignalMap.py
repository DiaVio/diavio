import DSL as sd
import numpy as np
import hdmap
from hdmap import MapParser

class SignalMap(object):
    '''
    This class is used to determine whether the vehicle ran a red light when an accident occurred
    '''
    def __init__(self) -> None:
        pass
        self.signal_dict = dict() # key:id in hdmap，value:index in sim.controllables
        self.signal_rule_dict = dict() # key:id in hdmap，value: change rules of the signal

    def set_signal_dict(self):
        self.signal_dict = dict()
        signals_lg = sd._sim.get_controllables()
        signals_id = sd._ma.get_signals() 
        for signal_id in signals_id:
            min_dis = 10000
            min_arg = -1
            for i in range(len(signals_lg)):
                dis = self.get_distance(signals_lg[i], signal_id)
                if dis < min_dis:
                    min_dis = dis
                    min_arg = i
            self.signal_dict[signal_id] = min_arg
            policy = signals_lg[min_arg].default_control_policy
            self.signal_rule_dict[signal_id] = policy



    def get_distance(self, signal_lg,signal_id):
        x_lg,y_lg = sd.LGSVL2MapPos(signal_lg.transform)
        point_lg = np.array([x_lg, y_lg])
        points_hd = sd._ma.get_signal_by_id(signal_id).boundary.point
        x_hd, y_hd = 0,0
        for point in points_hd:
            x_hd += point.x
            y_hd += point.y
        x_hd /= len(points_hd)
        y_hd /= len(points_hd)
        point_hd = np.array([x_hd,y_hd])
        return sd.points_distance(point_lg,point_hd)
    
    def get_current_state(self, signal_id):
        '''
        return state of signal
        '''
        signals_lg = sd._sim.get_controllables()
        index = self.signal_dict[signal_id]
        return signals_lg[index].current_state
    
    def check_run_red_light(self, lane_id):
        '''
        return True or False,whether run a red light or not
        '''
        lj_dict = sd._ma.get_is_lane_in_junction()
        if lj_dict[lane_id] is False:
            return False
        signals_id = sd._ma.get_lane_controlled_by_signals(lane_id)
        for signal_id in signals_id:
            if self.get_current_state(signal_id) == 'red':
                return True
        return False
    
    def check_run_red_light_by_time(self, lane_id, time):
        '''
        check whether run a red light or not by time
        '''
        lj_dict = sd._ma.get_is_lane_in_junction()
        if lj_dict[lane_id] is False:
            return False
        signals_id = sd._ma.get_lane_controlled_by_signals(lane_id)
        for signal_id in signals_id:
            if self.get_state_by_time(signal_id, time) == 'red':
                return True
        return False


    def get_state_by_time(self, signal_id, time):
        policy = self.signal_rule_dict[signal_id]
        total_time = 0
        color_list = list()
        time_list = list()
        for item in policy:
            if item['action'] == 'state':
                color_list.append(item['value'])
            elif item['action'] == 'wait':
                time_list.append(int(item['value']))
                total_time += int(item['value'])
            else:
                pass
        time_remainder = time % total_time
        for index in range(len(time_list)):
            time_remainder -= time_list[index]
            if time_remainder < 0:
                return color_list[index]
        return color_list[0]



