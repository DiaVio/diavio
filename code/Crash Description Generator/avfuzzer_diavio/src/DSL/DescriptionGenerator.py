import DSL as sd
import datetime
import os
import json

def dump_report(is_Hit):
    violation = sd.Violation()
    is_violation = violation.check_violation()
    if is_Hit == False and is_violation == False: # No accidents or violations occurred
        return
    reportname = datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
    middle_path = os.path.join(sd.report_base_dir, reportname)
    os.mkdir(middle_path)
    report_path = os.path.join(middle_path, 'report.json')
    identity_path = os.path.join(middle_path, 'identity.json')
    history_path = os.path.join(middle_path, 'history.json')
    violation_path = os.path.join(middle_path, 'violation.json')
    f2 = open(history_path, 'w')
    json.dump(sd._simHistory.__dict__, f2, cls=sd.MyJsonEncoder, indent=2)
    f2.close()
    f1 = open(identity_path, 'w')
    json.dump(sd._vehicleDict.get_uid_dict(), f1, indent=2)
    f1.close()
    if is_Hit:
        f = open(report_path, 'w')
        json.dump(sd._report.__dict__, f, cls=sd.MyJsonEncoder, indent=2)
        f.close()
    if is_violation:
        f3 = open(violation_path, 'w')
        json.dump(violation.violation_dict, f3, indent=2)
        f3.close()