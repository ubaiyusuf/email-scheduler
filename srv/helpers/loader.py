import importlib
import json
import os
from http import HTTPStatus
from typing import Union

from flask import Response


def discover_blueprints(path: str) -> list:
    blueprints = list()
    dir_name = os.path.basename(path)
    packages = os.listdir(os.path.join(path, "blueprints"))

    for package in packages:
        if str(package).endswith(".py") and str(package) != "__init__.py":
            package = str(package).replace(".py", "")
            module_name = f"{dir_name}.blueprints.{package}"
            module = importlib.import_module(module_name)
            module_blueprints = [bp for bp in dir(module) if bp.endswith("_blueprint")]

            for mb in module_blueprints:
                blueprints.append(getattr(module, mb))

    return blueprints


def load_models(path: str) -> list:
    dir_name = os.path.basename(path)
    packages = os.listdir(f"{path}/models")

    for package in packages:
        if str(package).endswith(".py") and str(package) != "__init__.py":
            package = str(package).replace(".py", "")
            module_name = f"{dir_name}.models.{package}"
            importlib.import_module(module_name)


def make_json_response(http_status: Union[HTTPStatus, int], data: dict) -> Response:
    return Response(
        response=json.dumps(data), status=http_status, mimetype="application/json"
    )
