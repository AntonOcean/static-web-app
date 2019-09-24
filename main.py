# import mimetypes
# import os
# import socket
# import logging
# from datetime import datetime
# from urllib.parse import unquote
#
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format='%(message)s')
#
# HOST = 'localhost'
# PORT = 9090
#
# StatusOk = 200
# NotFound = 404
# MethodNotAllowed = 405
# Forbidden = 403
#
# DIST_DIR = 'httptest'
#
#
# RESPONSE_OK = 'HTTP/{} {}\r\n' \
# 			'Content-Type: {}\r\n' \
# 			'Content-Length: {}\r\n'\
# 			'Date: {}\r\n' \
# 			'Server: PythonServer\r\n\r\n'
#
# RESPONSE_FAIL = 'HTTP/{} {}\r\n' \
# 			'Server: PythonServer'
#
# DATETIME_TEMPLATE = '%a, %d %b %Y %H:%M:%S GMT'
#
# ALLOW_METHODS = ['HEAD', 'GET']
#
# # test_response = \
# #     '''HTTP/1.1 200 OK
# # Date: Mon, 27 Jul 2009 12:28:53 GMT
# # Server: Linux
# # Connection: keep-alive
# # '''
# #
# # test_response_i = \
# #     '''HTTP/1.1 200 OK
# # Date: Mon, 27 Jul 2009 12:28:53 GMT
# # Server: Linux
# # Connection: keep-alive
# # Content-Length: 88
# # Content-Type: text/html
# #
# # <html>
# # <body>
# # <h1>Hello, World!</h1>
# # </body>
# # </html>
# # '''
# #
# # mime_type = {
# #     "html": "text/html",
# #     "css": "text/css",
# #     "js": "application/javascript",
# #     "jpg": "image/jpeg",
# #     "jpeg": "image/jpeg",
# #     "png": "image/png",
# #     "gif": "image/gif",
# #     "swf": "application/x-shockwave-flash",
# #     'txt': 'text/txt',
# #     'default': 'text/plain'
# # }
#
#
# # namedtuple
# # class HTTPContent:
# #     def __init__(self, content: bytes, content_type: str):
# #         self.data = content
# #         self.content_type = mime_type.get(content_type, 'text/plain')
#
#
# def parse_http_request(http: bytes):
#     http_protocol_lines = [line for line in http.decode().split('\r\n') if line]
#
#     if not http_protocol_lines or not http_protocol_lines[0].split():
#         return None
#
#     start_line = http_protocol_lines[0]
#     headers = http_protocol_lines[1:]
#     http_data = {
#         "method": start_line.split()[0],
#         "path": start_line.split()[1],
#         "protocol": start_line.split()[2],
#     }
#     http_data.update({header.split(': ')[0]: header.split(': ')[1] for header in headers if header.split(': ')})
#
#     logger.info(http_data)
#
#     return http_data
#
#
# def parse_http_response(request, status=200, content: bytes = None) -> bytes:
#     # print(status)
#     protocol = request.get("protocol")
#     status_description = {
#         200: "OK",
#         400: "Bad Request",
#         403: "Forbidden",
#         404: "Not Found",
#         405: "Method Not Allowed"
#     }
#     http_protocol_lines = [f'{protocol} {status} {status_description.get(status)}']
#     header = {
#         "Date": datetime.now().strftime('%a, %d %b %Y %H:%M:%S GMT'),
#         "Server": "Linux",
#         "Connection": "keep-alive",
#     }
#     if status == 200:
#         content_type, _ = mimetypes.guess_type(request["path"])
#         header.update({
#             "Content-Length": str(len(content)) if content else '0',
#             "Content-Type": content_type or 'text/plain'
#         })
#     http_protocol_lines.extend([": ".join([k, v]) for k, v in header.items()])
#     http_protocol_lines.append("\r\n")
#
#     content_data = content or b"\r\n\r\n"
#
#     if request["method"] == "HEAD":
#         content_data = b""
#
#     return "\r\n".join(http_protocol_lines).encode() + content_data
#
#
# # model
# def get_file_content(abs_path: str) -> bytes:
#     with open(abs_path, "rb") as fs:
#         data = fs.read()
#     return data
#
#
# # view
# def static_handler(request):
#     if request["method"] not in ALLOW_METHODS:
#         return parse_http_response(request, status=405)
#
#     base_path = request["path"].split('?')[0][1:]
#     security = '..' not in base_path.split('/')
#
#     permission = base_path.startswith(DIST_DIR)
#     if not permission or not security:
#         return parse_http_response(request, status=400)
#
#     abs_path = unquote(os.path.join(os.getcwd(), base_path))
#
#     if os.path.isdir(abs_path):
#         abs_path = os.path.join(abs_path, "index.html")
#         if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
#             return parse_http_response(request, status=403)
#
#     if not os.path.exists(abs_path) or not os.path.isfile(abs_path):
#         return parse_http_response(request, status=404)
#
#     content = get_file_content(abs_path)
#
#     return parse_http_response(request, content=content)
#
#
# def main():
#     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#         s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#         s.bind((HOST, PORT))
#         s.listen()  # максимальное кол-во коннектов в очереди
#
#         logger.info(f"ready http://{HOST}:{PORT}")
#         while True:
#             conn, addr = s.accept()
#             with conn:
#                 data = conn.recv(1024)
#                 if not data:
#                     break
#
#                 # todo middleware
#                 try:
#                     r = parse_http_request(data)
#
#                     if not r:
#                         conn.sendall(b"")
#                         continue
#
#                     ans = static_handler(r)
#                 except Exception as e:
#                     logger.error("ERROR " + str(e))
#                     conn.sendall(b"")
#                     continue
#                 conn.sendall(ans)
#
#
# if __name__ == '__main__':
#     main()
