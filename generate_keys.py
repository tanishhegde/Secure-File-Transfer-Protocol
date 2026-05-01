# generate_keys.py
import sys
sys.path.insert(0, '.')
from crypto.rsa import generate_rsa_key, save_keys
import os

os.makedirs("peer_a/keys", exist_ok=True)
os.makedirs("peer_b/keys", exist_ok=True)

private_a, public_a = generate_rsa_key()
save_keys(private_a, public_a, "peer_a/keys")

private_b, public_b = generate_rsa_key()
save_keys(private_b, public_b, "peer_b/keys")

# cross-copy public keys
import shutil
shutil.copy("peer_b/keys/public_key.pem", "peer_a/keys/B_public_key.pem")
shutil.copy("peer_a/keys/public_key.pem", "peer_b/keys/B_public_key.pem")

print("Done! Keys generated and exchanged.")
