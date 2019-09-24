import logging


def parse_http_request(http: bytes):
    http_protocol_lines = [line for line in http.decode().split('\r\n') if line]

    if not http_protocol_lines or not http_protocol_lines[0].split():
        return None

    start_line = http_protocol_lines[0]
    headers = http_protocol_lines[1:]
    http_data = {
        "method": start_line.split()[0],
        "path": start_line.split()[1],
        "protocol": start_line.split()[2],
    }
    http_data.update({header.split(': ')[0]: header.split(': ')[1] for header in headers if header.split(': ')})

    logging.info(http_data)

    return http_data
