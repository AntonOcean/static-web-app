import asyncio
import logging
import socket

CHUNK_SIZE_HTTP = 1024
QUEUE_SOCKET = 8
TIMEOUT_CLIENT = 5


async def get_data(client):
    loop = asyncio.get_event_loop()
    data = b''
    while True:
        chunk = await loop.sock_recv(client, CHUNK_SIZE_HTTP)
        data += chunk
        if len(chunk) < CHUNK_SIZE_HTTP:
            break
    return data


def get_socket(host, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen(QUEUE_SOCKET)
    server_sock.setblocking(False)
    logging.info('Start on {}'.format(server_sock.getsockname()))
    return server_sock


async def handle_client(client, core_engine, loop):
    data = await get_data(client)

    data_generator = await core_engine(data)

    for chunk in data_generator:
        await loop.sock_sendall(client, chunk)

    client.close()


async def run(loop, server_sock, core_engine):
    while True:
        client, _ = await loop.sock_accept(server_sock)
        client.settimeout(TIMEOUT_CLIENT)
        loop.create_task(handle_client(client, core_engine, loop))
