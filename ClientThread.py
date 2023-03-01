import threading


class ClientThread(threading.Thread):
    def __init__(self, clientAddress, clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        self.clientAddress = clientAddress
        print("New connection added: ", clientAddress)

    def run(self):
        print("Connection from : ", self.clientAddress)
        # self.csocket.send(bytes("Hi, This is from Server..",'utf-8'))
        msg = ""
        while True:
            data = self.csocket.recv(2048)
            msg = data.decode()
            if msg == "bye":
                break
            print("from client", msg)
            self.csocket.send(bytes(msg, "UTF-16"))
        print("Client at ", self.clientAddress, " disconnected...")
