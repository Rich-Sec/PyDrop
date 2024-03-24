# Title: PyDrop
# Description: A file transfer tool written using Python
# Author: Richard Smith

from server import Server
from client import Client
import argparse

def main():
    parser = argparse.ArgumentParser(description='Transfer files using Python.')
    parser.add_argument('MODE', type=str, choices=['server','client'], help="Use PyDrop in Server or Client mode")
    parser.add_argument('--filepath', '-FP', type=str, help="The directory containing files for access, for use in SERVER mode. By default PyDrop users the current working directory")
    parser.add_argument('--filename', '-F', type=str, help="The filename to retrieve from the PyDrop server")
    parser.add_argument('--host', '-H', type=str, help="Use in CLIENT mode to specify the IPv4 address of the PyDrop server. By default, PyDrop Server listens on 0.0.0.0")
    parser.add_argument('--port', '-P', type=int, help="The TCP port of the PyDrop Server, in SERVER mode PyDrop defaults to 9090/tcp")
    args = parser.parse_args()

    # Instantiate a new server object:
    if (args.MODE == "server"):
        # Port and Filepath are user defined:
        if (args.port is not None and args.filepath is not None):
            PyDropServer = Server(PORT=args.port, FILEPATH=args.filename)
        # Filepath is user defined:
        elif(args.port is not None and args.filepath is None):
            PyDropServer = Server(PORT=args.port)
        # Port is user defined:
        elif(args.port is None and args.filepath is not None):
            PyDropServer = Server(FILEPATH=args.filepath)
        # Nothing is user defined:
        else:
            PyDropServer = Server()
        PyDropServer.unencryptedServer()
    # Instantiate a new client object:
    elif (args.MODE == "client"):
        # User must specify all neccessary parameters in client mode:
        if (args.host is None or args.port is None or args.filename is None):
            print(f"In CLIENT mode the following flags must be specified:\n*--filename/-f\n*--host/-h\n*--port/-p")
        else:
            PyDropClient = Client(args.host, args.port, args.filename)
            PyDropClient.fetchFile()
    else:
        pass

main()