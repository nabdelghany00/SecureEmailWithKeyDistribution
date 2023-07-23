import socket, threading
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
class ClientThread(threading.Thread):
    
    masterKeys={"18P5806@eng.asu.edu.eg": "e2573b16e5b4daff43518071eef73282",
                "18P1789@eng.asu.edu.eg":"2e6f8b1c5a5477974de88122f2fa53f8",
                "18p7298@eng.asu.edu.eg":"3ba2bc5c12f58381022cff3773896b4a"}
    

    def __init__(self,ip,port,clientsocket):
        threading.Thread.__init__(self)

        self.ip = ip
        self.port = port

        self.csocket = clientsocket

        print ("[+] New thread started for ",ip,":",str(port))
    def run(self):
        print ("Connection from : ",ip,":",str(port))
        clientsock.send("Welcome to the multi-thraeded server".encode())

        data = "dummydata"

        ictr=0
        while len(data):
            if ictr==0:
                mail = self.csocket.recv(2048).decode()
                sk = self.generateSecret()

                uk = self.getKey(mail)

                ciphertxt = self.encrypt_message( uk.encode(),sk)


                self.csocket.send(ciphertxt)
                print("Client Secret Key Sent:",ciphertxt)
                ictr+=1


            elif ictr==1:
                recepientEmail = self.csocket.recv(2048).decode()
                recepientKey =self.getKey(recepientEmail)

                ciphertxt = self.encrypt_message(recepientKey.encode(),sk)
                self.csocket.send(ciphertxt)


                print("Client Secret Key Sent:",ciphertxt)
                ictr+=1

            elif ictr==2:

                self.csocket.close()

                print ("Client at ",self.ip," disconnected...")
                data=''
    def getKey(self,email):
        return self.masterKeys[email]
    
    def generateSecret(self):
        return get_random_bytes(16)
    
    def encrypt_message(self,key, message):
        cipher = AES.new(key, AES.MODE_ECB)

        ciphertext = cipher.encrypt(message)
        return ciphertext
    


host = "0.0.0.0"
port = 10000

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

tcpsock.bind((host,port))

while True:
    tcpsock.listen(4)
    print ("Listening for incoming connections...")
    (clientsock, (ip, port)) = tcpsock.accept()
    #pass clientsock to the ClientThread thread object being created
    newthread = ClientThread(ip, port, clientsock)
    newthread.run()