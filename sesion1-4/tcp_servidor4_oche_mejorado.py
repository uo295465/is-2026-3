
import socket
import sys
import time

def recibe_mensaje(sd):
    buffer = []

    while True:
        byte = sd.recv(1)

        if byte == b"":
            return b"".join(buffer)

        buffer.append(byte)

        if byte == b"\n" and len(buffer) >= 2 and buffer[-2] == b"\r":
            return b"".join(buffer)


# Puerto por defecto
if len(sys.argv) < 2:
    puerto = 9999
else:
    puerto = int(sys.argv[1])

# Crear socket TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignar puerto
s.bind(("", puerto))

# Poner en modo pasivo
s.listen(5)

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")

    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)

    time.sleep(1)

    continuar = True

    while continuar:
        mensaje = recibe_mensaje(sd)

        if mensaje == b"":
            print("El cliente ha cerrado la conexión")
            continuar = False

        else:
            mensaje = mensaje.decode("utf8")
            linea = mensaje[:-2]
            linea = linea[::-1]

            sd.sendall((linea + "\r\n").encode("utf8"))

    sd.close()
