import os
import random

import bcrypt as bcrypt
from sqlalchemy import and_

from controllers.AlchemyEncoder import AlchemyEncoder
from models import db, Users as UserModel
import json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
from controllers import Utils

load_dotenv()


def admin_existence():
    user_data = []
    users = db.session.query(UserModel).filter(UserModel.email == "hasua.mr@gmail.com").first()
    print("User obj")
    print(users)
    if users is None:
        print("User does not exist")
        user_model = UserModel(email="hasua.mr@gmail.com", password="12345")
        db.session.add(user_model)
        db.session.commit()
        users = user_model
    else:
        print("User exist")
    return json.loads(json.dumps(users, cls=AlchemyEncoder))


def add_user(names, phone, email, user_type, password):
    user_data = []
    users = db.session.query(UserModel).filter(UserModel.email == email).first()
    pwd = bcrypt.hashpw(str(password).encode("UTF-8"), bcrypt.gensalt())
    print("User obj")
    print(users)
    if users is None:
        print("User does not exist")
        user_model = UserModel(name=names, user_type=user_type, phone=phone, email=email, password=pwd)
        db.session.add(user_model)
        db.session.commit()
        users = user_model
        users = {"status": True, "message": "User created successfully", "data": user_model}
    else:
        print("User exist")
        users = {"status": False, "message": "User already exist"}
    return json.loads(json.dumps(users, cls=AlchemyEncoder))


def remove_user(email):
    data = {}
    user = db.session.query(UserModel).filter(UserModel.email == email).first()

    if user is not None:
        print("User does not exist")
        db.session.delete(user)
        db.session.commit()
        data = {"status": True, "message": "User deleted successfully"}
    else:
        print("User exist")
        data = {"status": False, "message": "User does not exist"}
    return json.loads(json.dumps(data, cls=AlchemyEncoder))


def load_users():
    data = []
    users = db.session.query(UserModel).all()
    return json.loads(json.dumps(users, cls=AlchemyEncoder))


def login(email, password):
    resp = {"status": False, "user": {}}
    user_model = db.session.query(UserModel).filter(UserModel.email == email).first()

    if user_model is not None:
        if user_model.is_otp_needed:
            return {"status": False, "message": "OTP Required"}
        elif bcrypt.checkpw(str(password).encode("UTF-8"), str(user_model.password).encode("UTF-8")):
            return {"status": True, "user": {"id": user_model.id, "name": user_model.name, "email": user_model.email,
                                             "type": user_model.user_type}}
        else:
            return {"status": False, "message": "Wrong email address or password"}

    return resp


def change_password(userid, current_password, newpassword):
    user_model = db.session.query(UserModel).filter(UserModel.id == userid).first()
    if user_model is not None:
        if bcrypt.checkpw(current_password, user_model.password):
            user_model.password = bcrypt.hashpw(newpassword, bcrypt.gensalt())
            db.session.commit()
            return {"status": True, "message": "Password successfully changed",
                    "user": {"id": user_model.id, "email": user_model.email}}
        else:
            return {"status": False, "message": "Invalid current password"}

    return {"status": False, "message": "User does not exist"}


def reset_password(userid, newpassword):
    user_model = db.session.query(UserModel).filter(UserModel.id == userid).first()
    print("User info")
    print(user_model)
    if user_model is not None:
        user_model.password = bcrypt.hashpw(str(newpassword).encode("UTF-8"), bcrypt.gensalt())
        db.session.commit()
        return {"status": True, "message": "Password successfully changed",
                "user": {"id": user_model.id, "email": user_model.email}}
    return {"status": False, "message": "User does not exist"}


def forgot_password(phone):
    user_model = db.session.query(UserModel).filter(UserModel.phone == phone).first()
    print(user_model)
    if user_model is not None:  # send otp email
        otp = generate_otp()
        # render templates and send email to user
        res = Utils.send_sms(user_model.phone, f"Hello {user_model.name},Your OTP Code is: {otp}")
        # res = send_otp_email(user_model.email, "Host scanner OTP", otp)

        if res:
            user_model.is_otp_needed = True
            user_model.otp = otp
            db.session.commit()
            return {"status": True, "message": "OTP Sent successfully", "user": {"email": user_model.email}}
        else:
            return {"status": False, "message": "Something went wrong"}

    return {"status": False, "message": "User does not exist"}


def verify_otp(email, otp):
    user_model = db.session.query(UserModel).filter(UserModel.email == email).first()
    if user_model is not None:
        if user_model.otp == int(otp):
            user_model.is_otp_needed = False
            user_model.otp = None
            db.session.commit()
            return {"status": True, "message": "OTP successfully verified",
                    "user": {"id": user_model.id, "email": user_model.email}}
        else:
            return {"status": False, "message": "Invalid One Time Passcode"}

    return {"status": False, "message": "User does not exist"}


def generate_otp():
    mycode = [str(random.randint(0, 9)) for _ in range(6)]
    otp = "".join(mycode)
    return otp


def send_otp_email(receiver, title, otp):
    try:
        sender = os.getenv("SENDER_EMAIL")
        # Create message container - the correct MIME type is multipart/alternative.
        msg = MIMEMultipart('alternative')
        msg['Subject'] = title
        msg['From'] = sender
        msg['To'] = receiver

        # Create the body of the message (a plain-text and an HTML version).
        text = "Hello!\nKindly use this One Time Passcode:" + otp + "<font>\n to change your account password?\n\nBest Regards,\nHost scanner Admin\nIshimwe Fabienne"
        html = """\
        <html>
          <head></head>
          <body>
            <p>Hello!<br>
               Kindly use this <b>One Time Passcode:<font color='blue'>""" + otp + """</font> </b><br> to change your account password?<br><br>
               Best Regards,<br><br>
    
               <b>Host scanner Admin<br>Ishimwe Fabienne</b>
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
        print(f"Error occurred {str(e)}")
        return False
    return True
