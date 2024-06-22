import socket
import pickle

class Network:
    def __init__(self):
        # Initialize the client socket for TCP/IP communication
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Define the server address and port
        self.server = "192.168.0.102"
        self.port = 5546
        self.addr = (self.server, self.port)
        # Connect to the server and get the player number
        self.p = self.connect()

    def getP(self):
        # Return the player number
        return self.p

    def connect(self):
        try:
            # Attempt to connect to the server
            self.client.connect(self.addr)
            # Receive and return the player number from the server
            return self.client.recv(2048).decode()
        except:
            pass  # Handle connection errors silently

    def send(self, data):
        try:
            # Send data to the server
            self.client.send(str.encode(data))
            # Receive and return the response from the server (deserialized)
            return pickle.loads(self.client.recv(2048))
        except socket.error as e:
            # Print any socket errors
            print(e)
