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
        except ValueError:
            print("An integer was not correctly inputted for the n_port, please input an integer")
            return 0
        except:
            print("Some other error has occured, restart the server")
        break
        
    if (n_port < 1024):
        print("You have entered a port number for the TCP handshake which is smaller than 1024. \
                  Port numbers smaller than 1024 are already reserved, please enter a proper port number")
        return 0
    elif (n_port > 65535):
        print("Port numbers larger than 65535 do not exist, please enter a proper port number")
        return 0

    # Below while loop reads the req_code inputted into the command line
    while True:
        try:
            int(sys.argv[2])
            # sys.argv[2] is the third command line input which is the req_code

            # Need to check that an integer was actually inputted into the command line before
            # before we assign it as the request code
            
        except ValueError:
            print("An integer was not correctly inputted for the req_code, please input an integer")
            return 0
        except MemoryError:
            print("Value inputted was too large or too small and caused an integer overflow")
            return 0
        except:
            print("Some other error has occured")
        req_code_server = sys.argv[2]
        break
    
    
    # Create a TCP socket for negotiation
    server_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF.INET refers to the IPV4 address family
    # SOCK_STREAM is connection-oriented and used for TCP connections

    # Need to check if n_port is a port that is open
    try:
        server_tcp_socket.bind((server_address, n_port))
    # bind() assigns an IP address and a port number to a socket instance
    except OSError as e:
        if e.errno == 98:  # errno 98 is 'Address already in use'
            print("The port chosen for negotiation is already in use, \
                   restart the server choosing an appropiate port")
            return False
        else:
            raise

    server_tcp_socket.listen(1)

    addresses = socket.getaddrinfo(server_address, None)
    r_port = random.choice(addresses)[4][1]
    # Above finds a random port for transaction not in use

    print(r_port)

    print(1)

    # Accept client connection
    while True:
        # The accept() accepts an incoming connection request from a TCP client.
        connectionSocket, addr = server_tcp_socket.accept()

        # Receive request code from client
        req_code_client = connectionSocket.recv(1024).decode()
        # receives at most 1024 bytes from the client
        # decode() converts the byte object to a string object
        
        if req_code_client == req_code_server:
            # Send random port number to client
            connectionSocket.send(str(r_port).encode())
            # Converts r_port to string which is necessary because integers can't be sent through sockets

            connectionSocket.close()
            server_tcp_socket.close()
            print("TCP socket has been closed")
            break
        else:
            print("The request code from the client was incorrect, please state the correct request code")
            connectionSocket.close()
            # In this instance only the TCP client socket connection closes meaning the TCP server waits until
            # it recieves a proper request code from the TCP client before closing it's connection
            continue
    
    print(2)
        
    # Create a UDP socket for transaction
    server_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # SOCK_DGRAM provides datagrams, which are connectionless messages of a fixed maximum length
    # which is what UDP protocol uses
    
    server_udp_socket.bind((server_address, r_port))
    # The port number for the UDP socket is binded to r_port

    print(3)

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


reverse_string_server()
