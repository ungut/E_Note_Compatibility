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
from tkinter.ttk import Style
from tkinter import Menu
from tkinter import Label
from tkinter import StringVar
from tkinter import Entry

from fpdf import FPDF
import unicodedata
import atexit

BG_COLOR = "#346466"
WIN_WIDTH = 600
WIN_HEIGHT = 800
class MyDialog(tk.simpledialog.Dialog):

    def body(self, master):

        Label(master, text="Username:").grid(row=0)
        Label(master, text="Password:").grid(row=1)

        self.e1 = Entry(master,show="*")
        self.e2 = Entry(master,show="*")

        self.e1.grid(row=0, column=1)
        self.e2.grid(row=1, column=1)
        return self.e1 # initial focus

    def apply(self):
        global username_and_password
        first = self.e1.get()
        second = self.e2.get()
        username_and_password = f"{first}{second}"


class items_data:
    items = []
    items0 = []
    def set_initial_values(self,items_in):
        self.items0 = []
        self.items = items_in[::]
        for ii in range(len(items_in)):
            sd = {}
            for key in items_in[ii]:
                value = items_in[ii][key]
                sd[key] = value
                
            self.items0.append(sd)
 

    def set_items(self,index,key,value):
        self.items[index][key] = value


    def set_items0(self,index,key,value):
        self.items0[index][key] = value

    def is_changed(self):
        bay = len([i for i in self.items if i not in self.items0]) != 0
        return bay 

        

data_class = items_data()

def login_verification():
    pass
 

def import_enote_items_struct() -> {}:
    tk.Tk().withdraw()
    global filename
    filename = askopenfilename()
    hint = read_hint(filename)
    if hint != "-1":
        tk.Tk().withdraw()
        d = MyDialog(root)
        #print (username_and_password)
        #username = tk.simpledialog.askstring("Username", "Enter username:", show='*')
        #password = tk.simpledialog.askstring("Password", "Enter password:", show='*')

    encrypted_data = read_enote_file(filename,passdata= username_and_password)
    return get_enote_items(encrypted_data)


def pack_enote_items(items: [{}]):
    id = f"{uuid.uuid1()}"
    dict2 = []
    for dict in items:
        dict4 = {}
        for key in dict:
            dict4[key] = dict[key]
        dict3 = {"id": f"{uuid.uuid1()}", "item": dict4}
        dict2.append(dict3)
    ss = {"id": id, "items": dict2}
    # print(ss)
    return ss


def get_enote_items(data) -> [{str: str}]:
    enote_items = []
    for key in data:
        if key == "id":
            id_enote = data[key]
        else:
            for dict in data[key]:
                enote_items.append(dict["item"])

    return enote_items

def read_hint(filename)->str:
        try:
            plist = readPlist(filename)
            if len(plist) > 1:
                hint_data = plist[1]
                return str(hint_data,encoding="utf-8")
            else:
                return ""
        except (InvalidPlistException, NotBinaryPlistException):
            return "-1"


def read_enote_file(filename, passdata):
    try:
        plist = readPlist(filename)
    except (InvalidPlistException, NotBinaryPlistException):
        print("Not a plist:")
    nonce = plist[0][0:12]
    tag = plist[0][-16:]
    ciphertext = plist[0][12:-16]
    pass_word = SHA256.new(b64encode((passdata).encode("utf-8"))).digest()
    cipher = AES.new(pass_word, AES.MODE_GCM, nonce)
    decrypted_cyphertext = cipher.decrypt_and_verify(ciphertext, tag)
    decrypted_data = json.loads(decrypted_cyphertext)
    # print("The size of the dictionary is {} bytes".format(sys.getsizeof(decrypted_data)))
    return decrypted_data


def write_enote_items(items, filename, passdata) -> bytes:
    gg = pack_enote_items(items)
    data = bytes(json.dumps(gg), "utf-8")
    nonce = os.urandom(12)
    pass_word = SHA256.new(b64encode((passdata).encode("utf-8"))).digest()
    cipher = AES.new(pass_word, AES.MODE_GCM, nonce)
    ciphertext, tag = cipher.encrypt_and_digest(data)
    # print(' '.join('{:02d}'.format(x) for x in nonce))
    hint = "Kus Memleket numara".encode("utf-8")
    dd = cipher.nonce + ciphertext + tag
    encrypted_data = [dd, hint]
    try:
        writePlist(encrypted_data, filename)
    except (InvalidPlistException, NotBinaryPlistException):
        print("Not a plist:")

    return encrypted_data


 




