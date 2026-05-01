from cryptography.hazmat.primitives.asymmetric.x25519 import X25519PrivateKey, X25519PublicKey
from cryptography.hazmat.primitives import serialization

def generate_keys():
    private_key = X25519PrivateKey.generate()
    public_key = private_key.public_key()

    return private_key, public_key

def generate_shared_secret(private_key, public_key):
    shared_secret = private_key.exchange(public_key)

    return shared_secret

def public_key_to_bytes(public_key):
    public_key_bytes = public_key.public_bytes(encoding = serialization.Encoding.Raw, format = serialization.PublicFormat.Raw)

    return public_key_bytes

def public_key_from_bytes(data: bytes):
    public_key = X25519PublicKey.from_public_bytes(data)

    return public_key

