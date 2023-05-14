from biplist import *
import struct
import Cryptodome
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256
from hashlib import sha256
from Cryptodome.Protocol.KDF import PBKDF2
from base64 import b64encode
try:
    plist = readPlist("misc.enote")
except (InvalidPlistException, NotBinaryPlistException):
    print ("Not a plist:")

nonce = plist[0][0:12]
tag = plist[0][-16:]
ciphertext = plist[0][12:-16]
print(f"{len(tag) + len(nonce) + len(ciphertext)}")
#passi = SHA256.hash(bytes("aa+bb", "utf-8"))
pass_word = SHA256.new(b64encode("aabb".encode("utf-8"))).digest()
encobj = AES.new(pass_word,  AES.MODE_GCM, nonce)
dd = encobj.decrypt_and_verify(ciphertext, tag)
print(dd)
#E0pSoiwAW5SLBAPFOmOa+qL7Tj8uw3t6ofvTxZPNjMI=