import tkinter as tk
from tkinter import filedialog
from Crypto.Cipher import AES
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
import os
from EncryptionandDecryption import decrypt_file

"Modify the variable of the uk (user secret key) to the receiver's"
"which you want to send him the mail"

class FileAttachmentApp:
    def __init__(self):
        "Initializing and setting the secret key of the receiver "

        self.sk=""

        self.uk="2e6f8b1c5a5477974de88122f2fa53f8"

        self.window = tk.Tk()
        self.window.title("File Decryptor")
        self.attachments = []

        self.create_widgets()

        self.message = MIMEMultipart()
        "Initializing a read button to decrypt the ciphertext"
    def create_widgets(self):
        


        readbtn = tk.Button(self.window, text="Read Message", 
        command=self.read_message)


        readbtn.pack(pady=10)

        self.result = tk.Text(self.window, height=10, width=40, 
        state=tk.DISABLED)


        self.result.pack()

        sbar = tk.Scrollbar(self.window)
        sbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.result.config(yscrollcommand=sbar.set)
        sbar.config(command=self.result.yview)

    def read_message(self):
        "Decrypts wrappedkey.txt to get the needed secret key"
        "to decrypt the RealMessageBody.txt"
        self.result.config(state=tk.NORMAL)
        self.result.delete(1.0, tk.END)
        with open("wrappedkey.txt", 'rb') as file:
            encSK = file.read()
            decrypt = AES.new(self.uk.encode('utf-8'), AES.MODE_ECB)
            print(type(encSK))
            self.sk=decrypt.decrypt(encSK)


        decrypt_file(self.sk,"RealMessageBody.txt","DecryptedMessage.txt")
        with open("DecryptedMessage.txt","rb") as f:
            decMsg = f.read()
            self.result.insert(tk.END, decMsg)

            self.result.insert(tk.END, "\n")


            self.result.config(state=tk.DISABLED)
    def run(self):
        self.window.mainloop()


app = FileAttachmentApp()

app.run()
