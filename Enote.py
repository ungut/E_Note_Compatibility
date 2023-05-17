from biplist import *
import os
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256
from base64 import b64encode
import tkinter as tk
import tkinter as ttk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import json
import uuid
import sys
from tkmacosx import Button
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

#çreate a Canvas
master_frame = tk.Frame(root, width=WIN_WIDTH / 3, height=WIN_HEIGHT, bg=BG_COLOR)
master_frame.pack(side="left", fill="y", expand=0)
master_frame.pack_propagate(False)

master_canvas = tk.Canvas(master_frame)
master_canvas.pack(side="left",fill="both",expand=1)

#Add A Scrollbar To The Canvas
master_scrollbar =  ttk.Scrollbar(root,orient="vertical",command=master_canvas.yview,bg=BG_COLOR)
master_scrollbar.pack(side="left",fill="y")

#Configure The Canvas
master_canvas.configure(yscrollcommand=master_scrollbar.set)
master_canvas.bind("<Configure>",lambda e:  master_canvas.configure(scrollregion=master_canvas.bbox("all")))

#Create A Second Frame INSIADE The Canvas
second_frame = tk.Frame(master_canvas)

#Add That Frame To a Window In The Canvas
master_canvas.create_window((0,0),window=second_frame,anchor="nw")



detail_frame = tk.Frame(
    root,
    width=WIN_WIDTH,
    height=WIN_HEIGHT,
    bg=BG_COLOR,
    highlightbackground="green",
    highlightthickness=2,
)
def load_detail_frame():
    print("hello")


detail_frame.pack(side="left",fill="both",expand="yes")
detail_frame.pack_propagate(False)


img = Image.open("Icon1024.jpeg")
resized_image = img.resize((30, 30), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(resized_image)
logo_widget = tk.Label(master_frame, image=logo_image, bg="#346466")
logo_widget.image = logo_image
#logo_widget.pack(anchor="w")
def generate_master_view(items):
    for i,item in enumerate(items):
        text = item["Title"]
        Button(
            second_frame,
            text= text,
            width=(master_frame.winfo_width()-10),
            anchor="w",
            font=("TkHeadingFont",15),
            bg="#28393a",
            fg="white",
            cursor="hand2",
            activebackground="#badee2",
            activeforeground="black",
            command = lambda: load_detail_frame()
        ).grid(row=i+2,column=0,sticky="w",pady=5)



items = import_enote_items_struct()
generate_master_view(items)
#write_enote_items(items, "dummy.enote", "aa", "bb")
#  read_enote_file("dummy.enote", "aa", "bb")
# for item in items:
#     for key in item:
#         print(f"{key} = {item[key]} \n")
#print(pack_enote_items(items))

root.mainloop()
