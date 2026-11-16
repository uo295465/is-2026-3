
import socket
import sys

# Puerto por defecto
if len(sys.argv) < 2:
    puerto = 9999
else:
    puerto = int(sys.argv[1])

# Creación del socket de escucha TCP
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Asignar puerto
s.bind(("", puerto))

# Poner el socket en modo pasivo
s.listen(5)

# Bucle principal de espera por clientes
while True:
    print("Esperando un cliente")

    sd, origen = s.accept()
    print("Nuevo cliente conectado desde %s, %d" % origen)

    continuar = True

    # Bucle de atención al cliente
    while continuar:
        datos = sd.recv(5)
        datos = datos.decode("ascii")

        if datos == "":
            print("Conexión cerrada de forma inesperada por el cliente")
            sd.close()
            continuar = False

        elif datos == "FINAL":
            print("Recibido mensaje de finalización")
            sd.close()
            continuar = False

        else:
            print("Recibido mensaje: %s" % datos)
