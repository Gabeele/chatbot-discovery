import socket
from query import Query
from actions import request_maintenance



def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 3001))
    server_socket.listen(1)
    print('Server listening on port 3001...')
    
    while True:
        client_socket, client_address = server_socket.accept()
        try:
            print(f'Connected to client: {client_address}')

            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break  # Connection closed by client
                print(f'Received data: {data}')

                query = Query(data, client_address)
                intent = query.determine_intent()

                if intent == "Maintenance Request":
                    # Pass client_socket to request_maintenance() to interact directly with the client
                    request_maintenance(client_socket)
                if intent == "Farewell":
                    client_socket.sendall("Goodbye!".encode('utf-8'))
                    client_socket.close()
                    break
                if intent == "Greeting":
                    client_socket.sendall("Hello! How can I help you today?".encode('utf-8'))
                else:
                    client_socket.sendall("I am not too sure what you are asking for. Please try again or ask for help.".encode('utf-8'))
        finally:
            client_socket.close()
            print('Connection closed, waiting for new client...')

start_server()