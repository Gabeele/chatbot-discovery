import socket

# Server address and port
server_address = ('localhost', 3001)

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to the server
    client_socket.connect(server_address)
    print('Connected to the server.')

    while True:
        # Send message to the server
        message = input('Enter your message: ')
        client_socket.sendall(message.encode())

        # Receive response from the server
        response = client_socket.recv(1024).decode()
        print('Server response:', response)

        # Check if the conversation is over
        if response.lower() == 'bye':
            break

except ConnectionRefusedError:
    print('Connection refused. Make sure the server is running.')

finally:
    # Close the socket
    client_socket.close()
    print('Connection closed.')