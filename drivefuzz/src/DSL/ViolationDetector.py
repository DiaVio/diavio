from DSL.RuleChecker import AgainstRules
import DSL as sd
import config
from collections import defaultdict

class Violation(object):
    def __init__(self) -> None:
        self.violation_dict = defaultdict(lambda: dict()) 

    def check_violation(self):
        if_violate = False
        id_list = sd._state.npc_id
        id_list.append(sd._state.ego_id)
        for id in id_list:
            state = sd._state.get_state_by_id(id)
            for i in range(0, len(state.transforms), 20):
                againstRules = AgainstRules(state)
                rules = againstRules.check(index= i)
                if len(rules) > 0:
                    self.violation_dict[sd._vehicleDict.name(id)][i] = ';'.join(rules)
                    if id == sd._state.ego_id:
                        if_violate = True
        return if_violate