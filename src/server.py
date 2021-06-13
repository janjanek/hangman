import socket
import threading
import ssl


from src.game import Game

SERVER = "127.0.0.1"
PORT = 5001
GAMES = {}
FORMAT = 'utf-8'
BUFF_SIZE = 1024
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


def is_not_connected(client_sock, game_id: int) -> bool:
    client_sock.send("WAITING FOR PLAYER...\n".encode(FORMAT))
    # client_sock.send("TO DISCONNECT GAME TYPE 'end'\n".encode(FORMAT))
    while game_id not in GAMES:
        pass
    return False


def handle_client(client_sock: socket.socket, game_id: int, client_number: int) -> None:
    """
    :param client_sock:
    :param game_id:
    :param client_number:
    :return:
    """
    """before game has been started"""
    if is_not_connected(client_sock, game_id):
        return None

    game = GAMES[game_id]
    client_sock.send("GAME HAS BEEN STARTED\n".encode(FORMAT))
    client_sock.send(f"CATEGORY {game.category}\n".encode(FORMAT))

    first_msg = True
    while True:
        try:
            msg = client_sock.recv(BUFF_SIZE).decode(FORMAT)
            print(msg)
            if not first_msg:
                # TODO Here should be playing logic with sockets
                game.playing(client_number, msg)

                """if somebody won"""
                if game.score():
                    break
            else:
                first_msg = False
                game.set_words(client_number, msg)
                game.set_lives(client_number, 4)
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

    server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock.bind((SERVER, PORT))
    server_sock.listen(5)

    print(f"SERVER STARTED ON {SERVER}:{PORT}")
    client_1 = None
    client_number = 0
    while True:
        client, addr = server_sock.accept()

        print(f"CLIENT: {client.fileno()} ADDR: {addr} CONNECTED")
        # TODO every print should be saved in logs.txt file

        ssl_client = ssl.wrap_socket(client,
                                     server_side=True,
                                     certfile="src/server_utils/server.crt",
                                     keyfile="src/server_utils/server.key",
                                     ssl_version=ssl.PROTOCOL_TLSv1_2)

        client_sock = ssl_client

        if not CLIENTS_COUNTER % 2:
            client_2 = client_sock
            client_number = 1
            GAMES[game_id // 2] = Game(client_1, client_2, FORMAT, BUFF_SIZE)
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

