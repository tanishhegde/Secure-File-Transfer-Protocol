from crypto.rsa import verify
from crypto.aesgcm import decrypt
from transport.socket_transport import receive
import hashlib
import os

def receive_file(sock, session_key, their_rsa_public):
    filename = receive(sock).decode()
    ciphertext = receive(sock)
    nonce = receive(sock)
    signature = receive(sock)

    plaintext = decrypt(ciphertext, session_key, nonce)
    hash = hashlib.sha256(plaintext).digest()
    
    if verify(hash, signature, their_rsa_public) != True:
        raise Exception("Verification of Hash Failed!")

    os.makedirs("files", exist_ok = True)
    with open(f"files/{filename}", "wb") as f:
        f.write(plaintext)
