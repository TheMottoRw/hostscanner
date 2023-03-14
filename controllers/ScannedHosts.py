import datetime
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from sqlalchemy import and_, not_, join, between, select

from controllers.AlchemyEncoder import AlchemyEncoder
from models import db, Hosts as HostsModel, StatusChanges as StatusChangesModel, IpGroups as IpGroupsModel
import json
from controllers import Utils


def save(hostname, ip):
    hosts = []
    host = db.session.query(HostsModel).filter(and_(HostsModel.hostname == hostname),
                                               HostsModel.current_ip == ip).first()

    if host is None:
        print("Host does not exist")
        host_model = HostsModel(hostname=hostname, current_ip=ip)
        db.session.add(host_model)
        db.session.commit()
        hosts = host_model
    else:
        print(f"Host {hostname} with ip: {ip} exist,skip it still connected..!")
    return json.loads(json.dumps(hosts, cls=AlchemyEncoder))


def save_array(arr):
    hosts = []
    hostnames = []
    for host_obj in arr:
        for key in host_obj:
            hostname = key
            ip = host_obj[key]
            # put hostname in list to updates disconnected hosts
            hostnames.append(hostname)
            host = db.session.query(HostsModel).filter(HostsModel.hostname == hostname).first()

            if host is None:
                print("Host does not exist,register it for the first time")
                host_model = HostsModel(hostname=hostname, current_ip=ip)
                db.session.add(host_model)
                db.session.commit()
                hosts = host_model
                change_model = StatusChangesModel(host_id=host_model.id, status="Connected",
                                                  message=f"New host {hostname} connected with ip:{ip}")
                db.session.add(change_model)
                db.session.commit()
                print(f"Host {hostname} created successfully")

            else:  # check status if was disconnected,set to connected
                if host.current_ip == ip:
                    print(f"Ip didn't change  update only status for {hostname}")
                    if host.status == 'Disconnected':
                        host.status = 'Connected'
                        host.scan_date = datetime.datetime.now()
                        db.session.commit()
                        change_model = StatusChangesModel(host_id=host.id, status="Connected",
                                                          message=f"Host reconnected")
                        db.session.add(change_model)
                        db.session.commit()
                else:
                    previous_ip = host.current_ip
                    print(f"Ip for {hostname} changed to : {ip} from {host.current_ip}")
                    host.current_ip = ip
                    host.status = 'Connected'
                    host.scan_date = datetime.datetime.now()
                    db.session.commit()
                    change_model = StatusChangesModel(host_id=host.id, status="Connected",
                                                      message=f"Host reconnected but ip changed from {previous_ip} to {ip}")
                    db.session.add(change_model)
                    db.session.commit()
    # Update disconnected hosts
    disconnected_hosts = update_disconnected_hosts(hostnames)
    if len(disconnected_hosts) > 0:
        print("Disconnected devices",disconnected_hosts)
        # send email notification of disconnected hosts to admin
        print("Sending email notification of disconnected hosts to admin")
        # send_notification_email("Disconnected host from network", disconnected_hosts)
        discon_hosts_ip = [x['current_ip'] for x in disconnected_hosts]
        Utils.send_sms(os.getenv("SMS_TECH_RECEIVER"), "Disconnected host: " + ', '.join(discon_hosts_ip))
    return json.loads(json.dumps(disconnected_hosts, cls=AlchemyEncoder))


def update_disconnected_hosts(arr):
    print("Updating disconnected hosts")
    data = []
    hosts = db.session.query(HostsModel).filter(
        and_(HostsModel.status == 'Connected', not_(HostsModel.hostname.in_(arr))))
    print(hosts)
    for host in hosts:
        data.append(host)
        host.status = 'Disconnected'
        db.session.commit()
        change_model = StatusChangesModel(host_id=host.id, status='Disconnected',
                                          message='Device disconnected from network')
        db.session.add(change_model)
        db.session.commit()
    return json.loads(json.dumps(data, cls=AlchemyEncoder))


