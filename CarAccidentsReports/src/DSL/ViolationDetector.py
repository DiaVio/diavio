from DSL.RuleChecker import AgainstRules
import DSL as sd
import config
from collections import defaultdict

class Violation(object):
    def __init__(self) -> None:
        self.violation_dict = defaultdict(lambda: dict()) 

    def check_violation(self):
        if_violate = False
        simList = sd._simHistory.get_simList()
        for i in range(len(simList)):
            state_dict = simList[i]
            time = (i + 1) * config.timeSliceLength
            for uid,state in state_dict.items():
                againstRules = AgainstRules(state)
                rules = againstRules.check(time= time)
                if len(rules) > 0 and sd._vehicleDict.get_identity_by_uid(uid) == 'EGO':
                    if_violate = True
                    self.violation_dict[uid][i] = ';'.join(rules)
        return if_violate

