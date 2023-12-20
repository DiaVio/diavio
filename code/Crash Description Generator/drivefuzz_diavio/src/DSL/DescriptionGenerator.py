import DSL as sd
import os
import json

def dump_report():
    is_Hit = sd._isHit
    violation = sd.Violation()
    is_violation = violation.check_violation()
    if is_Hit == False and is_violation == False:# No accidents or violations occurred
        return
    reportname = sd.datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    middle_path = os.path.join(sd.report_base_dir, reportname)
    os.mkdir(middle_path)
    report_path = os.path.join(middle_path, 'report.json')
    identity_path = os.path.join(middle_path, 'identity.json')
    violation_path = os.path.join(middle_path, 'violation.json')
    f1 = open(identity_path, 'w')
    json.dump(sd._vehicleDict.get_uid_dict(), f1, indent=2)
    f1.close()
    if is_Hit:
        f = open(report_path, 'w')
        json.dump(sd._report.__dict__, f, cls=sd.MyJsonEncoder, indent=2)
        f.close()
    if True: #is_violation:
        f3 = open(violation_path, 'w')
        json.dump(violation.violation_dict, f3, indent=2)
        f3.close()