root = tk.Tk()
root.title("Enote")
root.eval("tk::PlaceWindow . center")

# çreate a Canvas
master_frame = tk.Frame(root, width=WIN_WIDTH / 3, height=WIN_HEIGHT, bg=BG_COLOR)
master_frame.pack(side="left", fill="y", expand=0)
master_frame.pack_propagate(False)

detail_frame = tk.Frame(
    root,
    width=WIN_WIDTH,
    height=WIN_HEIGHT,
    bg=BG_COLOR,
    highlightbackground="green",
    highlightthickness=2,
)

detail_frame.pack_propagate(False)
detail_frame.pack(side="right", fill="both", expand="yes")
master_canvas = tk.Canvas(master_frame)
detail_canvas = tk.Canvas(detail_frame)
master_canvas.pack(side="left", fill="both", expand=1)
detail_canvas.pack(side="left", fill="both", expand=1)

# Add A Scrollbar To The Canvas
master_scrollbar = ttk.Scrollbar(root, orient="vertical", command=master_canvas.yview)
master_scrollbar.pack(side="right", fill="y", padx=10, pady=10)
detail_scrollbar = ttk.Scrollbar(
    detail_frame, orient="vertical", command=detail_canvas.yview
)
detail_scrollbar.pack(side="right", fill="y", padx=10, pady=10)

# Configure The Canvas
master_canvas.configure(yscrollcommand=master_scrollbar.set)
master_canvas.bind(
    "<Configure>",
    lambda e: master_canvas.configure(scrollregion=master_canvas.bbox("all")),
)
detail_canvas.configure(yscrollcommand=detail_scrollbar.set)
detail_canvas.bind(
    "<Configure>",
    lambda e: detail_canvas.configure(scrollregion=detail_canvas.bbox("all")),
)

# Create A Second Frame INSIADE The Canvas
second_frame = tk.Frame(master_canvas)
second_detail_frame = tk.Frame(detail_canvas)
# Add That Frame To a Window In The Canvas
master_canvas.create_window((0, 0), window=second_frame, anchor="nw")
detail_canvas.create_window((0, 0), window=second_detail_frame, anchor="nw")

img = Image.open("Icon1024.jpeg")
resized_image = img.resize((30, 30), Image.LANCZOS)
logo_image = ImageTk.PhotoImage(resized_image)
logo_widget = tk.Label(master_frame, image=logo_image, bg="#346466")
logo_widget.image = logo_image
# logo_widget.pack(anchor="w")


def set_detail_Viev(index):
    for widgets in second_detail_frame.winfo_children():
        widgets.destroy()
    items = data_class.items
    for key in items[index]:
        nn = 0
        i = 0
        def text_edit(e):
            k_key = str(e.widget).split('.')[-1][1:]
            new_value = f"{e.widget.get('1.0','end')}"
            if items[index][k_key] is not  new_value:
                data_class.set_items(index=index, key=k_key, value=new_value)
                write_enote_items(data_class.items, filename, passdata=username_and_password)
 

        match key:
            case "Title":
                i = 0
            case "URL":
                i = 1
            case "UserName":
                i = 2
            case "Password":
                i = 3
            case "PIN":
                i = 4
            case "Parola":
                i = 5
            case "Notes":
                i = 6
            case _:
                i = nn + 7
                nn += 1
        text = data_class.items[index][key]
        height = text.splitlines()
        w = tk.Text(second_detail_frame, borderwidth=3, font=("TkHeadingFont", 15),name=f"n{key}")
        w.config(height=max(3, len(height)))
        w.insert(1.0, text)
        w.grid(row=i, column=1, sticky="nwse", columnspan=10)
        tk.Label(second_detail_frame, text=key).grid(row=i, column=0, sticky="w")
        w.bind('<FocusOut>',lambda e:text_edit(e))


