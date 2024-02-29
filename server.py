import socket
import random
import sys

# Make sure you run this file before running client.py as mentioned in README.txt!

def reverse_string_server():

    # sys.argv[0] will simply just be the file name

    # Define server address and ports
    server_address = 'localhost'

    # Below while loop checks the n_port inputted into the command line
    # n_port = negotiation port for TCP handshake between client and server
    while True:
        try:
            n_port = int(sys.argv[1]) 
            # sys.argv[1] is the second command line argument
        except TypeError:
            print("An integer was not correctly inputted for the n_port, please input an integer")
            return 0
        if (n_port < 1024):
            print("You have entered a port number for the TCP handshake which is smaller than 1024. \
                  Port numbers smaller than 1024 are already reserved")
            return 0
        elif (n_port > 65535):
            print("Port numbers larger than 65535 do not exist")
            return 0
        else:
            break

    # Below while loop reads the req_code inputted into the command line
    while True:
        try:
            int(sys.argv[2])
            # sys.argv[2] is the third command line input which is the req_code

            # Need to check that an integer was actually inputted into the command line before
            # before we assign it as the request code
            
        except TypeError:
            print("An integer was not correctly inputted for the req_code, please input an integer")
            return 0
        except ValueError:
            print("Value inputted was too large or too small and caused an integer overflow")
            return 0
        req_code_server = sys.argv[2]
        break


    
    r_port = random.randint(1024, 65535)  # Random port for transaction
    # ports 0-1023 are already reserved for other transport protocol purposes
    # The maximum port number value for UDP and TCP protocols is 65, 535
    
    # Create a TCP socket for negotiation
    server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF.INET refers to the IPV4 address family
    # SOCK_STREAM is connection-oriented and used for TCP connections

    server_tcp_socket.bind((server_address, n_port))
    # bind() assigns an IP address and a port number to a socket instance

    server_tcp_socket.listen(1)
    ## listen() makes a socket ready for accepting connections.
    
    # Accept client connection
    while True:
        # The accept() accepts an incoming connection request from a TCP client.
        connectionSocket, addr = server_tcp_socket.accept()

        # Receive request code from client
        req_code_client = connectionSocket.recv(1024).decode()
        # receives at most 1024 bytes from the client
        # decode() converts the byte object to a string object
        
        # Check if request code matches
        if req_code_client == req_code_server:
            # Send random port number to client
            connectionSocket.send(str(r_port).encode())
            # Converts r_port to string which is necessary because integers can't be sent through sockets

            connectionSocket.close()
            server_tcp_socket.close()
            break
        else:
            print("The request code from the client was incorrect, please state the correct request code")
            connectionSocket.close()
            # In this instance only the TCP client socket connection closes meaning the TCP server waits until
            # it recieves a proper request code from the TCP client before closing it's connection
            continue
        
    # Create a UDP socket for transaction
    server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # SOCK_DGRAM provides datagrams, which are connectionless messages of a fixed maximum length
    # which is what UDP protocol uses
    
    server_udp_socket.bind((server_address, r_port))
    # The port number for the UDP socket is binded to r_port

    while True:
        # Receive message from client
        msg, client_address = server_udp_socket.recvfrom(1024)
        # Message recieved from client can onyl have a maximum amount of 1024 bytes
        
        # Reverse the message
        reversed_msg = msg[::-1]
        
        # Send reversed message back to client
        server_udp_socket.sendto(reversed_msg, client_address)
        # sendto() used for TCP connection
        # The UDP socket does not need to close
