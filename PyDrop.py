# Title: PyDrop
# Description: A file transfer tool written using Python
# Author: Richard Smith

from server import Server
from client import Client
import time
import argparse

def main():

    pyDropImage = """                                                                                                    
                                                 7!                                                 
                                                !55!                                                
                                               !5555!                                               
                                              75555557                                              
                                            .?55555555?.                                            
                                           :J5555555555J:                                           
                                          ~Y555555555555Y~                                          
                                        .755555555555555557.                                        
                                       :J555555555555555555J:                                       
                                      ~Y55555555555555555555Y~                                      
                                    .75555555555555555555555557.                                    
                                   :J55555555555555555555555555J:                                   
                                  ^Y5555555555555555555555555555Y^                                  
                                 ~55555555555555555555555555555555~                                 
                                !55YY555555555555555555555555555555!                                
                               ~55Y!55555555555555555555555555555555~                               
                              ^55Y:~555555555555555555555555555555555^                              
                             .Y55~ 7555555555555555555555555555555555Y.                             
                             ~55J  75555555555555555555555555555555555~                             
                             7557  !55555555555555555555555555555555557                             
                             !55?  :5555555555555555555555555555555555!                             
                             :555:  ?555555555555555555555555555555555:                             
                              755J. :Y55555555555555555555555555555557                              
                               ?55J. ^555555555555555555555555555555?                               
                                755Y~ :Y5555555555555555555555555557                                
                                 ^J55J~:7Y55555555555555555555555J^                                 
                                  .~J55Y7!?Y5555555555555555555J~.                                  
                                     :!J555Y555555555555555YJ!:                                     
                                        :^!?JYY555555YYJ?!^:                                        
                                             ..::::::..                                             
                                                                                                    
                                                                                                    
                                                                                                    """
      
    print(pyDropImage)

    parser = argparse.ArgumentParser(description='Transfer files using Python.')
    parser.add_argument('MODE', type=str, choices=['server','client'], help="Use PyDrop in Server or Client mode")
    parser.add_argument('--filepath', '-fp', type=str, help="The directory containing files for access, for use in SERVER mode. By default PyDrop users the current working directory")
    parser.add_argument('--filename', '-f', type=str, help="The filename to retrieve from the PyDrop server")
    parser.add_argument('--host', '-H', type=str, help="Use in CLIENT mode to specify the IPv4 address of the PyDrop server. By default, PyDrop Server listens on 0.0.0.0")
    parser.add_argument('--port', '-p', type=int, help="The TCP port of the PyDrop Server, in SERVER mode PyDrop defaults to 9090/tcp")
    parser.add_argument('--encrypted', '-e', action='store_true', help="Use SSL/TLS encryption to transfer files")
    parser.add_argument('--certfile','-c', type=str, help="If --encryption/-e is specified in SERVER mode, a certfile must be specified")
    parser.add_argument('--keyfile','-k', type=str, help="If --encryption/-e is specified in SERVER mode, a keyfile must be specified")
    args = parser.parse_args()

    # Instantiate a new server (encrypted) object:
    if (args.MODE == "server" and args.encrypted is True):
        # Check certfiles and keyfiles:
        if (args.certfile is None or args.keyfile is None):
            parser.print_help()
            exit()
        else:
            print(f"[!] Starting PyDrop Server")
            print(f"[!] Using {args.certfile} as certificate")
            print(f"[!] Using {args.keyfile} as key file")
            time.sleep(3) # Delay and wait for manual abort

            if (args.port is not None and args.filepath is not None):
                PyDropServer = Server(PORT=args.port, FILEPATH=args.filename, CERTFILE=args.certfile, KEYFILE=args.keyfile) # Port and filename are user defined
            elif(args.port is not None and args.filepath is None):
                PyDropServer = Server(PORT=args.port, CERTFILE=args.certfile, KEYFILE=args.keyfile) # Port is user defined
            elif(args.port is None and args.filepath is not None):
                PyDropServer = Server(FILEPATH=args.filepath, CERTFILE=args.certfile, KEYFILE=args.keyfile) # Filepath is user defined
            else:
                PyDropServer = Server(CERTFILE=args.certfile, KEYFILE=args.keyfile) # Only neccessary encryption files are specified
        PyDropServer.encrypted_server()
    
    # Instantiate a new server (unencrypted) object:
    elif (args.MODE == "server" and args.encrypted is False):
        print(f"[!] Starting PyDrop Server")
        print(f"[!] WARNING - PyDrop starting in unencrypted mode!")
        time.sleep(3) # Delay and wait for manual abort
        if (args.port is not None and args.filepath is not None):
            PyDropServer = Server(PORT=args.port, FILEPATH=args.filename) # Port and Filepath are user defined:
        elif(args.port is not None and args.filepath is None):
            PyDropServer = Server(PORT=args.port) # Filepath is user defined:
        elif(args.port is None and args.filepath is not None):
            PyDropServer = Server(FILEPATH=args.filepath) # Port is user defined:
        else:
            PyDropServer = Server() # Nothing is user defined:
        PyDropServer.unencrypted_server()

    # Instantiate a new client object:
    elif (args.MODE == "client" and args.encrypted is False):
        if (args.host is None or args.port is None or args.filename is None): # User must specify all neccessary parameters in client mode:
            parser.print_help()
        else:
            PyDropClient = Client(args.host, args.port, args.filename)
            PyDropClient.fetch_file()
    elif (args.MODE == "client" and args.encrypted is True):
        if (args.host is None or args.port is None or args.filename is None): # User must specify all neccessary parameters in client mode:
            parser.print_help()
        else:
            PyDropClient = Client(args.host, args.port, args.filename)
            PyDropClient.secure_fetch_file()
main()