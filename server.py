import socket
from _thread import *
from game import Game
import pickle

server = "192.168.0.102"
port = 5546

# Create a socket object for TCP/IP communication
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Try to bind the socket to the specified server and port
try:
    s.bind((server, port))
except socket.error as e:
    str(e)  # Handle binding errors

# Start listening for incoming connections, with a backlog of 2 connections
s.listen(2)
print("Waiting for a connection, Server Started")

# Initialize a set to keep track of connected clients
connected = set()
# Dictionary to store game instances with their IDs
games = {}
# Counter for player IDs
idCount = 0

# Handle client connections in a separate thread
def threaded_client(conn, p, gameId):
    global idCount
    conn.send(str.encode(str(p)))  # Send the player number to the client
    reply = ""

    while True:
        try:
            data = conn.recv(4096).decode()  # Receive data from the client

            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.resetWent()  # Reset game state
                    elif data != "get":
                        game.play(p, data)  # Process the game move

                    reply = game
                    conn.sendall(pickle.dumps(reply))  # Send the updated game state to the client
            else:
                break  # Break if the game ID is not found
        except:
            break  # Break on any exception

    print("Lost connection")
    try:
        del games[gameId]  # Remove the game instance
        print("Closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close()

# Main server loop to accept and handle new connections
while True:
    conn, addr = s.accept()  # Accept a new connection
    print("Connected to: ", addr)

    idCount += 1
    p = 0  # Player number
    gameId = (idCount - 1) // 2  # Calculate game ID based on player count

    if idCount % 2 == 1:  # If odd, create a new game
        games[gameId] = Game(gameId)
        print("Creating a new game...")
    else:  # If even, set the game as ready and assign player number 1
        games[gameId].ready = True
        p = 1

    # Start a new thread for the client connection
    start_new_thread(threaded_client, (conn, p, gameId))