def generate_master_button(item, index):
    text = item["Title"]
    Button(
        second_frame,
        text=text,
        width=(master_frame.winfo_width() - 10),
        anchor="w",
        font=("TkHeadingFont", 15),
        bg="#28393a",
        fg="white",
        cursor="hand2",
        activebackground="#badee2",
        activeforeground="black",
        command=lambda: set_detail_Viev(index),
    ).grid(row=index + 2, column=0, sticky="w", pady=5)


def convert_to_pdf():
    # save FPDF() class into a
    # variable pdf
    pdf = FPDF(format="a4",unit="mm")

    # Add a page
    pdf.add_page()

    # set style and size of font
    # that you want in the pdf
    pdf.set_font("Times", size=15)
    epw = pdf.w - 2*pdf.l_margin
    text_height = 15
    for index, item in enumerate(items):
        items_text = []

        for key in item:
            nn = 0
            i = 0
            match key:
                case "Title":
                    i = 0

                case "URL":
                    i = 1
                case "UserName":
                    i = 2
                case "Password":
                    i = 3
                case "PIN":
                    i = 4
                case "Parola":
                    i = 5
                case "Notes":
                    i = 6
                case _:
                    i = nn + 7
                    nn += 1
            items_text.insert(i, (key,item[key]))

        for text in items_text: 
            text1 = f"{text[0].encode('latin-1', 'replace').decode('latin-1')}"
            text2 = f"{text[1].encode('latin-1', 'replace').decode('latin-1')}"
 
            if pdf.y + text_height > pdf.page_break_trigger:
                pdf.add_page()
            top = pdf.y
 
            offset = pdf.x + 40
            pdf.set_text_color(194,8,8)
            pdf.set_font('',style='BU')
            pdf.multi_cell(
                w=100,
                h=text_height,
                txt= text1,
                border=0,
                align="L",
                fill=False,
            )
            pdf.set_text_color(0,0,0)
            pdf.set_font('')
            pdf.set_font('',style="")

            pdf.y = top

            # Move to computed offset
            pdf.x = offset 
            pdf.multi_cell(
            w=160, 
            h=text_height,
            txt= text2,
            border=1,
            align="L",
            fill=False,
            )
        pdf.multi_cell(
        w=210,
        h=10,
        txt= "\n\n",
        border=0,
        align="L",
        fill=False,
    )


    pdf.output("GFG.pdf")

def my_exit_function():
    print("hello")

def open_file():
    items = import_enote_items_struct()
    data_class.set_initial_values(items)
    update_master_view()

menubar = Menu(root)
file = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='File', menu = file)
file.add_command(label ='New File', command = None)
file.add_command(label ='Open...', command = lambda: open_file())
file.add_command(label ='Save', command = None)
file.add_separator()


def exiting_app():
    if  data_class.is_changed() == False:
        root.destroy()
    else:
        if tk.messagebox.askyesno("Save Changes", "Save changes to the file?"):
            items = data_class.items
            write_enote_items(items, filename,passdata=username_and_password)
            data_class.set_initial_values(items)
            return
        else:
            root.destroy()
    
  
file.add_command(label ='Exit', command = exiting_app)

# Adding Edit Menu and commands
edit = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Edit', menu = edit)
edit.add_command(label ='Undo', command = None)
edit.add_command(label ='Redo', command = None)
edit.add_command(label ='Cut', command = None)
edit.add_command(label ='Copy', command = None)
edit.add_command(label ='Paste', command = None)
edit.add_command(label ='Select All', command = None)
edit.add_separator()
edit.add_command(label ='Find...', command = None)
# edit.add_command(label ='Find again', command = None)
  
# Adding Help Menu
help_ = Menu(menubar, tearoff = 0)
menubar.add_cascade(label ='Help', menu = help_)
# help_.add_command(label ='Tk Help', command = None)
# help_.add_command(label ='Demo', command = None)
help_.add_separator()
help_.add_command(label ='About Tk', command = None)
  
# display Menu
root.config(menu = menubar)

def update_master_view():
    for widgets in second_frame.winfo_children():
        widgets.destroy()

    master_buttons = [len(data_class.items)]
    for index, item in enumerate(data_class.items):
        master_buttons.append(generate_master_button(item, index))

if data_class.items == []:
    open_file()
#convert_to_pdf()
# write_enote_items(items, "dummy.enote", "aa", "bb")

root.mainloop()
