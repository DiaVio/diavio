import DSL as sd
import json
import lgsvl

#report = sd.AccidentReport()
#print(json.dumps(report.__dict__,cls=sd.MyJsonEncoder))

import numpy as np
x=np.array([-1,0])
y=np.array([1,0])
Lx=np.sqrt(x.dot(x))
Ly=np.sqrt(y.dot(y))
cos_angle=x.dot(y)/(Lx*Ly)
#print(cos_angle)
angle=np.arccos(cos_angle)
angle2=angle*180/np.pi
#print(angle2)
#x.dot(y) =  y=∑(ai*bi)
print(sd.get_angle(1,1) )
print(sd.point_to_line_distance(np.array([2,2]),np.array([0,0]),np.array([1,1])))
