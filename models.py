import datetime

from config import db


class Users(db.Model):
    """ Admin management """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    user_type = db.Column(db.String(100))
    password = db.Column(db.String(255))
    is_otp_needed = db.Column(db.Boolean, default=False)
    otp = db.Column(db.Integer)
    created_at = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def __repr__(self):
        return f'<User {self.email}>'

    def __json__(self):
        return ['id', 'name','phone', 'email', 'user_type', 'created_at']


class Hosts(db.Model):
    """ Purposely for gateway and PC with hostname """
    id = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(100))
    current_ip = db.Column(db.String(40))
    status = db.Column(db.String(100), default="Connected")
    scan_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def __repr__(self):
        return f'<Hosts {self.current_ip}>'

    def __json__(self):
        return ['id', 'hostname', 'current_ip', 'status', 'scan_date']


class StatusChanges(db.Model):
    """ Track ip changes for each host with IP and hostname """
    id = db.Column(db.Integer, primary_key=True)
    host_id = db.Column(db.Integer(), db.ForeignKey(Hosts.id))
    status = db.Column(db.String(10))
    message = db.Column(db.String(100))
    last_scan_date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    host = db.relationship(Hosts)
    hostname = db.String()

    def __json__(self):
        return ['id', 'host_id', 'hostname', 'status', 'message', 'last_scan_date']


class IpGroups(db.Model):
    """ Shows ip group regarding to where they are being used """
    id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(100))
    first_ip = db.Column(db.String(100))
    last_ip = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=False), default=datetime.datetime.now())

    def __json__(self):
        return ['id', 'group_name', 'first_ip', 'last_ip', 'created_at']
