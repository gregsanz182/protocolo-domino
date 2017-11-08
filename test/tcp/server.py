import socket
import sys
import json

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_address = ('localhost', 3001)
    print('Comenzando en {} puerto {}'.format(*server_address))
    sock.bind(server_address)

    sock.listen(1)

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

    while True:
        print('Esperando por una conexion')
        connection, client_address = sock.accept()
        try:
            print('Conexion desde', client_address)

            while True:
                data = connection.recv(2024)
                if data:
                    menrec = json.loads(data.decode('utf-8'))
                    print(menrec)
                    connection.sendall(json.dumps(men).encode('utf-8'))
                else:
                    print('No hay datos desde', client_address)
                    break

        finally:
            connection.close()
