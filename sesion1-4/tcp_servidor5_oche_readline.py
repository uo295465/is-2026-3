
import socket
import sys
import time

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

    # Convertir el socket en un fichero de texto
    f = sd.makefile(encoding="utf8", newline="\r\n")

    time.sleep(1)

    continuar = True

    # Bucle de atención al cliente
    while continuar:
        mensaje = f.readline()

        if mensaje == "":
            print("El cliente ha cerrado la conexión")
            continuar = False

        else:
            # Eliminar el delimitador CRLF
            linea = mensaje[:-2]

            # Invertir el mensaje
            linea = linea[::-1]

            # Enviar respuesta
            sd.sendall((linea + "\r\n").encode("utf8"))

    # Cerrar fichero y socket
    f.close()
    sd.close()
