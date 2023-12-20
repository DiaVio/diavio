import hdmap
from hdmap import MapParser
import DSL as sd

class RoadNetWork(object):
    def __init__(self):
        self.RoadType = "two-way"
        self.LaneType = "0-lane"
        self.RoadShape = "curved to the right"
        self.RoadSlope = "unmentioned"
        self.SpeedLimit = 80

    def set_all(self, lane, road):
        lj_dict = sd._ma.get_is_lane_in_junction()
        if lj_dict[lane.id.id] is not False:
            self.RoadType = 'in junction'
        self.LaneType = '{}-lane'.format(len(road.section[0].lane_id))
        self.SpeedLimit = lane.speed_limit
        self.RoadShape = self.RoadShape_int2str(lane.turn)

    def RoadShape_int2str(self, shape_index):
        match shape_index:
            case 1:
                return 'NO_TURN'
            case 2:
                return 'LEFT_TURN'
            case 3:
                return 'RIGHT_TURN'
            case _:
                return 'not mentioned'
