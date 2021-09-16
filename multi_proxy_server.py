#!/usr/bin/env python3

import socket, time, sys
from multiprocessing import Process

HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


#TO-DO: get_remote_ip() method

def get_remote_ip(host):
    print(f'Getting IP for {host}')
    try:
        remote_ip = socket.gethostbyname( host )
    except socket.gaierror:
        print ('Hostname could not be resolved. Exiting')
        sys.exit()

    print (f'Ip address of {host} is {remote_ip}')
    return remote_ip

#TO-DO: handle_request() method

def handle_request(conn,proxy_end):
    #send the data
    send_full_data = conn.recv(BUFFER_SIZE)
    print(f"Sending Recieved Data {send_full_data} to Google.com")
    proxy_end.sendall(send_full_data)

    #shutdown
    proxy_end.shutdown(socket.SHUT_WR)

    data = proxy_end.recv(BUFFER_SIZE)
    print(f"Sending Recieved Data {data} to Client")
    
    #send the data back
    conn.send(data)


def main():


#TO-DO: establish localhost, extern_host (google), port, buffer size
    extern_host = 'www.google.com'
    port = 80
    buffer_size = 1024

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_start: #establish "start" of proxy (connects to localhost)
        #to-do bind, and set to listening mode
        print("Starting Proxy Server")
        proxy_start.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        proxy_start.bind((HOST, PORT))
        proxy_start.listen(1)

        while True:
            #to-do: accept incoming connections from proxy_start, print information abotu connection
            conn, addr = proxy_start.accept()
            print("Connected By...", addr)

            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_end: #establish "end" of proxy (connects to google)
                #to-do: get remote IP of google, connect proxy_end to it
                print("Connecting to Google")
                remote_ip = get_remote_ip(extern_host)
                proxy_end.connect((remote_ip , port))

                #now for the multiprocessing
                #todo: allow for the muliple connections with a process daemon
                #make sure to set target = handle_request when creating the process

                p = Process(target = handle_request, args=(conn,proxy_end))
                p.daemon = True
                p.start()
                print("Started Process... ", p)

            #todoL close the connection
        
        conn.close()

if __name__ == "__main__":
    main()





