#!/usr/bin/env python3
import socket, time, sys


#define address & buffer size
HOST = "localhost"
PORT = 8001
BUFFER_SIZE = 1024

#get ip

def get_remote_ip(host):
    print("f'Getting IP for {host}")
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print( 'Hostname could not be resolved. exiting')
        sys.exit()

def main():

    #QUESTION 6
    extern_host = 'www.google.com'
    port = 80

    #create socket
    with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as proxy_start:
        print("Starting Proxy Server")
        #allow reused addresses, bind, and set to listening mode.
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            #connect proxy_start
            conn, addr = proxy_start.accept()
            print("Connected by", addr)


            with socket.socket( socket.AF_INET, socket.SOCK_STREAM ) as proxy_end:
                print("Connecting to google")
                remote_ip = get_remote_ip(extern_host)

                #connect proxy_end
                proxy_end.connect((remote_ip, port))

                #send data
                send_full_data = conn.recv(BUFFER_SIZE)
                print(f"Sending recieved data {send_full_data} to google")
                proxy_end.sendall(send_full_data)

                #remember to shutdown
                proxy_end.shutdown(socket.SHUT_WR) #shutdown different from close()

                data = proxy_end.recv(BUFFER_SIZE)
                print(f"Sending recieved Data {data} to client")
                #send data back

            conn.close()

if __name__ == "__main__":
    main()



