import socket
import threading

# Client configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12345        # Port server is listening on

# Function to handle receiving messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except Exception as e:
            print("Error receiving message from server:", e)
            break

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to server.")

# Start thread to receive messages from server
receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
receive_thread.start()

# Send messages to server
while True:
    try:
        message = input()
        client_socket.sendall(message.encode())
        if message.lower() == 'bye':
            break
    except Exception as e:
        print("Error sending message to server:", e)
        break

# Close the connection
client_socket.close()
