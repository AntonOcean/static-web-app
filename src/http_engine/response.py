import mimetypes
import os
from datetime import datetime
from http_engine import status as http_status

DATETIME_TEMPLATE = '%a, %d %b %Y %H:%M:%S GMT'
CHUNK_SIZE_FILE = 262144


def read_in_chunks(path, chunk_size=CHUNK_SIZE_FILE):
    with open(path, "rb") as fs:
        while True:
            data = fs.read(chunk_size)
            if not data:
                break
            yield data


def parse_http_response(request, status=http_status.StatusOk, path_to_content=None) -> bytes:
    protocol = request.get("protocol")
    http_protocol_lines = [f'{protocol} {status} {http_status.STATUS_DESCRIPTION.get(status)}']
    header = {
        "Date": datetime.now().strftime(DATETIME_TEMPLATE),
        "Server": "Linux",
        "Connection": "close",
    }
    if status == http_status.StatusOk:
        content_type, _ = mimetypes.guess_type(request["path"])
        header.update({
            "Content-Length": str(os.path.getsize(path_to_content)) if path_to_content else '0',
            "Content-Type": content_type or 'text/plain'
        })
    http_protocol_lines.extend([": ".join([k, v]) for k, v in header.items()])
    http_protocol_lines.append("\r\n")

    null_body = path_to_content or request["method"] == "HEAD"
    content_data = b"" if null_body else b"\r\n\r\n"

    yield "\r\n".join(http_protocol_lines).encode() + content_data

    if request["method"] != "HEAD" and path_to_content:
        for chunk in read_in_chunks(path_to_content):
            yield chunk
