from DSL.AccidentReport import AccidentReport
from DSL.RoadParser import RoadNetWork
from DSL.EnvironmentParser import Environment
from DSL.VehicleAnalyzer import VehicleReport
from DSL.ObjectiveBehavior import ObjectiveBehavior
from DSL.MyJsonEncoder import MyJsonEncoder
from DSL.SignalMap import SignalMap
from DSL.VehicleDict import VehicleDict
from DSL.SimHistory import SimHistory
from DSL.ViolationDetector import Violation
from DSL.ObstacleParser import Obstacles

import config
import hdmap
from hdmap import MapParser

import json
import datetime
import os
import numpy as np

# globals
_sim = None
_ma = MapParser(config.map_filename)
_signalMap = SignalMap()
_report = AccidentReport()
_vehicleDict = VehicleDict()
_simHistory = SimHistory()

report_base_dir = r'reports'

def init_global(sim, ego, npcList):
    global _sim
    _sim = sim
    global _report
    _report = AccidentReport()
    _signalMap.set_signal_dict()
    global _vehicleDict
    _vehicleDict = VehicleDict()
    _vehicleDict.set_uid_dict(ego, npcList)
    _simHistory = SimHistory()

def add_collision(agent1, agent2):
    _report.set_report(agent1, agent2)

def dump_report(is_Hit):
    violation = Violation()
    is_violation = violation.check_violation()
    if is_Hit == False and is_violation == False: # no accident or violation
        return
    reportname = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    middle_path = os.path.join(report_base_dir, reportname)
    os.mkdir(middle_path)
    report_path = os.path.join(middle_path, 'report.json')
    identity_path = os.path.join(middle_path, 'identity.json')
    history_path = os.path.join(middle_path, 'history.json')
    violation_path = os.path.join(middle_path, 'violation.json')
    f2 = open(history_path, 'w')
    json.dump(_simHistory.__dict__, f2, cls=MyJsonEncoder, indent=2)
    f2.close()
    f1 = open(identity_path, 'w')
    json.dump(_vehicleDict.get_uid_dict(), f1, indent=2)
    f1.close()
    if is_Hit:
        f = open(report_path, 'w')
        json.dump(_report.__dict__, f, cls=MyJsonEncoder, indent=2)
        f.close()
    if is_violation:
        f3 = open(violation_path, 'w')
        json.dump(violation.violation_dict, f3, indent=2)
        f3.close()

def LGSVL2MapPos(transform):
    '''
    Coordinate system conversion
    '''
    x,y = hdmap.LGSVL2MapPos(_sim, transform)
    return x,y

def get_lane_road_by_state(state):
    '''
    Return to the current lane and road where the car is located
    '''
    x,y = hdmap.LGSVL2MapPos(_sim, state.transform)
    lane_id = hdmap.findLane(_ma, x, y)
    road_id = hdmap.findRoadByLane(_ma, lane_id)
    lane = _ma.get_lane_by_id(lane_id)
    road = _ma.get_road_by_id(road_id)
    return lane, road

def lane_point_2_numpy(point):
    '''
    Convert the points in lane to numpy array type
    '''
    return np.array([point.x, point.y])

def points_distance(a,b=np.array([0, 0])):
    c = a - b
    return np.sqrt(c.dot(c))

def get_angle(x,y):
    '''
    Given the x and y of a vector, find the rotation corresponding to the direction of this vector
    '''
    a = np.array([x, y])
    b = np.array([1, 0])
    La=points_distance(a)
    Lb=points_distance(b)
    cos_angle=a.dot(b)/(La*Lb)
    angle=np.arccos(cos_angle)
    angle2=angle*180/np.pi
    if y > 0:
        angle2 = 360 - angle2
    return angle2

def point_to_line_distance(p, l1, l2):
    line_length = points_distance(l1, l2)
    u1 = ( (p[0]-l1[0])*(l2[0]-l1[0]) + (p[1]-l1[1])*(l2[1]-l1[1]) )
    u = u1 / (line_length**2)
    if u <= 0 or u > 1: 
        return min( points_distance(p,l1), points_distance(p,l2) )
    else:
        pl = np.array(l1+u*(l2-l1))
        return points_distance(p,pl)

