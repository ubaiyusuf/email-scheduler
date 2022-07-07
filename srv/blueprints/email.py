from flask import Blueprint
from flask_restful import Api

from srv.resources.email import EmailScheduleSaveResource

email_blueprint = Blueprint("scheduler", __name__, url_prefix="")
email_resource = Api(email_blueprint)

email_resource.add_resource(EmailScheduleSaveResource, "/save_emails")
