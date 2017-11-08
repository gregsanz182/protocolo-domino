import sys
import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_adress = ('localhost', 3001)
    print('Comenzando en {} port {}'.format(*server_adress))
    sock.bind(server_adress)

    while True:
        print('\nEsperando para recibir mensajes')
        data, address = sock.recvfrom(4096)

        print('received {} bytes from {}'.format(len(data), address))
        print(data)

        if data:
            sent = sock.sendto(data, address)
            print('sent {} bytes back to {}'.format(sent, address))


