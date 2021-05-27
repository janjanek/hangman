import socket
import threading
from src.game import Game

SERVER = "127.0.0.1"
PORT = 5001
GAMES = {}
FORMAT = 'utf-8'
BUF_SIZE = 1024


def handle_disconnect(client_sock) -> None:
    # TODO handle disconnecting
    raise NotImplementedError


def handle_client(client_sock, game_id: int, client_number: int) -> None:
    """
    :param client_sock:
    :param game_id:
    :param client_number:
    :return:
    """
    while True:
        try:
            msg = client_sock.recv(BUF_SIZE).decode(FORMAT)
            # TODO implement protocol logic
            print(msg, client_sock.fileno())
            # TODO handle disconnect
            if game_id in GAMES:
                game = GAMES[game_id]
                if client_number == 0:
                    game.client_2_sock.send(msg.encode(FORMAT))
                else:
                    game.client_1_sock.send(msg.encode(FORMAT))
        except (EOFError, ConnectionError):
            # TODO Client switching
            """
            After disconnecting of client, connected
            client should back to the game query.
            Alternatively send information to connected
            client about disconnection of first client
            and ask him about restarting the game.
            """
            handle_disconnect(client_sock)
            del GAMES[game_id]
            break


if __name__ == "__main__":
    clients_counter = 1
    game_id = 0
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER, PORT))
    server_sock.listen(5)

    print(f"SERVER STARTED ON {SERVER}:{PORT}")
    client_1 = None
    client_number = 0
    while True:
        client_sock, addr = server_sock.accept()

        print(f"CLIENT: {client_sock.fileno()} ADDR: {addr} CONNECTED")
        # TODO implement logs

        if not clients_counter % 2:
            client_2 = client_sock
            client_number = 1
            GAMES[game_id//2] = Game(client_1, client_2)
        else:
            client_1 = client_sock
            client_number = 0

        client_thread = threading.Thread(target=handle_client,
                                         args=[client_sock,
                                               game_id // 2,
                                               client_number],
                                         daemon=True)
        client_thread.start()

        clients_counter += 1
        game_id += 1

