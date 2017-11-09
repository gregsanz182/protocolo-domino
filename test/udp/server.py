import sys
import socket
import json

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    server_adress = ('localhost', 3001)
    print('Comenzando en {} port {}'.format(*server_adress))
    sock.bind(server_adress)

    while True:
        print('\nEsperando para recibir mensajes')
        data, address = sock.recvfrom(4096)

        print('received {} bytes from {}'.format(data, address))
        print(data)
        cont = 0
        if data:
            data_json = {
                "identificador": "DOMINOCOMUNICACIONESI",
                "nombre_mesa": "LOS TIGRES"
            }
            data = json.dumps(data_json).encode('utf-8')
            sent = sock.sendto(data, address)
            print('sent {} bytes back to {}'.format(sent, address))
            if cont == 2:
                break
            cont = cont + 1


