import sys
import socket
import json

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('192.168.0.255', 3001)
    men = {
        'identificador': 'DOMINOCOMUNICACIONESI',
        'fichas': [
            {
                'token': 'qwerty',
                'entero_uno': 6,
                'entero_dos': 1
            },
            {
                'token': 'qwerty2',
                'entero_uno': 5,
                'entero_dos': 4
            },
            {
                'token': 'qwerty3',
                'entero_uno': 3,
                'entero_dos': 2
            }
        ]
    }
    message = json.dumps(men).encode('utf-8')
    try:
        print('Enviando {!r}'.format(message))
        sent = sock.sendto(message, server_address)

        print('Esperando para recibir')
        data, server = sock.recvfrom(4096)
        print(json.loads(data.decode('utf-8')))

    finally:
        print('closing socket')
        sock.close()
