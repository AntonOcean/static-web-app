import os
from urllib.parse import unquote

from http_engine import status
from http_engine.methods import GET, HEAD
from http_engine.response import parse_http_response

DIST_DIR = 'httptest'


def static_handler(request):
    if request["method"] not in [GET, HEAD]:
        return parse_http_response(request, status=status.MethodNotAllowed)

    base_path = request["path"].split('?')[0][1:]
    security = '..' not in base_path.split('/')

    permission = base_path.startswith(DIST_DIR)
    if not permission or not security:
        return parse_http_response(request, status=status.BadRequest)

    abs_path = unquote(os.path.join(os.getcwd(), "../", base_path))

    if os.path.isdir(abs_path):
        abs_path = os.path.join(abs_path, "index.html")
        if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
            return parse_http_response(request, status=status.Forbidden)

    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
        return parse_http_response(request, status=status.NotFound)

    with open(abs_path, "rb") as fs:
        content = fs.read()

    return parse_http_response(request, content=content)
