import socket
import re
import decimal
from Crypto.Util.number import *
from Crypto.Cipher import AES

# TODO: Replace password
PASSWORD = b"f2aa724b2f528763"

def recv_until(s, needle):
    """Receive data from a socket connection until the needle appears"""
    buf = b""
    while True:
        b = s.recv(1024)
        if not b:
            break
        buf += b
        if needle in buf:
            return buf
    return buf

s = socket.socket()
s.connect(("itsec.sec.in.tum.de", 7012))

# Read password prompt
recv_until(s, b": ")
s.sendall(PASSWORD + b"\n")

msg = recv_until(s, b"by a newline!").decode()
# Print message from server
print(msg)

# Parse crypto stuff and save it to variables you can work with
enc_k = int(re.search("enc_k = ([0-9a-f]+)", msg).group(1), 16)
iv = bytes.fromhex(re.search("iv = ([0-9a-f]*)", msg).group(1))
N = int(re.search("N = ([0-9a-f]*)", msg).group(1), 16)
e = int(re.search("e = ([0-9a-f]*)", msg).group(1), 16)
enc_msg = bytes.fromhex(re.search("enc_msg = ([0-9a-f]*)", msg).group(1))

# might be useful:
# use the decimal type for arbitary precision arithmetic
# the line bellow allows for 'precise enough' decimal floats
decimal.getcontext().prec = N.bit_length()

# TODO: Modify the lines below to your needs

enc_k_decrypted = pow(enc_k, 1/e)
k = long_to_bytes(enc_k_decrypted)[:16]
cipher = AES.new(key=k, mode=AES.MODE_CTR)
msg_decrypted = cipher.decrypt(enc_msg)
print(msg_decrypted)

s.sendall(f"{enc_msg.hex()}\n".encode())
answer = s.recv(1024)
print(answer) 