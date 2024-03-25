# Title: PyDrop server implementation
# Author: Richard Smith

import socket
import ssl
import os
import signal
import select

class Server:
    def __init__(self, HOST="0.0.0.0", PORT=9090, FILEPATH="./", CERTFILE=None, KEYFILE=None, *args, **kwargs):
        self.HOST = HOST
        self.PORT = PORT
        self.FILEPATH = FILEPATH # Default to current directory
        self.SERVER_SOCKET = None
        self.ALIVE = False
        self.CERTFILE= CERTFILE
        self.KEYFILE = KEYFILE
    
    def unencrypted_server(self):
        # Register signal handler for SIGINT (CTRL+C):
        signal.signal(signal.SIGINT, self.signal_handler)

        # Create server socket:
        self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_SOCKET.bind((self.HOST, self.PORT))
        self.SERVER_SOCKET.listen()
        self.ALIVE = True

        print(f"PyDrop Listening on {self.HOST}:{self.PORT}")

        # Accept incoming connection from client and send file data:
        while self.ALIVE:
            try:
                # Use select.select() to wait for connection with timeout
                readable, _, _ = select.select([self.SERVER_SOCKET], [], [], 1.0)
                if readable:
                    conn, addr = self.SERVER_SOCKET.accept()
                    try:
                        with conn:
                            print(f"Client Connection {addr} Initiated")

                            # Read filename specified by the client
                            filenameLengthBytes = conn.recv(4)
                            filenameLength = int.from_bytes(filenameLengthBytes, byteorder='big')
                            filename = conn.recv(filenameLength).decode()

                            # Check if file exists
                            try:
                                # Open the file and parse the contents
                                with open(filename, "rb") as file:
                                    fileData = file.read()
                            except:
                                print(f"Unable to access file {filename}")
                                continue
                            try:
                                # Send filename length and data to client:
                                conn.sendall(len(filename).to_bytes(4, byteorder='big'))
                                conn.sendall(filename.encode())
                                # Send file data length and file data to client:
                                conn.sendall(len(fileData).to_bytes(8, byteorder='big'))
                                conn.sendall(fileData)

                                print(f"File {filename} Sent Successfully")          
                            except Exception as e:
                                print(e)
                    except Exception as e:
                        print(e)
            except KeyboardInterrupt:
                print("Stopping PyDrop Server...")
                self.stop()

    def encrypted_server(self):
        # Register signal handler for SIGINT (CTRL+C)
        signal.signal(signal.SIGINT, self.signal_handler)

        # Create server socket
        self.SERVER_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER_SOCKET.bind((self.HOST, self.PORT))
        self.SERVER_SOCKET.listen()

        # Wrap server socket with SSL/TLS context
        ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        ssl_context.load_cert_chain(certfile=self.CERTFILE, keyfile=self.KEYFILE)
        
        with ssl_context.wrap_socket(self.SERVER_SOCKET, server_side=True) as ssl_socket:
            self.ALIVE = True
            print(f"PyDrop Listening on {self.HOST}:{self.PORT}")

            # Accept incoming connection from client and send file data:
            while self.ALIVE:
                try:
                    # Used to wait for connection with timeout
                    readable, _, _ = select.select([ssl_socket], [], [], 1.0)
                    if readable:
                        conn, addr = ssl_socket.accept()
                        try:
                            with conn:
                                print(f"Client Connection {addr} Initiated")

                                # Read filename specified by the client
                                filenameLengthBytes = conn.recv(4)
                                filenameLength = int.from_bytes(filenameLengthBytes, byteorder="big")
                                filename = conn.recv(filenameLength).decode()
                                
                                # Check if file exists
                                try:
                                    # Open the file and parse the contents
                                    with open(filename, "rb") as file:
                                        fileData = file.read()
                                except:
                                    print(f"Unable to access file {filename}")
                                    continue
                                try:
                                    # Send filename length and data to client:
                                    conn.sendall(len(filename).to_bytes(4, byteorder="big"))
                                    conn.sendall(filename.encode())
                                    # Send file data length and file data to client:
                                    conn.sendall(len(fileData).to_bytes(8, byteorder="big"))
                                    conn.sendall(fileData)

                                    print(f"File {filename} Sent Successfully")
                                except Exception as e:
                                    print(e)
                        except Exception as e:
                            print(e)
                except KeyboardInterrupt:
                    print("Stopping TLS Server...")
                    self.stop()

    def signal_handler(self, sig, frame):
        print("Caught CTRL+C, Stopping PyDrop Server...")
        self.stop()

    def stop(self):
        self.ALIVE = False
        if self.SERVER_SOCKET:
            self.SERVER_SOCKET.close()
        exit(0)        
                
                