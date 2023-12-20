import DSL as sd
import random

class VehicleDict(object):
    def __init__(self) -> None:
        self.uid_dict = dict()

    def set_uid_dict(self, ego_id, npcList):
        agent_num = len(npcList)+1 
        ego_index = random.randint(1,agent_num)
        self.uid_dict[ego_id] = {'name':'Vehicle{}'.format(ego_index), 'identity': 'EGO'}
        npc_index = 1
        for npc_id in npcList:
            if npc_index == ego_index:
                npc_index += 1
            self.uid_dict[npc_id] = {'name':'Vehicle{}'.format(npc_index), 'identity': 'NPC'}
            npc_index += 1

    def name(self, uid):
        return self.uid_dict[uid]['name']
    
    def get_identity_by_uid(self, uid):
        return self.uid_dict[uid]['identity']

    def get_uid_dict(self):
        return self.uid_dict