import socket

def generate_response(data):
    # Example response generation based on the received data
    # You can customize this function as needed
    return f"Echo: {data}"

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to a specific address and port
    server_socket.bind(('localhost', 3001))

    # Listen for incoming connections
    server_socket.listen(1)
    print('Server listening on port 3001...')

    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print(f'Connected to client: {client_address}')

        while True:
            # Receive data from the client
            data = client_socket.recv(1024).decode('utf-8')
            print(f'Received data: {data}')

            # Check if the received data is the "bye" message
            if data.lower() == 'bye':
                print('Received "bye" from client. Closing connection...')
                break  # Exit the inner loop to close the connection

            # Generate a response based on the received data
            response = generate_response(data)

            # Send the response back to the client
            client_socket.sendall(response.encode('utf-8'))

        # Close the client socket after receiving "bye"
        client_socket.close()
        print('Waiting for new client...')

# Start the server
start_server()
