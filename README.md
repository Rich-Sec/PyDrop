# Introduction:
PyDrop was written as a side project but also has practical applications! Use PyDrop to transfer files **securely** over SSL/TLS or unsecurely! Quickly transfer files from one host to another whether your playing a CTF, performing a penetration test or carrying out general administration. PyDrop is designed to be deployed quickly and easily in any environment that supports the Python programming language, on both Windows and Linux.

# Prerequisites:
PyDrop requires the following prerequisites to work:
* Python 3.x
* A certificate file (for use in encrypted mode)
* A key file (for use in encrypted mode)

To use TLS, PyDrop requires you to specify a certificate and a private key using the `-c` and `-k` flags. To create your own certificate and key, you can use the `openssl` command:

* openssl x509 -req -days 365 -in server.csr -signkey server.key -out server.crt

Note this will create a "self-signed certificate", which by default PyDrop will accept without warning. 

# Usage:
By default, the PyDrop server listens on port 9090/tcp, this can be changed using the `-p` flag, similarly PyDrop will listen on all interfaces `0.0.0.0`, this can be changed using `-H`. 

* Start an Unencrypted Server on port 9090/tcp: `PyDrop.py server`
* Connect to Unencrypted PyDrop Server: `PyDrop.py client --host <IP> --port <PORT> --filename <FILENAME_TO_FETCH>`
* Start an Encrypted Server on port 9090/tcp: `PyDrop.py server --encrypted --certfile ./server.crt --keyfile ./server.key`
* Connect to Encrypted Server: `PyDrop client --encrypted --host 127.0.0.1 --port 9090 --filename <FILENAME_TO_FETCH>`

```
python .\PyDrop.py -h

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



usage: PyDrop.py [-h] [--filepath FILEPATH] [--filename FILENAME] [--host HOST] [--port PORT] [--encrypted] [--certfile CERTFILE] [--keyfile KEYFILE]
                 {server,client}

Transfer files using Python.

positional arguments:
  {server,client}       Use PyDrop in Server or Client mode

options:
  -h, --help            show this help message and exit
  --filepath FILEPATH, -fp FILEPATH
                        The directory containing files for access, for use in SERVER mode. By default PyDrop users the current working directory
  --filename FILENAME, -f FILENAME
                        The filename to retrieve from the PyDrop server
  --host HOST, -H HOST  Use in CLIENT mode to specify the IPv4 address of the PyDrop server. By default, PyDrop Server listens on 0.0.0.0
  --port PORT, -p PORT  The TCP port of the PyDrop Server, in SERVER mode PyDrop defaults to 9090/tcp
  --encrypted, -e       Use SSL/TLS encryption to transfer files
  --certfile CERTFILE, -c CERTFILE
                        If --encryption/-e is specified in SERVER mode, a certfile must be specified
  --keyfile KEYFILE, -k KEYFILE
                        If --encryption/-e is specified in SERVER mode, a keyfile must be specified
```
