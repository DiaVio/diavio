import DSL as sd

class AccidentReport(object):
    def __init__(self):
        self.RoadNetWork = sd.RoadNetWork()
        self.Environment = sd.Environment()
        self.accidents = []
        self.Obstacles = sd.Obstacles()


    def set_report(self):
        self.set_roadNetwork()
        self.set_env()
        self.set_vehicles()
        self.set_Obstacles()

    
    def set_roadNetwork(self):
        self.RoadNetWork.set_all()

    def set_env(self):
        self.Environment.set_weather()
    
    def set_vehicles(self):
        vehicle1 = sd.VehicleReport()
        vehicle1.set_all(sd._cid_list[0])
        vehicle2 = sd.VehicleReport()
        vehicle2.set_all(sd._cid_list[1])
        self.accidents.append({sd._vehicleDict.name(sd._cid_list[0]):vehicle1,sd._vehicleDict.name(sd._cid_list[1]):vehicle2})

    def set_Obstacles(self):
        pass
