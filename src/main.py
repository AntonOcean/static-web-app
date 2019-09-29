import asyncio
import logging

from http_engine.request import parse_http_request
from server import run
from views import static_handler

logging.basicConfig(level=logging.INFO, format='%(message)s')

HOST = '0.0.0.0'
PORT = 80


async def engine(recv_data: bytes) -> bytes:
    try:
        r = parse_http_request(recv_data)

        if not r:
            return b""

        return await static_handler(r)
    except Exception as e:
        logging.error("ERROR " + str(e))
        return b""


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(run(HOST, PORT, engine))
    except KeyboardInterrupt:
        loop.close()


if __name__ == '__main__':
    main()
