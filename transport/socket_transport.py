import struct

def send(sock, data):
    length = len(data)
    length_bytes = struct.pack(">I", length)

    sock.sendall(length_bytes)
    sock.sendall(data)

def receive(sock):
    length_bytes = sock.recv(4)
    length = struct.unpack(">I", length_bytes)[0]

    data = b""
    while len(data) < length:
        chunk = sock.recv(length - len(data))
        data += chunk

    return data
