import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client_socket.connect(('localhost', 8000))

try:

    client_socket.sendall(b"Hellow from client")

    file_data = client_socket.recv(1024*1024)

    with open('received_sample.txt', 'ab') as file:
        file.write(file_data)

    print("File received successfully.")
except Exception as e:
    print(e)

finally:
    # 5. Close the socket
    client_socket.close()
    print("Connection closed")
