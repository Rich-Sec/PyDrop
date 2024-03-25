# Title: PyDrop Client Implementation
# Author: Richard Smith

import socket
import ssl

class Client:
    def __init__(self, HOST, PORT, FILENAME, *args, **kwargs):
        self.HOST = HOST
        self.PORT = PORT
        self.FILENAME = FILENAME

    def fetch_file(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            try:
                clientSocket.sslSocketect((self.HOST, self.PORT))
                print(f"sslSocketected to PyDrop Server")

                # Send the name of the file we wish to retreive to the server:
                filenameLength = len(self.FILENAME)
                clientSocket.sendall(filenameLength.to_bytes(4, byteorder='big'))
                clientSocket.sendall(self.FILENAME.encode())
                
                # Receive filename length
                filenameLengthBytes = clientSocket.recv(4)
                filenameLength = int.from_bytes(filenameLengthBytes, byteorder='big')
                
                # Receive filename
                filename = clientSocket.recv(filenameLength).decode()

                # Receive file data length
                fileDataLengthBytes = clientSocket.recv(8)
                fileDataLength = int.from_bytes(fileDataLengthBytes, byteorder='big')

                # Receive file data
                file_data = b''
                while len(file_data) < fileDataLength:
                    file_data += clientSocket.recv(1024)

                # Write file data to disk with the original filename
                with open(filename, "wb") as file:
                    file.write(file_data)

                print(f"File received successfully")
            except Exception as e:
                print(e)
    
    def secure_fetch_file(self):
        # Create client socket
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as clientSocket:
            try:
                # Wrap client socket with SSL context
                sslContext = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
                sslContext.check_hostname = False
                sslContext.verify_mode = ssl.CERT_NONE
                sslSocket = sslContext.wrap_socket(clientSocket, server_hostname=self.HOST)
                
                # sslSocketect to server
                sslSocket.connect((self.HOST, self.PORT))
                print(f"Connected to PyDrop Server Securely")
            
                # Send the name of the file we wish to retreive to the server:
                filenameLength = len(self.FILENAME)
                sslSocket.sendall(filenameLength.to_bytes(4, byteorder='big'))
                sslSocket.sendall(self.FILENAME.encode())
                
                # Receive filename length
                filenameLengthBytes = sslSocket.recv(4)
                filenameLength = int.from_bytes(filenameLengthBytes, byteorder='big')
                
                # Receive filename
                filename = sslSocket.recv(filenameLength).decode()

                # Receive file data length
                fileDataLengthBytes = sslSocket.recv(8)
                fileDataLength = int.from_bytes(fileDataLengthBytes, byteorder='big')

                # Receive file data
                file_data = b''
                while len(file_data) < fileDataLength:
                    file_data += sslSocket.recv(1024)

                # Write file data to disk with the original filename
                with open(filename, "wb") as file:
                    file.write(file_data)

                print(f"File received successfully")
            except Exception as e:
                print(e)
        

            