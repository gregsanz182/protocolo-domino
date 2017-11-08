import sys
import socket

if __name__ == '__main__':
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = ('localhost', 2134)
    message = b'Este es el mensaje. Sera repetido'

    try:
        print('Enviando {!r}'.format(message))
        sent = sock.sendto(message, server_address)

        print('Esperando para recibir')
        data, server = sock.recvfrom(4096)
        print('received {!r}'.format(data))

    finally:
        print('closing socket')
        sock.close()
