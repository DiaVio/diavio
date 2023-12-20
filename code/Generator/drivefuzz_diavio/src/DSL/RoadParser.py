import DSL as sd
import math

import config
config.set_carla_api_path()
try:
    import carla
except ModuleNotFoundError as e:
    print("[-] Carla module not found. Make sure you have built Carla.")
    proj_root = config.get_proj_root()
    print("    Try `cd {}/carla && make PythonAPI' if not.".format(proj_root))
    exit(-1)

class RoadNetWork(object):
    def __init__(self):
        self.RoadType = "0-way"
        self.LaneType = "0-lane"
        self.RoadShape = "curved to the right"
        self.RoadSlope = "unmentioned"
        self.SpeedLimit = "unmentioned"

    def set_all(self):
        waypoint = sd.get_waypoint_by_transform(sd.get_last_n_transforms(sd._state, num = 1)[0])
        if waypoint:
            # get lane_type
            lane_type = waypoint.lane_type
            if lane_type == carla.LaneType.Driving:
                self.RoadType = "One-way"
            elif lane_type == (carla.LaneType.Driving | carla.LaneType.Bidirectional):
                self.RoadType = "Two-way"
            else:
                self.RoadType = "umentioned"

            road_topology = sd.get_map().get_topology()
            total_lanes_on_road = 0
            road_id = waypoint.road_id
            for segment in road_topology:
                if segment[0].road_id == road_id:
                    total_lanes_on_road += len(segment)
            self.LaneType = '{}-lane'.format(total_lanes_on_road)
            self.SpeedLimit = sd._state.speed_lim[-1]
            self.get_road_shape(waypoint)
        else:
            self.RoadType = "umentioned"

    
    def get_road_shape(self, waypoint):
        road_id = waypoint.road_id
        waypoints_next = waypoint.next(100)
        waypoints_previous = waypoint.previous(100)
        waypoints_on_road = [wp for wp in waypoints_previous + waypoints_next if wp.road_id == road_id]
        road_shape = [waypoint.transform.location for waypoint in waypoints_on_road]
        turn_direction = None

        for i in range(len(road_shape) - 2):
            angle1 = self.calculate_angle(road_shape[i], road_shape[i + 1])
            angle2 = self.calculate_angle(road_shape[i + 1], road_shape[i + 2])
    
            angle_diff = angle2 - angle1
    
            if angle_diff < -30:
                turn_direction = "right"
                break
            elif angle_diff > 30:
                turn_direction = "left"
                break

        if turn_direction:
            self.RoadShape = f"curved to the {turn_direction}"
        else:
            self.RoadShape = "straight"
    

    def calculate_angle(self, point1, point2):
        dx = point2.x - point1.x
        dy = point2.y - point1.y
        angle = math.atan2(dy, dx)
        return math.degrees(angle)
        
