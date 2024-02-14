import socket
import threading

# Function to handle receiving messages from the client
def receive_messages(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            if not message:
                print(f"Client at {address} disconnected.")
                break
            print(f"Client at {address}: {message}")
        except:
            print(f"Error receiving message from client at {address}")
            break

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

# Accept incoming connections and handle them in separate threads
while True:
    client_socket, address = server_socket.accept()
    print(f"Accepted connection from {address}")
    
    # Create thread to receive messages from client
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket, address))
    receive_thread.start()
    
    # Send messages to client
    while True:
        try:
            message = input("Server: ")
            if message.lower() == 'bye':
                client_socket.sendall("Server disconnected.".encode())
                client_socket.close()
                break
            client_socket.sendall(message.encode())
        except:
            print("Error sending message to client.")
            break
