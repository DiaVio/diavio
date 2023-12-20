import DSL as sd

class AccidentReport(object):
    def __init__(self):
        self.RoadNetWork = sd.RoadNetWork()
        self.Environment = sd.Environment()
        self.accidents = []
        self.Obstacles = sd.Obstacles()


    def set_report(self, agent1, agent2):
        lane, road = sd.get_lane_road_by_state(agent1.state)
        self.set_roadNetwork(lane, road)
        self.set_env()
        self.set_vehicles(agent1,agent2)
        self.set_Obstacles()

    
    def set_roadNetwork(self, lane, road):
        self.RoadNetWork.set_all(lane, road)

    def set_env(self):
        self.Environment.set_weather()
    
    def set_vehicles(self, agent1, agent2):
        vehicle1 = sd.VehicleReport()
        vehicle2 = sd.VehicleReport()
        vehicle1.set_all(agent1, agent2)
        vehicle2.set_all(agent2, agent1)
        name1 = sd._vehicleDict.name(agent1)
        name2 = sd._vehicleDict.name(agent2)
        self.accidents.append({name1:vehicle1, name2:vehicle2})

    def set_Obstacles(self):
        pass


