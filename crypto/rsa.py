from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature
import os

# This generates the RSA keys for authentication which is used only once. 
def generate_rsa_key(key_size: int = 2048):
    private_key = rsa.generate_private_key(public_exponent = 65537, key_size = key_size)
    public_key = private_key.public_key()
    return private_key, public_key

# This function saves the private_key and public_key to "/keys" directory
def save_keys(private_key, public_key, filepath: str):
    encryption = (serialization.NoEncryption())

    private_pem = private_key.private_bytes(encoding = serialization.Encoding.PEM, format = serialization.PrivateFormat.PKCS8, encryption_algorithm = encryption)
    os.makedirs(filepath, exist_ok = True)
    with open(f"{filepath}/private_key.pem", "wb") as f:
        f.write(private_pem)

    public_pem = public_key.public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo)
    with open(f"{filepath}/public_key.pem", "wb") as f:
        f.write(public_pem)

# This function loads the private_key
def load_private_key(filepath: str):
    with open(f"{filepath}/private_key.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password = None)
    return private_key

# This function loads the public_key
def load_public_key(filepath: str):
    with open(f"{filepath}", "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    return public_key

# Function for signing
def sign(data: bytes, private_key):
    signature = private_key.sign(data, padding.PSS(mgf = padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH), hashes.SHA256())
    return signature

def verify(data: bytes, signature: bytes, public_key):
    try:
        public_key.verify(signature, data, padding.PSS(mgf = padding.MGF1(hashes.SHA256()), salt_length = padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except InvalidSignature:
        return False

