import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


server_socket.bind(('localhost', 8000))


server_socket.listen(1)
print("Server is listening...")


conn, addr = server_socket.accept()
print(f"Connected to {addr}")

try:
    # use r with encode and rb without encode
    data  = conn.recv(1024)
    print("data from client : ",data)
    with open('sample.txt', 'r') as file:
        data = file.read().encode()
        conn.sendall(data)

    print("File sent successfully.")
except Exception as e:
    print(e)
finally:
    conn.close()
    server_socket.close()
    print("connection closed")
