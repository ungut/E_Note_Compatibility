from biplist import *
import os
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256
from base64 import b64encode
import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import json
import uuid
import sys
BG_COLOR = "#346466"
WIN_WIDTH = 600
WIN_HEIGHT = 600

def import_enote_items_struct()->{}:
    tk.Tk().withdraw()
    filename = askopenfilename()
    encrypted_data = read_enote_file(filename,username="aa",password="bb")
    return  get_enote_items(encrypted_data)
    
def pack_enote_items(items:[{}]):
    id = f"{uuid.uuid1()}"
    dict2 = []
    for dict in items:
        dict4 = {}
        for key in dict:
            dict4[key] = dict[key]
        dict3 = {"id":f"{uuid.uuid1()}","item":dict4}
        dict2.append(dict3)
    ss = {"id":id,"items":dict2}
    #print(ss)
    return ss

def get_enote_items(data)-> [{str:str}]:
    enote_items = []
    for key in data:
        if key == "id":
            id_enote = data[key]
        else:
            for dict in data[key]:
                enote_items.append(dict["item"])
        
        
        
    return enote_items  

def read_enote_file(filename, username, password):
    try:
        plist = readPlist(filename)
    except (InvalidPlistException, NotBinaryPlistException):
        print("Not a plist:")
    nonce = plist[0][0:12]
    tag = plist[0][-16:]
    ciphertext = plist[0][12:-16]
    pass_word = SHA256.new(b64encode((username + password).encode("utf-8"))).digest()
    cipher = AES.new(pass_word, AES.MODE_GCM, nonce)
    decrypted_cyphertext = cipher.decrypt_and_verify(ciphertext, tag)
    decrypted_data = json.loads(decrypted_cyphertext)
    #print("The size of the dictionary is {} bytes".format(sys.getsizeof(decrypted_data)))
    return decrypted_data
    
def write_enote_items(items,filename, username, password)->bytes:
    gg = pack_enote_items(items)
    data = bytes(json.dumps(gg),"utf-8")
    nonce = os.urandom(12)
    pass_word = SHA256.new(b64encode((username + password).encode("utf-8"))).digest()
    cipher = AES.new(pass_word, AES.MODE_GCM, nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    #print(' '.join('{:02d}'.format(x) for x in nonce)) 
    hint = "Kus Memleket numara".encode("utf-8")
    dd = cipher.nonce + ciphertext + tag
    encrypted_data = [dd,hint]
    try:
        writePlist(encrypted_data, filename)
    except(InvalidPlistException, NotBinaryPlistException):
        print("Not a plist:")



    return encrypted_data
    


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



items = import_enote_items_struct()
write_enote_items(items, "dummy.enote", "aa", "bb")
read_enote_file("dummy.enote", "aa", "bb")
# for item in items:
#     for key in item:
#         print(f"{key} = {item[key]} \n")
#print(pack_enote_items(items))

root.mainloop()
