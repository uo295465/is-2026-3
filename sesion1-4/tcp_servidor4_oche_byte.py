
import socket
import sys

def recibe_mensaje(sd):
    mensaje = b""

    while True:
        byte = sd.recv(1)

        if byte == b"":
            return mensaje

        mensaje += byte

        if mensaje.endswith(b"\r\n"):
            return mensaje


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

    continuar = True

    # Bucle de atención al cliente
    while continuar:
        mensaje = recibe_mensaje(sd)

        if mensaje == b"":
            print("El cliente ha cerrado la conexión")
            continuar = False

        else:
            # Convertir bytes a texto
            mensaje = mensaje.decode("utf8")

            # Eliminar el delimitador CRLF
            linea = mensaje[:-2]

            # Invertir el mensaje
            linea = linea[::-1]

            # Enviar respuesta con CRLF
            sd.sendall((linea + "\r\n").encode("utf8"))

    sd.close()
