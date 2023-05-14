from biplist import *
import os
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256
from base64 import b64encode
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk

BG_COLOR = "#346466"
WIN_WIDTH = 600
WIN_HEIGHT = 600


def read_enote_file(filename, username, password):
    try:
        plist = readPlist(filename)
    except (InvalidPlistException, NotBinaryPlistException):
        print("Not a plist:")

    nonce = plist[0][0:12]
    tag = plist[0][-16:]
    ciphertext = plist[0][12:-16]
    pass_word = SHA256.new(b64encode((username + password).encode("utf-8"))).digest()
    encobj = AES.new(pass_word, AES.MODE_GCM, nonce)
    dd = encobj.decrypt_and_verify(ciphertext, tag)
    # print(dd)


root = tk.Tk()
root.title("Enote")
root.eval("tk::PlaceWindow . center")

master_frame = tk.Frame(root, width=WIN_WIDTH / 3, height=WIN_HEIGHT, bg=BG_COLOR)
master_frame.pack(side="left", fill="y", expand="no")
master_frame.pack_propagate(False)

detail_frame = tk.Frame(
    root,
    width=WIN_WIDTH,
    height=WIN_HEIGHT,
    bg=BG_COLOR,
    highlightbackground="green",
    highlightthickness=2,
)


detail_frame.pack(side="left",fill="both",expand="yes")
detail_frame.pack_propagate(False)


img = Image.open("Icon1024.jpeg")
resized_image = img.resize((30, 30), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(resized_image)
logo_widget = tk.Label(master_frame, image=logo_image, bg="#346466")
logo_widget.image = logo_image
logo_widget.pack(anchor="w")


# tk.Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# filename = askopenfilename() # show an "Open" dialog box and return the path to the selected file
# read_enote_file(filename,username="aa",password="bb")
root.mainloop()
