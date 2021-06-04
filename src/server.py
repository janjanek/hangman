import socket
import threading
# TODO implement tsl connection
# import ssl


from src.game import Game

SERVER = "127.0.0.1"
PORT = 5001
GAMES = {}
FORMAT = 'utf-8'
BUF_SIZE = 1024
CLIENTS_COUNTER = 1


def handle_disconnect(client_sock, game_id: int) -> None:
    global CLIENTS_COUNTER
    CLIENTS_COUNTER -= 1
    if game_id in GAMES:
        game = GAMES[game_id]
        print(f"CLIENT: {game.client_1_sock.fileno()} DISCONNECTED")
        print(f"CLIENT: {game.client_2_sock.fileno()} DISCONNECTED")
        game.client_1_sock.close()
        game.client_2_sock.close()
        del GAMES[game_id]
    else:
        print(f"CLIENT: {client_sock.fileno()} DISCONNECTED")
        client_sock.close()

def handle_disconnect(client_sock) -> None:
    # TODO handle disconnecting
    raise NotImplementedError

def is_not_connected(client_sock, game_id: int) -> bool:
    client_sock.send("WAITING FOR PLAYER...\n".encode(FORMAT))
    client_sock.send("TO DISCONNECT GAME TYPE 'end'\n".encode(FORMAT))
    while game_id not in GAMES:
        msg = client_sock.recv(BUF_SIZE).decode(FORMAT)
        if msg == "end":
            handle_disconnect(client_sock, -1)
            return True
    return False


def handle_client(client_sock: socket.socket, game_id: int, client_number: int) -> None:
    """
    :param client_sock:
    :param game_id:
    :param client_number:
    :return:
    """
    """before game logic"""
    if is_not_connected(client_sock, game_id):
        return None

    game = GAMES[game_id]
    client_sock.send("GAME HAS BEEN STARTED\n".encode(FORMAT))
    client_sock.send(f"CATEGORY {game.category}\n".encode(FORMAT))

    while True:
        try:
            msg = client_sock.recv(BUF_SIZE).decode(FORMAT)
            game = GAMES[game_id]
            game.logic(client_number, msg)
        except (EOFError, ConnectionError):
            # TODO Client switching
            """
            After disconnecting of client, connected
            client should back to the game query.
            Alternatively send information to connected
            client about disconnection of first client
            and ask him about restarting the game.
            """
            handle_disconnect(client_sock, game_id)
            break


if __name__ == "__main__":
    clients_counter = 1
    game_id = 0

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    server_sock.bind((SERVER, PORT))
    server_sock.listen(5)

    print(f"SERVER STARTED ON {SERVER}:{PORT}")
    client_1 = None
    client_number = 0
    while True:
        client_sock, addr = server_sock.accept()

        print(f"CLIENT: {client_sock.fileno()} ADDR: {addr} CONNECTED")
        # TODO every print should be saved in logs.txt file

        if not CLIENTS_COUNTER % 2:
            client_2 = client_sock
            client_number = 1
            GAMES[game_id // 2] = Game(client_1, client_2, FORMAT)
        else:
            client_1 = client_sock
            client_number = 0

        client_thread = threading.Thread(target=handle_client,
                                         args=[client_sock,
                                               game_id // 2,
                                               client_number],
                                         daemon=True)
        client_thread.start()

        CLIENTS_COUNTER += 1
        game_id += 1

