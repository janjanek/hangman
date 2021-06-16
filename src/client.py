import socket
import sys
import threading
import ssl

SERVER = "127.0.0.1"
PORT = 5001
GAMES = {}
FORMAT = 'utf-8'
BUF_SIZE = 1024


def handle_disconnect(client_sock) -> None:
    """
    :param client_sock:
    :return:
    function handling disconnection
    """
    client_sock.close()


def handle_input(client_sock) -> None:
    """
    :param client_sock:
    :return:
    function is responsible for sending
    data to server and handling input from client
    """
    while True:
        msg = input()
        if msg == "end":
            client_sock.send("end".encode(FORMAT))
            handle_disconnect(client_sock)
            break

        try:
            client_sock.send(msg.encode(FORMAT))
        except (BrokenPipeError, ConnectionError):
            print("SERVER CLOSED CONNECTION")


if __name__ == "__main__":
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)

    """ssl client sock"""
    client_sock = ssl.wrap_socket(client,
                                  cert_reqs=ssl.CERT_REQUIRED,
                                  ssl_version=ssl.PROTOCOL_TLSv1_2,
                                  ca_certs="./src/client_utils/trusted_certs.crt")

    client_sock.connect((SERVER, PORT))

    if not client_sock.getpeercert():
        raise Exception("Invalid SSL cert")

    # TODO implement logs
    print(f"CONNECTED TO {SERVER}:{PORT}")

    thread = threading.Thread(target=handle_input, args=[client_sock],
                              daemon=True)
    thread.start()
    while True:
        try:
            try:
                msg = client_sock.recv(BUF_SIZE)
                print(msg.decode(FORMAT))
                if msg.decode(FORMAT) == "end":
                    client_sock.close()
                    sys.exit()
            except ConnectionError:
                handle_disconnect(client_sock)
                break
        except KeyboardInterrupt:
            handle_disconnect(client_sock)
            break

    client_sock.close()
