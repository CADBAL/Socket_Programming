import socket
import sys

# Make sure you run server.py before running client.py as mentioned in README.txt!

def reverse_string_client():

    # sys.argv[0] will simply just be the file name

    # The server address which we are trying to connect to is stated as a command line argument,
    # specifically the second command line argument
    server_address = sys.argv[1]

    # Below while loop checks the n_port inputted into the command line
    # n_port = negotiation port for TCP handshake between client and server
    while True:
        try:
            n_port = int(sys.argv[2])
            # sys.argv[2] is the third command line argument
        except ValueError:
            print("An integer was not correctly inputted for the n_port, please input an integer")
            return 0
        except:
            print("Some other error has occured, restart the server")
        break
        
    if (n_port < 1024):
        print("You have entered a port number for the TCP handshake which is smaller than 1024. \
              Port numbers smaller than 1024 are already reserved")
        return 0
    elif (n_port > 65535):
        print("Port numbers larger than 65535 do not exist")
        return 0

    # Below while loop reads the req_code inputted into the command line
    while True:
        try:
            int(sys.argv[3])
            # sys.argv[3] is the fourth command line argument which is the req_code

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
        req_code_client = sys.argv[3]
        break

    # Create a TCP socket for negotiation
    client_tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # AF.INET refers to the IPV4 address family
    # SOCK_STREAM is connection-oriented and used for TCP connections

    client_tcp_socket.connect((server_address, n_port))
    # Above connects to server_address with the same n_port
    
    #send() is used for TCP connection
    client_tcp_socket.send(req_code_client.encode())
    # Above sends the request code that was stated in the command line and encodes it as bytes
    # UTF-8 is the default encoding
    
    # Receive random port number from server
    r_port = int(client_tcp_socket.recv(1024).decode())
    # recieves at most 1024 bytes from the server
    # decodes() converts the r_port created by the TCP server as byte object to string object

    client_tcp_socket.close()
    
    # Create a UDP socket
    client_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    cmd_msg = sys.argv[4:]
    # Above is the string which is inputted to the command line
    # sys.argv[4:] would create a list ["The", "man", "is", "walking"] if the string inputted was
    # "The man is walking". We start at index 4 since that is when the string starts in the command line
    # Every command line argument is separated by whitespace

    msg = ' '.join(cmd_msg)
    # Above is the string which is going to get sent to the UDP server.

    # Send message to server
    client_udp_socket.sendto(msg.encode(), (server_address, r_port))
    #sendto() used for TCP connection
    
    # Receive reversed message from server
    reversed_msg, server_address = client_udp_socket.recvfrom(1024)
    
    # Print reversed message
    print(f"Reversed Message: {reversed_msg.decode()}")
    
    # Close the UDP socket
    client_udp_socket.close()

reverse_string_client()

