from biplist import *
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256
from base64 import b64encode
from tkinter import Tk   
from tkinter.filedialog import askopenfilename

def read_enote_file(filename,username,password):
    try:
        plist = readPlist(filename)
    except (InvalidPlistException, NotBinaryPlistException):
        print ("Not a plist:")

    nonce = plist[0][0:12]
    tag = plist[0][-16:]
    ciphertext = plist[0][12:-16]
    pass_word = SHA256.new(b64encode((username + password).encode("utf-8"))).digest()
    encobj = AES.new(pass_word,  AES.MODE_GCM, nonce)
    dd = encobj.decrypt_and_verify(ciphertext, tag)
    print(dd)


Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
read_enote_file(filename,username="aa",password="bb")
