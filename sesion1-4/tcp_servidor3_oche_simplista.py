
import socket
import sys

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
        # Recibir mensaje
        mensaje = sd.recv(80)

        # Comprobar si el cliente ha cerrado la conexión
        if mensaje == b"":
            print("El cliente ha cerrado la conexión")
            continuar = False

        else:
            # Convertir bytes a texto
            mensaje = str(mensaje, "utf8")

            # Eliminar los dos caracteres del final de línea
            linea = mensaje[:-2]

            # Invertir el mensaje
            linea = linea[::-1]

            # Añadir el delimitador y enviar respuesta
            sd.sendall(bytes(linea + "\r\n", "utf8"))

    sd.close()
