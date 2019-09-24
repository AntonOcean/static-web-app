import mimetypes
from datetime import datetime

DATETIME_TEMPLATE = '%a, %d %b %Y %H:%M:%S GMT'


def parse_http_response(request, status=200, content: bytes = None) -> bytes:
    protocol = request.get("protocol")
    status_description = {
        200: "OK",
        400: "Bad Request",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed"
    }
    http_protocol_lines = [f'{protocol} {status} {status_description.get(status)}']
    header = {
        "Date": datetime.now().strftime(DATETIME_TEMPLATE),
        "Server": "Linux",
        "Connection": "close",
    }
    if status == 200:
        content_type, _ = mimetypes.guess_type(request["path"])
        header.update({
            "Content-Length": str(len(content)) if content else '0',
            "Content-Type": content_type or 'text/plain'
        })
    http_protocol_lines.extend([": ".join([k, v]) for k, v in header.items()])
    http_protocol_lines.append("\r\n")

    content_data = content or b"\r\n\r\n"

    if request["method"] == "HEAD":
        content_data = b""

    return "\r\n".join(http_protocol_lines).encode() + content_data
