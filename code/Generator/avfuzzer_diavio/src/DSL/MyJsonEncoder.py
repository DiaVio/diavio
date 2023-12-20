from typing import Any
import DSL as sd
import json
import lgsvl
from hdmap import MapParser

class MyJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o,sd.Environment):
            return o.__dict__
        if isinstance(o,sd.RoadNetWork):
            return o.__dict__
        if isinstance(o,sd.ObjectiveBehavior):
            return o.__dict__
        if isinstance(o,sd.VehicleReport):
            return o.__dict__
        if isinstance(o,lgsvl.ObjectState):
            return o.to_json()
        if isinstance(0,MapParser):
            return None
        if isinstance(o,sd.Obstacles):
            return o.get_dict()