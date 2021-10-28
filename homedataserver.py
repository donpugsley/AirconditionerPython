import socket
from subprocess import call

# Name of saved figure 
PICFILE = "temp.jpg"

HOST_N = socket.gethostname()
#HOST, PORT = socket.gethostbyname(HOST_N), 18888
HOST, PORT = socket.gethostbyname('192.168.1.203'), 10888

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_IP) 
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print('Serving HomeData using HTTP on port %s ...' % PORT)
while True:
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    option = request.decode().split(' ')
    # print("Request: ", request)

    if option[1]:

        if PICFILE in option[1]: # NEED TO UNDERSTAND THIS

            with open(PICFILE, "r+b") as image_file:
                data = image_file.read()
                HTTP_RESPONSE = b'\r\n'.join([b"HTTP/1.1 200 OK",
                                              b"Connection: close",
                                              b"Cache-Control: max-age=30, must-revalidate",
                                              b"Content-Type: image/jpg",
                                              bytes("Content-Length: %s" % len(data),'utf-8'),
                                              b'', data ] )
                print("Response: ", HTTP_RESPONSE)
                client_connection.sendall(HTTP_RESPONSE) 

        else:

            call(["python", "plot-homelogger-data.py"])
            with open(PICFILE, "r+b") as image_file:
                # encoded_string = base64.b64encode(image_file.read())
                # size = len(encoded_string)

                # HTTP_RESPONSE = "HTTP/1.1 200 OK\n" + "Connection: close\n" + "Content-Type: image/png\n" + "Content-Length: "+ size + "\n\n" + str(encoded_string)

                # client_connection.sendall(HTTP_RESPONSE)
                data = image_file.read()
                HTTP_RESPONSE = b'\r\n'.join([b"HTTP/1.1 200 OK",
                                              b"Connection: close",
                                              b"Cache-Control: max-age=30, must-revalidate"
                                              b"Content-Type: image/jpg",
                                              bytes("Content-Length: %s" % len(data),'utf-8'),
                                              b'', data ] )
                print("Response: ", HTTP_RESPONSE)
                client_connection.sendall(HTTP_RESPONSE) 

    else:
        pass    

    client_connection.close()
    
