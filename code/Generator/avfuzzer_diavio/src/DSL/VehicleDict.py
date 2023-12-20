import DSL as sd
import random

class VehicleDict(object):
    def __init__(self) -> None:
        self.uid_dict = dict()

    def set_uid_dict(self, ego, npcList):
        agent_num = len(npcList)+1
        ego_index = random.randint(1,agent_num)
        self.uid_dict[ego.uid] = {'name':'Vehicle{}'.format(ego_index), 'identity': 'EGO'}
        npc_index = 1
        for npc in npcList:
            if npc_index == ego_index:
                npc_index += 1
            self.uid_dict[npc.uid] = {'name':'Vehicle{}'.format(npc_index), 'identity': 'NPC'}
            npc_index += 1

    def name(self, agent):
        return self.uid_dict[agent.uid]['name']
    
    def get_identity_by_uid(self, uid):
        return self.uid_dict[uid]['identity']

    def get_uid_dict(self):
        return self.uid_dict