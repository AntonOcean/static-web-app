import logging
import socket


def run(host: str, port: int, core_engine):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen()  # максимальное кол-во коннектов в очереди

        logging.info(f"ready http://{host}:{port}")
        while True:
            conn, addr = s.accept()
            with conn:
                data = conn.recv(1024)
                if not data:
                    break

                ans = core_engine(data)

                conn.sendall(ans)
