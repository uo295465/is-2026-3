
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

    # Convertir socket en fichero
    f = sd.makefile(encoding="utf8", newline="\n")

    continuar = True

    while continuar:
        # Recibir longitud del mensaje
        longitud_texto = f.readline()

        if longitud_texto == "":
            print("El cliente ha cerrado la conexión")
            continuar = False

        else:
            # Convertir longitud a entero
            longitud = int(longitud_texto.strip())

            # Recibir exactamente la longitud indicada
            mensaje = f.read(longitud)

            if len(mensaje) < longitud:
                print("El cliente ha cerrado la conexión antes de completar el mensaje")
                continuar = False

            else:
                # Invertir mensaje
                respuesta = mensaje[::-1]

                # Calcular longitud de la respuesta en bytes
                longitud_respuesta = len(respuesta.encode("utf8"))

                # Enviar longitud y mensaje
                sd.sendall(
                    ("%d\n%s" % (longitud_respuesta, respuesta)).encode("utf8")
                )

    f.close()
    sd.close()