def load_hosts():
    data = []
    hosts = db.session.query(HostsModel).all()
    # j = join(HostsModel,IpGroupsModel,between(HostsModel.current_ip,IpGroupsModel.first_ip,IpGroupsModel.last_ip))
    # hosts = db.session.query(HostsModel,IpGroupsModel).join(between(HostsModel.current_ip,IpGroupsModel.first_ip,IpGroupsModel.last_ip))
    # hosts = select(HostsModel).select_from(j)
    for host in hosts:
        obj = None

        j = db.session.query(IpGroupsModel).filter(
            between(host.current_ip, IpGroupsModel.first_ip, IpGroupsModel.last_ip))
        if len(list(j)) > 0:
            obj = {"id": host.id, "current_ip": host.current_ip, "hostname": host.hostname, "status": host.status,
                   "scan_date": host.scan_date, "group": j[0].group_name}
        else:
            obj = {"id": host.id, "current_ip": host.current_ip, "hostname": host.hostname, "status": host.status,
                   "scan_date": host.scan_date, "group": "Unknown"}
        data.append(obj)
    # return json.loads(json.dumps(hosts, cls=AlchemyEncoder))
    return data


def recent_hosts():
    hosts = db.session.query(HostsModel).order_by(HostsModel.id.desc())[:5]
    print(hosts)
    return json.loads(json.dumps(hosts, cls=AlchemyEncoder))


def gateways():
    data = []
    hosts = db.session.query(HostsModel).filter(HostsModel.hostname == '_gateway')
    for obj in hosts:
        data.append(obj)
    return json.loads(json.dumps(data, cls=AlchemyEncoder))


def filter(host_id, status, startdate, enddate):
    data = []
    host_instance = db.session.query(HostsModel).filter(HostsModel.scan_date.between(startdate, enddate))
    if status != 'All':
        host_instance = host_instance.filter(HostsModel.status == status)

    if host_id is not None and host_id != 'All':
        host_instance = host_instance.filter(HostsModel.id == host_id)

    for obj in host_instance:
        data.append(obj)
    return json.loads(json.dumps(data, cls=AlchemyEncoder))


def send_notification_email(title, host_arr):
    if not Utils.is_in_work_time_range():
        print("Out of work time,Can't send email notification,time")
        return True
    try:
        sender = os.getenv("SENDER_EMAIL")
        receiver = os.getenv("ADMIN_EMAIL")
        admin_name = os.getenv("ADMIN_NAME")
        print(f"Sending email notification to {admin_name}:{receiver}")
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = receiver

        host_list = "<ol>"

        for host in host_arr:
            host_list += f"<li>{host['hostname']}: {host['current_ip']}</li>"

        host_list += "</ol>"
        # Create the body of the message (a plain-text and an HTML version).
        text = f"Hello {admin_name}!\nKindly find below list of host disconnected from network:" + host_list + "<font>\n to change your account password?\n\nBest Regards,\nHost scanner Admin\nIshimwe Fabienne"
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hello """ + admin_name + """!<br>
               Kindly find below list of host disconnected:""" + host_list + """ <br>For further causes information and troubleshoot access these hosts physically<br><br>
               Best Regards,<br><br>

               <b>Host scanner automation</b>
            </p>
          </body>
        </html>
        """

        # Record the MIME types of both parts - text/plain and text/html.
        part1 = MIMEText(text, 'plain')
        part2 = MIMEText(html, 'html')

        # Attach parts into message container.
        # According to RFC 2046, the last part of a multipart message, in this case
        # the HTML message, is best and preferred.
        msg.attach(part1)
        msg.attach(part2)
        # Send the message via local SMTP server.
        mail = smtplib.SMTP('smtp.gmail.com', 587)

        mail.ehlo()

        mail.starttls()

        mail.login(os.getenv("SENDER_EMAIL"), os.getenv("SENDER_PASSWORD"))
        mail.sendmail(sender, receiver, msg.as_string())
        mail.quit()
    except Exception as e:
        print(f"Email Error occurred {str(e)}")
        return False
    return True

