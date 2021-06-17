import socket
import threading
import ssl
import datetime
import time

from game import Game

SERVER = "127.0.0.1"
PORT = 5001
GAMES = {}
FORMAT = 'utf-8'
BUFF_SIZE = 1024
CLIENTS_COUNTER = 1


def write_to_logs(event):
    file_logs = open("logs.txt", "a")
    time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    file_logs.write(f"{time}: {event} \n")
    file_logs.close()


def end_game(game_id: int) -> None:
    if game_id in GAMES:
        game = GAMES[game_id]
        handle_disconnect(game.client_1_sock)
        handle_disconnect(game.client_2_sock)
        del GAMES[game_id]


def handle_disconnect(client_sock) -> None:
    try:
        print(f"CLIENT: {client_sock.fileno()} DISCONNECTED")
        write_to_logs(f"CLIENT: {client_sock.fileno()} DISCONNECTED")
        client_sock.send("end".encode(FORMAT))
        client_sock.close()
        global CLIENTS_COUNTER
        CLIENTS_COUNTER -= 1
    except Exception:
        write_to_logs("CLIENT ALREADY DISCONNECTED")
        print("CLIENT ALREADY DISCONNECTED")


def handle_client(client_sock, game_id: int, client_number: int) -> None:
    """
    :param client_sock:
    :param game_id:
    :param client_number:
    :return:
    """

    first_msg = client_sock.recv(BUFF_SIZE).decode(FORMAT)
    if first_msg != "start":
        handle_disconnect(client_sock)

    while game_id not in GAMES:
        client_sock.send("WAITING FOR PLAYER...\n".encode(FORMAT))
        # client_sock.send("TO REFRESH TYPE refresh\n".encode(FORMAT))
        time.sleep(1)

    game = GAMES[game_id]
    client_sock.send("GAME HAS BEEN STARTED\n".encode(FORMAT))
    client_sock.send(f"CATEGORY {game.category}\n".encode(FORMAT))
    client_sock.send(f"PUT THE WORD FROM GAME CATEGORY\n".encode(FORMAT))

    start = True
    while game_id in GAMES:
        try:
            msg = client_sock.recv(BUFF_SIZE).decode(FORMAT)
            # print(msg)

            if start:
                game.set_words(client_number, msg)
                game.set_lives(4)
                client_sock.send(f"PUT LETTER\n".encode(FORMAT))
                start = False
            else:
                game = GAMES[game_id]
                game.playing_hangman(client_number, msg)

                """if somebody won"""
                if game.score():
                    with game.lock:
                        end_game(game_id)
                    break

        except (EOFError, ConnectionError):
            handle_disconnect(client_sock)


if __name__ == "__main__":
    game_id = 0

    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # server_sock = socket.socket()
    server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_sock.bind((SERVER, PORT))
    server_sock.listen(5)

    print(f"SERVER STARTED ON {SERVER}:{PORT}")
    write_to_logs(f"SERVER STARTED ON {SERVER}:{PORT}")
    client_1 = None
    client_number = 0
    while True:
        try:
            try:
                client, addr = server_sock.accept()
            except ConnectionError as err:
                write_to_logs(repr(err))
                print(repr(err))

            print(f"CLIENT: {client.fileno()} ADDR: {addr} CONNECTED")
            write_to_logs(f"CLIENT: {client.fileno()} ADDR: {addr} CONNECTED")

            ssl_client = ssl.wrap_socket(client,
                                         server_side=True,
                                         certfile="./src/server_utils/server.crt",
                                         keyfile="./src/server_utils/server.key",
                                         ssl_version=ssl.PROTOCOL_TLSv1_2)

            client_sock = ssl_client

            """Fix CLIENTS_COUTNER"""
            # if not CLIENTS_COUNTER % 2:
            if not CLIENTS_COUNTER % 2:
                client_2 = client_sock
                client_number = 1
                GAMES[game_id // 2] = Game(client_1,
                                           client_2,
                                           FORMAT,
                                           BUFF_SIZE,
                                           threading.Lock())
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
        except KeyboardInterrupt:
            server_sock.close()
            break

