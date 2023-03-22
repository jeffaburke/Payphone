# Deprecated


import threading


class SocketClientThread(threading.Thread):
    def __init__(self, clientAddress, clientSocket):
        threading.Thread.__init__(self)
        self.csocket = clientSocket
        self.clientAddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", self.clientAddress)
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ""
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == "quit":
                break
            print("from client", msg)
            self.csocket.send(bytes(msg, "UTF-16"))
        print("Client at ", self.clientAddress, " disconnected...")
