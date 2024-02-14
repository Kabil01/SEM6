import socket

# Client configuration
HOST = '127.0.0.1'  # Server's IP address
PORT = 12345        # Port server is listening on

# Connect to the server
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print("Connected to server.")

while True:
    # Send message to server
    message = input("Client: ")
    client_socket.sendall(message.encode())

    # Receive message from server
    received_data = client_socket.recv(1024).decode()
    print(f"Server: {received_data}")

    if received_data.lower() == 'bye':
        break

# Close the connection
client_socket.close()
