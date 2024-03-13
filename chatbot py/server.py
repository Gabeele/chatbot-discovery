import socket
from bot import generate_response, initialize

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(('localhost', 3001))

    server_socket.listen(1)
    print('Server listening on port 3001...')
    
    initialize()

    while True:
        client_socket, client_address = server_socket.accept()
        print(f'Connected to client: {client_address}')

        while True:
            data = client_socket.recv(1024).decode('utf-8')
            print(f'Received data: {data}')
            
            response = generate_response(data)

            client_socket.sendall(response.encode('utf-8'))
            
            if(response.lower() == 'Goodbye!'):
                break

        client_socket.close()
        print('Waiting for new client...')

start_server()
