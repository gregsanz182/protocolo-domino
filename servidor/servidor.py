import sys
import socket
import json

if __name__ == '__main__':

    sockUDP = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    direccion_servidor = ('0.0.0.0', 3001)

    disponibilidad = 4
    clientes = []
    mesaJson = {
        'identificador': 'DOMINOCOMUNICACIONESI',
        'nombre_mesa': 'la que más aplaude'
    }

    print('Escuchando en {} por el puerto {}'.format(*direccion_servidor))

    sockUDP.bind(direccion_servidor)

    while True:
        mensaje, direccion = sockUDP.recvfrom(4096)

        if mensaje:
            msg = json.loads(mensaje.decode('utf-8'))
            if msg['identificador'] == 'DOMINOCOMUNICACIONESI' and disponibilidad > 0:
                sockUDP.sendto(json.dumps(mesaJson).encode('utf-8'), direccion)
                disponibilidad -= 1

        
        