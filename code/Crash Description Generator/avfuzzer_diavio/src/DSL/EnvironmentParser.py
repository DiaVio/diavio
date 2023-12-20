import DSL as sd

class Environment(object):
    def __init__(self) -> None:
        self.RoadCondition = "unmentioned" # LGSVL not support
        self.Weather = "unmentioned"

    def set_weather(self):
        '''
        The returned array of sim.weather is a length of 5, with each bit representingrain, fog, wetness, cloudiness, damage
        '''
        weathers = sd._sim.weather
        result = list()
        for i in range(len(weathers)):
            if weathers[i] > 0:
                result.append(self.weather_index2str(i))
        if len(result) == 0:
            result.append('sunny')
        self.Weather = result

    def weather_index2str(self,index):
        match index:
            case 0:
                return 'rain'
            case 1:
                return 'fog'
            case 2:
                return 'wetness'
            case 3:
                return 'cloudiness'
            case 4:
                return 'damage'
            case _:
                return None

