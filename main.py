import socket
import threading
import os
import time
from crypto.rsa import generate_rsa_key, save_keys, load_private_key, load_public_key
from protocol.handshake import perform_handshake
from protocol.sender import send_file
from protocol.receiver import receive_file

KEY_DIR = "keys"
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", 5001))
B_HOST = os.environ.get("B_HOST", "localhost")
B_PORT = int(os.environ.get("B_PORT", 5001))

def setup_keys():
    if not os.path.exists(f"{KEY_DIR}/private_key.pem"):
        private_key, public_key = generate_rsa_key()
        save_keys(private_key, public_key, KEY_DIR)
    else:
        private_key = load_private_key(KEY_DIR)

    their_public_key = load_public_key(f"{KEY_DIR}/B_public_key.pem")
    return private_key, their_public_key

def listener(my_private_key, their_public_key):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", LISTEN_PORT))
    server.listen(1)
    print(f"Listening on Port {LISTEN_PORT}...")

    while True:
        conn, addr = server.accept()
        print(f"Incoming Connection from {addr}")
        session_key = perform_handshake(conn, my_private_key, their_public_key)
        receive_file(conn, session_key, their_public_key)
        conn.close()

if __name__ == "__main__":
    my_private_key, their_public_key = setup_keys()

    t = threading.Thread(target = listener, args = (my_private_key, their_public_key), daemon = True)
    t.start()

    while True:
        command = input("Enter command(send/exit): ")
        if command == "send":
            filepath = input("Enter filepath: ")
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            for attempt in range(5):
                try:
                    sock.connect((B_HOST, B_PORT))
                    break
                except:
                    print(f"Retrying... {attempt+1}/5")
                    time.sleep(2)
            session_key = perform_handshake(sock, my_private_key, their_public_key)
            send_file(sock, filepath, session_key, my_private_key)
            sock.close()
        elif command == "exit":
            break
        else:
            print("Wrong Command! Use \"send\" or \"exit\" only!")
