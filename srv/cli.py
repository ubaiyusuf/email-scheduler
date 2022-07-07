import json
import os
import pytz

from flask import current_app
from flask.cli import AppGroup
from datetime import datetime

sg_tz = pytz.timezone("Asia/Singapore")

seeder_cli = AppGroup("seeder", help="All cli related to db seeder")

@seeder_cli.command("email_recipients", help="Seed email recipients data")
def email_recipients_seeder():
    from srv.models.email import EmailsModel
    filename = "email_recipients"
    base_dir = os.path.dirname(os.path.abspath(__file__))
    with open(f"{base_dir}/seeds/{filename}.json") as json_file:
        datum = json.load(json_file)
    for data in datum:
        existing = EmailsModel.query.filter_by(
            is_deleted=False,
            email=data.get("email")
        ).first()
        if not existing:
            print(f"inserting email recipient {data.get('email')}")
            EmailsModel(**data).save()
        else:
            print(f"email recipient {data.get('email')} is exist")

scheduler_cli = AppGroup("scheduler", help="All cli related to schedule checker")

@scheduler_cli.command("event_checker", help="check event to send")
def event_checker():
    from srv.models.email import EventsModel, EmailsModel
    from srv.controllers.email import send_email

    now = datetime.now(tz=sg_tz)
    now = now.strftime("%Y-%m-%d %H:%M")

    events = EventsModel.query.filter_by(
        is_deleted=False,
        is_sent=False,
        timestamp=now
    )

    if events.count() > 0 :
        events = events.all()

        emails = EmailsModel.query.filter_by(
            is_deleted=False
        ).all()

        for event in events :
            for mail in emails:
                mail_data = dict()
                mail_data["email_sender"] = current_app.config["MAIL_USERNAME"]
                mail_data["email_recipient"] = mail.email
                mail_data["email_subject"] = event.email_subject
                mail_data["email_content"] = event.email_content

            #send email
            send_email(**mail_data)

            #update is_sent attribute
            event.is_sent = True
            event.save()
        
