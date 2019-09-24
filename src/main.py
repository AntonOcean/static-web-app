import logging

from http_engine.request import parse_http_request
from server import run
from views import static_handler

logging.basicConfig(level=logging.INFO, format='%(message)s')

HOST = '0.0.0.0'
PORT = 80


def engine(recv_data: bytes) -> bytes:
    try:
        r = parse_http_request(recv_data)

        if not r:
            return b""

        return static_handler(r)
    except Exception as e:
        logging.error("ERROR " + str(e))
        return b""


def main():
    # BrokenPipeError: [Errno 32] Broken pipe
    # ab -k -c 100 -n 10000 127.0.0.1:9090/httptest/wikipedia_russia.html
    run(HOST, PORT, engine)


if __name__ == '__main__':
    main()
    # config = {}
    # with open("../httpd.conf", "r") as fs:
    #     for line in fs.readlines():
    #         k, v = line.split()
    #         config[k] = v

