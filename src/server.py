import asyncio
import logging
import socket


async def get_data(client):
    loop = asyncio.get_event_loop()
    data = b''
    while True:
        chunk = await loop.sock_recv(client, 1024)
        data += chunk
        if len(chunk) < 1024:
            break
    return data


def get_socket(host, port):
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((host, port))
    server_sock.listen()
    server_sock.setblocking(False)
    return server_sock


async def handle_client(client, core_engine):
    data = await get_data(client)

    ans = await core_engine(data)

    loop = asyncio.get_event_loop()
    await loop.sock_sendall(client, ans)

    client.close()


async def run(host, port, engine):
    server_sock = get_socket(host, port)
    logging.info('Start on {}'.format(server_sock.getsockname()))
    loop = asyncio.get_event_loop()

    while True:
        client, _ = await loop.sock_accept(server_sock)
        client.settimeout(5)
        loop.create_task(handle_client(client, engine))
