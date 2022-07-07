from flask_restful import Resource
from flask import Response, request
from srv.controllers.email import save_emails
from srv.helpers.loader import make_json_response

class EmailScheduleSaveResource(Resource):
    def post(self, **kwargs) -> Response:
        forms = request.json
        try:
            status, response = save_emails(**forms)
        except Exception as e:
            print(e)
            status, response = 500, dict(message="Internal Server Error")
        return make_json_response(http_status=status, data=response)
