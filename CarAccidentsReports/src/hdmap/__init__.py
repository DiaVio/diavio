from modules.map.proto.map_pb2 import Map
from hdmap.MapParser import MapParser
import lgsvl


def load_hd_map(filename: str):
    map = Map()
    f = open(filename, 'rb')
    map.ParseFromString(f.read())
    f.close()
    return map

def findLane(ma, x, y):
    min_dis = 1000
    result = None
    lanes_id = ma.get_lanes()
    for id in lanes_id:
        points = ma.get_lane_by_id(id).central_curve.segment[0].line_segment.point
        for point in points:
            dis = (point.x-x)**2 + (point.y-y)**2
            if dis < min_dis:
                min_dis = dis
                result = id
    return result

def findRoadByLane(ma,lane_id):
    roads_id = ma.get_roads()
    for rid in roads_id:
        templist = ma.get_road_by_id(rid).section[0].lane_id
        id_list = [x.id for x in templist]
        if lane_id in id_list:
            return rid
    return None

def LGSVL2MapPos(sim, transform):
    data = sim.map_to_gps(transform)
    return data.easting, data.northing
