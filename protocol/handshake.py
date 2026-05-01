from crypto.rsa import sign, verify
from crypto.ecdh import generate_keys, public_key_to_bytes, public_key_from_bytes, generate_shared_secret
from crypto.session import derive_session_key
from transport.socket_transport import send, receive

def perform_handshake(sock, my_rsa_private, their_rsa_public):
    ecdh_private_key, ecdh_public_key = generate_keys()
    ecdh_public_key_bytes = public_key_to_bytes(ecdh_public_key)

    signed_key = sign(ecdh_public_key_bytes, my_rsa_private)
    send(sock, ecdh_public_key_bytes)
    send(sock, signed_key)

    their_ecdh_public_key_bytes = receive(sock)
    their_signed_key = receive(sock)
    if verify(their_ecdh_public_key_bytes, their_signed_key, their_rsa_public) != True:
        raise Exception("Handshake Failed! Signature Verfication Failed!")

    their_ecdh_public_key = public_key_from_bytes(their_ecdh_public_key_bytes)

    shared_secret = generate_shared_secret(ecdh_private_key, their_ecdh_public_key)
    session_key = derive_session_key(shared_secret)

    return session_key

