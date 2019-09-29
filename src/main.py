import asyncio
import logging
import multiprocessing

import uvloop

from config import CONFIG
from http_engine.request import parse_http_request
from server import run, get_socket
from views import static_handler

logging.basicConfig(level=logging.INFO, format='%(message)s')

HOST = '0.0.0.0'
PORT = 80
CPU_COUNT = int(CONFIG.get('cpu_limit', multiprocessing.cpu_count())) - 1


async def engine(recv_data: bytes) -> bytes:
    try:
        r = parse_http_request(recv_data)

        if not r:
            return b""

        return await static_handler(r)
    except Exception as e:
        logging.error("ERROR " + str(e))
        return b""


def worker_run(loop, server_sock):
    loop.run_until_complete(run(loop, server_sock, engine))


def main():
    server_sock = get_socket(HOST, PORT)

    workers = []

    for _ in range(CPU_COUNT):
        loop = uvloop.new_event_loop()
        asyncio.set_event_loop(loop)

        worker_process = multiprocessing.Process(target=worker_run, args=(loop, server_sock))
        workers.append(worker_process)
        worker_process.start()

    try:
        for worker in workers:
            worker.join()
    except KeyboardInterrupt:
        for worker in workers:
            worker.terminate()


if __name__ == '__main__':
    main()
