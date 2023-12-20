from DSL.utils import *
from DSL.AccidentReport import AccidentReport
from DSL.RoadParser import RoadNetWork
from DSL.EnvironmentParser import Environment
from DSL.VehicleAnalyzer import VehicleReport
from DSL.ObjectiveBehavior import ObjectiveBehavior
from DSL.MyJsonEncoder import MyJsonEncoder
from DSL.VehicleDict import VehicleDict
from DSL.ViolationDetector import Violation
from DSL.ObstacleParser import Obstacles

from states import State

import config

import json
import datetime
import os
import numpy as np



_report:AccidentReport = AccidentReport() 
_state:State = State()
_client = None
_isHit = False

_cid_list = list() # collision id 

report_base_dir = r'reports'

def init_global(state, client):
    global _report
    _report = AccidentReport()
    global _state
    _state = state
    global _client
    _client = client
    global _isHit
    _isHit = False
    global _cid_list
    _cid_list = list()
    global _vehicleDict
    _vehicleDict = VehicleDict()
    _vehicleDict.set_uid_dict(_state.ego_id, _state.npc_id)

def set_isHit(is_Hit:bool):
    global _isHit
    _isHit = is_Hit

def add_collision(my_id, other_id):
    global _cid_list
    _cid_list = list()
    _cid_list.append(my_id)
    _cid_list.append(other_id)
    set_isHit(True)
    _report.set_report()

def dump_report():
    is_Hit = _isHit
    add_collision(_state.ego_id, _state.npc_id[0])
    violation = Violation()
    is_violation = violation.check_violation()
    if is_Hit == False and is_violation == False:
        return
    reportname = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    middle_path = os.path.join(report_base_dir, reportname)
    os.mkdir(middle_path)
    report_path = os.path.join(middle_path, 'report.json')
    identity_path = os.path.join(middle_path, 'identity.json')
    violation_path = os.path.join(middle_path, 'violation.json')
    f1 = open(identity_path, 'w')
    json.dump(_vehicleDict.get_uid_dict(), f1, indent=2)
    f1.close()
    if is_Hit:
        f = open(report_path, 'w')
        json.dump(_report.__dict__, f, cls=MyJsonEncoder, indent=2)
        f.close()
    if True: #is_violation:
        f3 = open(violation_path, 'w')
        json.dump(violation.violation_dict, f3, indent=2)
        f3.close()
