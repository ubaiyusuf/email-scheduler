from srv import db
from srv.models.commons import BaseModel

class EmailsModel(BaseModel):
    __tablename__ = "emails"

    email_id = db.Column(db.Integer(), primary_key=True)
    email = db.Column(db.String, nullable=False)

class EventsModel(BaseModel):
    __tablename__ = "events"
    
    event_id = db.Column(db.Integer(), primary_key=True)
    email_subject = db.Column(db.String, nullable=True)
    email_content = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, nullable=False)
    is_sent = db.Column(db.Boolean, nullable=False, default=False)
    