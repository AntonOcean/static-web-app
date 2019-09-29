import asyncio
import os
from urllib.parse import unquote

from config import CONFIG
from http_engine import status
from http_engine.methods import GET, HEAD
from http_engine.response import parse_http_response

ROOT_DIR = CONFIG.get('document_root', '/var/www/html')


def get_file(path):
    with open(path, "rb") as fs:
        return fs.read()


async def static_handler(request):
    if request["method"] not in [GET, HEAD]:
        return parse_http_response(request, status=status.MethodNotAllowed)

    base_path = request["path"].split('?')[0][1:]
    security = '..' not in base_path.split('/')

    if not security:
        return parse_http_response(request, status=status.BadRequest)

    abs_path = unquote(os.path.join(ROOT_DIR, base_path))

    if os.path.isdir(abs_path):
        abs_path = os.path.join(abs_path, "index.html")
        if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
            return parse_http_response(request, status=status.Forbidden)

    if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
        return parse_http_response(request, status=status.NotFound)

    loop = asyncio.get_event_loop()
    content = await loop.run_in_executor(None, get_file, abs_path)

    return parse_http_response(request, content=content)
