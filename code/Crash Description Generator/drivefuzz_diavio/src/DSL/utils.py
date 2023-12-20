import DSL as sd
import numpy as np
from states import State

import config
config.set_carla_api_path()
try:
    import carla
except ModuleNotFoundError as e:
    print("[-] Carla module not found. Make sure you have built Carla.")
    proj_root = config.get_proj_root()
    print("    Try `cd {}/carla && make PythonAPI' if not.".format(proj_root))
    exit(-1)

def get_waypoint_by_transform(transform):
    map = sd._client.get_world().get_map()
    waypoint = map.get_waypoint(transform.location)
    return waypoint

def get_map():
    return sd._client.get_world().get_map()

def get_last_n_transforms(state, num = 1):
    res = list()
    for i in range(1, num+1):
        res.append(state.transforms[-1 * i])
    return res

def get_other_state(id):
    for cid in sd._cid_list:
        if cid != id :
            return sd._state.get_state_by_id(cid)
        
def get_other_id(id):
    for cid in sd._cid_list:
        if cid != id :
            return cid


def points_distance(a,b=np.array([0, 0])):
    c = a - b
    return np.sqrt(c.dot(c))

def get_angle(x,y):
    a = np.array([x, y])
    b = np.array([1, 0])
    La=points_distance(a)
    Lb=points_distance(b)
    cos_angle=a.dot(b)/(La*Lb)
    angle=np.arccos(cos_angle)
    angle2=angle*180/np.pi
    if y < 0:
        angle2 = 360 - angle2
    return angle2

def check_changing_lane(state:State, index):
    history_length = 8 
    transforms = state.transforms
    if len(transforms) < 2:
        return 'no', None
    now_lane_id = get_waypoint_by_transform(transforms[index]).lane_id
    old_lane_id = now_lane_id
    old_index = index
    for i in range(index-1, np.max(index-history_length-1, -1), -4):
       temp_lane_id = get_waypoint_by_transform(transforms[i]).lane_id
       if temp_lane_id != now_lane_id:
           old_lane_id = temp_lane_id
           old_index = i
           break
    old_waypoint = get_waypoint_by_transform(transforms[old_index])
    left_waypoint = old_waypoint.get_left_lane()
    right_waypoint = old_waypoint.get_right_lane()
    if left_waypoint is not None and left_waypoint.lane_id == now_lane_id:
        return 'left', old_waypoint.left_lane_marking
    elif right_waypoint is not None and right_waypoint.lane_id == now_lane_id:
        return 'right', old_waypoint.right_lane_marking
    else:
        return 'no', None