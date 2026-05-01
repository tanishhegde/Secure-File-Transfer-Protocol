from crypto.rsa import sign
from crypto.aesgcm import encrypt
from transport.socket_transport import send
import hashlib
import os

def send_file(sock, filepath, session_key, my_rsa_private):
    with open(filepath, "rb") as f:
        file = f.read()

    hash = hashlib.sha256(file).digest()
    signature = sign(hash, my_rsa_private)

    ciphertext, nonce = encrypt(file, session_key)

    send(sock, os.path.basename(filepath).encode())
    send(sock, ciphertext)
    send(sock, nonce)
    send(sock, signature)
