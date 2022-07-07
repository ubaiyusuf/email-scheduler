import http
import pytz

from flask_mail import Message
from datetime import datetime

from srv import mail
from srv.models.email import EventsModel

jkt_tz = pytz.timezone("Asia/Singapore")

def save_emails(*args,**kwargs):
    event_id = kwargs.get('event_id')
    email_subject = kwargs.get('email_subject')
    email_content = kwargs.get('email_content')
    timestamp = kwargs.get('timestamp')

    #check timestamp and convert it to 0 seconds
    if timestamp:
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M")
    else:
        return http.HTTPStatus.BAD_REQUEST, dict(message="timestamp mandatory")

    #edit event 
    if event_id:
        #get related event
        event = EventsModel.query.filter_by(
            is_deleted=False,
            event_id=event_id
        ).first()

        #if event not found, return bad request
        if not event:
            return http.HTTPStatus.BAD_REQUEST, dict(message="event not found")
        
        #check if edit email_subject
        if email_subject:
            event.email_subject = email_subject
        #check if edit email content
        if email_content:
            event.email_content = email_content
        #get timestamp
        event.timestamp = timestamp

        event.save()

        response = dict(
            code=int(http.HTTPStatus.OK), message="event edited"
        )

        return http.HTTPStatus.OK, response
    #save new event
    else:
        #check email subject (can be empty)
        if not email_subject:
            email_subject = ""
        #check email content (can be empty)
        if not email_content:
            email_content = ""

        new_event_data = dict()
        new_event_data['event_id'] = event_id
        new_event_data['email_subject'] = email_subject
        new_event_data['email_content'] = email_content
        new_event_data['timestamp'] = timestamp

        EventsModel(**new_event_data).save()
    
        response = dict(
            code=int(http.HTTPStatus.CREATED), message="event created"
        )

        return http.HTTPStatus.CREATED, response

def send_email(*args,**kwargs):
    #try to send message
    try:
        msg = Message(
            kwargs.get("email_subject"),
            sender = ("Event", kwargs.get("email_sender")),
            recipients = [kwargs.get("email_recipient")]
        )
        msg.body = kwargs.get("email_content")
        mail.send(msg)
    except Exception as e:
        print(e)
