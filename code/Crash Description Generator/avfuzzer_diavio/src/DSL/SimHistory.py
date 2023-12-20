import lgsvl
import copy
import numpy as np
import DSL as sd
import config

class SimHistory(object):
    def __init__(self) -> None:
        self.timeSliceLength = config.timeSliceLength
        self.simList = list() # element is dict，uid->state
        self.lineList = None

    def add(self, ego, npcList):
        state_dict = dict()
        state_dict[ego.uid] = copy.deepcopy(ego.state)
        for npc in npcList:
            state_dict[npc.uid] = copy.deepcopy(npc.state)     
        self.simList.append(state_dict)

    def get_simList(self):
        return self.simList
    
    def get_speed_list(self, agent):
        uid = agent.uid
        speeds = np.array([item[uid].speed for item in self.simList])
        return speeds
    
    def speed_change_action(self, agent):
        speeds = self.get_speed_list(agent)
        if len(speeds)<2:
            return 0
        if np.abs(speeds[-1] - speeds[-2]) < 0.1: 
            return 0
        return speeds[-1] - speeds[-2]
    
    def is_brake(self, agent):
        return self.speed_change_action(agent) < -0.3
    
    def get_lane_list(self):
        if self.lineList is None:
            self.lineList = list()
            for state_dict in self.simList:
                line_dict = dict()
                for uid,state in state_dict.items():
                    lane, road = sd.get_lane_road_by_state(state)
                    line_dict[uid] = lane.id.id
                self.lineList.append(line_dict)
        return self.lineList
    
    def get_lane_list_by_agent(self,agent):
        all_list = self.get_lane_list()
        agent_list = [item[agent.uid] for item in all_list]
        return agent_list
    
    def get_agent_changing_line_dir(self,agent):
        history_num = 5
        lane_list = self.get_lane_list_by_agent(agent)
        if len(lane_list) < 2:
            return 'no'
        now_lane_id = lane_list[-1]
        old_lane_id = now_lane_id
        for i in range(len(lane_list)-2, np.max(len(lane_list)-6, -1), -1):
            if lane_list[i] != now_lane_id:
                old_lane_id =lane_list[i]
                break
        old_lane = sd._ma.get_lane_by_id(old_lane_id)
        if now_lane_id in [item.id for item in old_lane.left_neighbor_forward_lane_id]:
            return 'left'
        elif now_lane_id in [item.id for item in old_lane.right_neighbor_forward_lane_id]:
            return 'right'
        else:
            return 'no'




    