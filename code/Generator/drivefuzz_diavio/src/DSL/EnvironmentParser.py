import DSL as sd

class Environment(object):
    def __init__(self) -> None:
        self.RoadCondition = "unmentioned" 
        self.Weather = "unmentioned"

    def set_weather(self):
        self.Weather = self.weather_dict_2_list(sd._state.weather)

    def weather_dict_2_list(self, weather_dict:dict):
        weather_list = list()
        for key,value in weather_dict.items():
            if value > 20:
                weather_list.append(key)
        if len(weather_list) < 1:
            weather_list.append()
        return weather_list