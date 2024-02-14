import socket
import select

# Server configuration
HOST = '127.0.0.1'  # Loopback address
PORT = 12345        # Port to listen on

# Create socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the address and port
server_socket.bind((HOST, PORT))

# Listen for incoming connections
server_socket.listen(5)
print(f"Server listening on {HOST}:{PORT}")

# List to keep track of socket objects
sockets_list = [server_socket]

# Dictionary to keep track of connected clients
clients = {}

# Function to broadcast message to all connected clients
def broadcast_message(sender_socket, message):
    for client_socket in clients:
        if client_socket != sender_socket:
            try:
                client_socket.sendall(message)
            except:
                client_socket.close()
                del clients[client_socket]
                sockets_list.remove(client_socket)

while True:
    # Use select to wait for input/output events on sockets
    read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list)

    # Iterate through readable sockets
    for notified_socket in read_sockets:
        # If the notified socket is the server socket, it means a new connection
        if notified_socket == server_socket:
            client_socket, client_address = server_socket.accept()
            print(f"Accepted connection from {client_address}")

            # Add the new client socket to the list of sockets
            sockets_list.append(client_socket)

            # Add the new client socket to the dictionary of clients
            clients[client_socket] = client_address

            # Send a welcome message to the new client
            client_socket.sendall("Welcome to the chat room!\n".encode())

            # Broadcast to other clients that a new client has joined
            broadcast_message(client_socket, f"{client_address[0]} has joined the chat!\n".encode())

        # If the notified socket is a client socket, it means a new message from a client
        else:
            message = notified_socket.recv(1024)
            if message:
                # Broadcast the message to all clients
                broadcast_message(notified_socket, f"{clients[notified_socket][0]}: {message.decode()}\n".encode())
            else:
                # If there is no message, it means the client has disconnected
                print(f"Closed connection from {clients[notified_socket]}")
                sockets_list.remove(notified_socket)
                del clients[notified_socket]

    # Handle any exceptional conditions
    for notified_socket in exception_sockets:
        print(f"Exceptional condition from {clients[notified_socket]}")
        sockets_list.remove(notified_socket)
        del clients[notified_socket]
        notified_socket.close()
