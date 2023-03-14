import os
import requests
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()


def send_sms(receiver=None, message=None):
    if is_in_work_time_range():
        data = {
            'recipients': receiver,
            'message': message,
            'sender': os.getenv("SMS_SENDER_USERNAME")
        }

        r = requests.post(
            'https://www.intouchsms.co.rw/api/sendsms/.json',
            data,
            auth=(os.getenv("SMS_USERNAME"), os.getenv("SMS_PASSWORD"))
        )

        print(r.json(), r.status_code)
        return r.status_code

    else:
        print("Out of work time range")


def is_in_work_time_range():
    today = datetime.now()
    now = str(today)[11:16]
    start = "08:15"
    end = "23:45"
    day = int(today.strftime("%w"))

    return start < now < end and day not in [2, 6, 7]  # not working saturday and sunday

if __name__ == '__main__':
    send_sms()
