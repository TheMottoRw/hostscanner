import os
import random

from sqlalchemy import and_

from controllers.AlchemyEncoder import AlchemyEncoder
from models import db, IpGroups as IpGroupsModel
import json
from dotenv import load_dotenv

load_dotenv()

def add_ipgroup(group_name, first_ip, last_ip):
    user_data = []
    ipgroups = db.session.query(IpGroupsModel).filter(and_(IpGroupsModel.group_name == group_name,IpGroupsModel.first_ip == first_ip)).first()
    print("User obj")
    print(ipgroups)
    if ipgroups is None:
        print("ipgroups does not exist")
        user_model = IpGroupsModel(group_name=group_name, last_ip=last_ip, first_ip=first_ip)
        db.session.add(user_model)
        db.session.commit()
        ipgroups = {"status": True, "message": "IP group created successfully", "data": user_model}
    else:
        print("Ip group exist")
        ipgroups = {"status": False, "message": "IP Group already exist"}
    return json.loads(json.dumps(ipgroups, cls=AlchemyEncoder))


def load_ipgroups():
    data = []
    ipgroups = db.session.query(IpGroupsModel).all()
    return json.loads(json.dumps(ipgroups, cls=AlchemyEncoder))


def remove_ipgroup(name):
    data = {}
    ipgroup = db.session.query(IpGroupsModel).filter(IpGroupsModel.group_name == name).first()

    if ipgroup is not None:
        print("IP Group does not exist")
        db.session.delete(ipgroup)
        db.session.commit()
        data = {"status": True, "message": "Ip Group deleted successfully"}
    else:
        print("Ip Group exist")
        data = {"status": False, "message": "Ip Group does not exist"}
    return json.loads(json.dumps(data, cls=AlchemyEncoder))

