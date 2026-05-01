from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

def derive_session_key(shared_secret: bytes):
    session_key = HKDF(algorithm = hashes.SHA256(), length = 32, salt = None, info = b'session key').derive(shared_secret)

    return session_key

