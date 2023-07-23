import tkinter as tk
import tkinter.font as tkFont
import smtplib
import socket
import time
from Crypto.Cipher import AES
import os, random, struct
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from EncryptionandDecryption import encrypt_file
class App:
    sender = "18p7298@eng.asu.edu.eg"
    password = "islvfmh2015" # 
    tovar=""
    us=""
    rs=""
    sk=""
    def __init__(self, root):
        #setting title
        self.to_var=tk.StringVar()
        root.title("Secure Mail Composer")
        #setting window size
        width=600
        height=500
        screenwidth = root.winfo_screenwidth()
        screenheight = root.winfo_screenheight()
        alignstr = '%dx%d+%d+%d' % (width, height, (screenwidth - width) / 2,
        (screenheight - height) / 2)
        root.geometry(alignstr)
        root.resizable(width=False, height=False)
        ft = tkFont.Font(family='Times',size=12)
        label_To=tk.Label(root)
        label_To["font"] = ft
        label_To["fg"] = "#333333"
        label_To["justify"] = "right"
        label_To["text"] = "To:"
        label_To.place(x=40,y=40,width=70,height=25)
        label_Subject=tk.Label(root)
        label_Subject["font"] = ft
        label_Subject["fg"] = "#333333"
        label_Subject["justify"] = "right"
        label_Subject["text"] = "Subject:"
        label_Subject.place(x=40,y=90,width=70,height=25)
        self.email_To=tk.Entry(root, textvariable = self.to_var)
        self.email_To["borderwidth"] = "1px"
        self.email_To["font"] = ft
        self.email_To["fg"] = "#333333"
        self.email_To["justify"] = "left"
        self.email_To["text"] = "To"
        self.email_To.place(x=120,y=40,width=420,height=30)
        self.email_Subject=tk.Entry(root)
        self.email_Subject["borderwidth"] = "1px"
        self.email_Subject["font"] = ft
        self.email_Subject["fg"] = "#333333"
        self.email_Subject["justify"] = "left"
        self.email_Subject["text"] = "Subject"
        self.email_Subject.place(x=120,y=90,width=417,height=30)
        self.email_Body=tk.Text(root)
        self.email_Body["borderwidth"] = "1px"
        self.email_Body["font"] = ft
        self.email_Body["fg"] = "#333333"
        self.email_Body.place(x=50,y=140,width=500,height=302)
        button_Send=tk.Button(root)
        button_Send["bg"] = "#f0f0f0"
        button_Send["font"] = ft
        button_Send["fg"] = "#000000"
        button_Send["justify"] = "center"
        button_Send["text"] = "Send"
        button_Send.place(x=470,y=460,width=70,height=25)
        button_Send["command"] = self.button_Send_command
    def send_email(self, subject, body,attach, recipients):
        """
        Sends an encrypted email with attachments to the specified recipients
        :param subject: The subject of the email
        :param body: The body of the email
        :param attach: The User's Key
        :param recipients: The email addresses of the recipients
        """
        # Connect to KDS on localhost:10000 to get encrypted keys
        self.connect_to_kds(10000,self.sender,recipients)
        dec = AES.new(attach.encode('utf-8'), AES.MODE_ECB)
        self.sk=dec.decrypt(self.us)
        print("Secret key:")
        print(self.sk)
        # Add the receiver's secret key to a file named wrappedkey.txt
        with open("wrappedkey.txt","wb") as f:
            f.write(self.rs)
        # let it read the receiver's secret key from the wrappedkey.txt
        with open("wrappedkey.txt","rb") as f:
            key=f.read()
        # write the main body content of the e-mail and encrypt it using the secret key 
        with open("body.txt","wb") as f:
            f.write(body.encode("utf-8"))
        encrypt_file(self.sk,"body.txt","RealMessageBody.txt")
        with open("RealMessageBody.txt","rb") as f:
            file_contents = f.read()
        os.remove("body.txt")
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = recipients
        msg.attach(MIMEText("The encrypted message is the file's real message.txt", 'plain'))
        part = MIMEApplication(file_contents)
        part['Content-Disposition'] = f'attachment; filename={os.path.basename("RealMessageBody.txt")}'
        msg.attach(part)
        part=MIMEApplication(key)
        part['Content-Disposition'] = f'attachment; filename={os.path.basename("wrappedkey.txt")}'
        part['Content-Disposition']='attachment; filename=wrappedkey.txt'
        msg.attach(part)
        # Connect to the SMTP server and send the email
        smtp_server = smtplib.SMTP("smtp-mail.outlook.com", port=587)
        print("Connected")
        smtp_server.starttls()
        print("TLS OK")
        smtp_server.login(self.sender, self.password)
        print("login OK")
        smtp_server.sendmail(self.sender, recipients, msg.as_string())
        print("mail sent")
        smtp_server.quit()


    def button_Send_command(self):
        tovar=self.email_To.get()
        print(tovar)
        subject = self.email_Subject.get()
        body = self.email_Body.get("1.0","end")
        att='3ba2bc5c12f58381022cff3773896b4a'
        self.send_email(subject, body,att, tovar)

    def connect_to_kds(self,port,userEmail,recepientEmail):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('localhost', port)
        key_rec=False
        try:
            client_socket.connect(server_address)
            print("Connected to port", port)
            data=client_socket.recv(2048)
            client_socket.send(userEmail.encode('utf-8'))
            time.sleep(1)
            client_socket.send(recepientEmail.encode('utf-8'))
            ctr=0
            while not key_rec:
                data=client_socket.recv(2048)
                if ctr==0:
                    print(data)
                    self.us=data
                    ctr+=1
                elif ctr==1:
                    print(data)
                    self.rs=data
                    key_rec=True
            # Close the connection
            client_socket.close()
            print("Connection aborted")
        except ConnectionRefusedError:
            print("Connection error...Please try again on your server.")
            
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
