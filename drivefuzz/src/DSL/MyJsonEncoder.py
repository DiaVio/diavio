from typing import Any
import DSL as sd
import json
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

class MyJsonEncoder(json.JSONEncoder):
    def default(self, o: Any) -> Any:
        if isinstance(o,sd.Environment):
            return o.__dict__
        if isinstance(o,sd.RoadNetWork):
            return o.__dict__
        if isinstance(o,sd.ObjectiveBehavior):
            return o.get_dict()
        if isinstance(o,sd.VehicleReport):
            return o.get_dict()
        if isinstance(o, carla.Client):
            return None
        if isinstance(o, State):
            return None
        if isinstance(o,sd.Obstacles):
            return o.get_dict()
    