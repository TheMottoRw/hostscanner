from sqlalchemy import select

from controllers.AlchemyEncoder import AlchemyEncoder
from models import db, Hosts as HostsModel, StatusChanges as StatusChangesModel
import json


def load_logs():
    data = []
    obj = {}
    logs_obj = db.session.query(StatusChangesModel).all()
    logs = json.loads(json.dumps(logs_obj, cls=AlchemyEncoder))
    for log in logs:
        print("Logs class to object")
        print(log)
        if log['host_id'] not in obj:
            host = db.session.query(HostsModel).filter(HostsModel.id == log['host_id']).first()
            print(f" {host} {log['host_id']}")
            if host is not None:
                print("Host is not")
                log['hostname'] = host.hostname
                data.append(log)
                obj[host.id] = host.hostname
        else:
            log['hostname'] = obj[log['host_id']]
            data.append(log)
    return json.loads(json.dumps(data, cls=AlchemyEncoder))

def recent_logs():
    data = []
    obj = {}
    logs_obj = db.session.query(StatusChangesModel).order_by(StatusChangesModel.id.desc())[:5]
    logs = json.loads(json.dumps(logs_obj, cls=AlchemyEncoder))
    for log in logs:
        print("Logs class to object")
        print(log)
        if log['host_id'] not in obj:
            host = db.session.query(HostsModel).filter(HostsModel.id == log['host_id']).first()
            print(f" {host} {log['host_id']}")
            if host is not None:
                print("Host is not")
                log['hostname'] = host.hostname
                data.append(log)
                obj[host.id] = host.hostname
        else:
            log['hostname'] = obj[log['host_id']]
            data.append(log)
    return json.loads(json.dumps(data, cls=AlchemyEncoder))



def filter(host_id, status, startdate, enddate):
    data = []
    obj = {}
    print(f"{host_id} = {status} = {startdate} = {enddate}")
    logs_instance = db.session.query(StatusChangesModel).filter(
        StatusChangesModel.last_scan_date.between(startdate, enddate))
    if status != 'All':
        logs_instance = logs_instance.filter(StatusChangesModel.status == status)

    if host_id is not None and host_id != 'All':
        logs_instance = logs_instance.filter(StatusChangesModel.host_id == host_id)
    for log in logs_instance:
        log.hostname = log.host.hostname
        print(f"Relationship hostname {log.host.hostname}")
        # if log.host_id not in obj:  # avoid re-loop in host obj while host id already exist
        #     host = db.session.query(HostsModel).filter(HostsModel.id == log.host_id).first()
        #     if host is not None:
        #         log.hostname = host.hostname
        #         print(f"Log hostname {log.hostname}")
        #         data.append(log)
        #         obj[host.id] = host.hostname
        #         print(f"Hostname after append {data[len(data) - 1].hostname}")
        # else:
        #     log.hostname = obj[log.host_id]
        #     print(f"Log with hostname {log.hostname}")
        data.append(log)
        #     print(f"Hostname after append {data[len(data)-1].hostname}")
    return json.loads(json.dumps(data, cls=AlchemyEncoder))
