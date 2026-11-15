
import socket
import ssl
import sys
import getpass
from email import policy
from email.parser import BytesParser


# Función para recibir una línea y comprobar la respuesta POP3
def RecvReply(sock):
    respuesta = b""

    while not respuesta.endswith(b"\r\n"):
        dato = sock.recv(1)

        if not dato:
            print("ERROR: El servidor ha cerrado la conexión")
            sys.exit()

        respuesta += dato

        if len(respuesta) > 1024:
            print("ERROR: Respuesta demasiado larga")
            sys.exit()

    print(respuesta.decode("utf8", errors="replace"))

    if respuesta[:3] != b"+OK":
        print("ERROR: Respuesta inesperada del servidor")
        sys.exit()

    return respuesta


# Configuración del servidor POP3
server = "pop.gmail.com"
port = 995


# Pedimos usuario y contraseña
username = input("Usuario: ")
password = getpass.getpass("Contraseña de aplicación: ")


# Creamos el socket y conectamos
s = socket.socket()
s.connect((server, port))


# Establecemos el canal seguro
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)


# Recibimos el mensaje inicial del servidor
RecvReply(sc)


# Enviamos el usuario
sc.sendall(("USER " + username + "\r\n").encode("ascii"))
RecvReply(sc)


# Enviamos la contraseña
sc.sendall(("PASS " + password + "\r\n").encode("utf8"))
RecvReply(sc)


# Consultamos el número de correos disponibles
sc.sendall(b"STAT\r\n")
respuesta = RecvReply(sc)

# Extraemos el número de mensajes
datos = respuesta.decode().split()
num_correos = int(datos[1])

print("Número de correos disponibles:", num_correos)


# Si hay correos, recibimos el primero
if num_correos > 0:

    # Solicitamos el primer correo
    sc.sendall(b"RETR 1\r\n")
    RecvReply(sc)

    # Recibimos el contenido completo del correo
    correo = b""

    while True:
        linea = b""

        while not linea.endswith(b"\r\n"):
            dato = sc.recv(1)

            if not dato:
                print("ERROR: Conexión cerrada durante la recepción")
                sys.exit()

            linea += dato

        # El correo termina con una línea que contiene solamente un punto
        if linea == b".\r\n":
            break

        # Eliminamos el punto adicional de las líneas que empiezan por punto
        if linea.startswith(b".."):
            linea = linea[1:]

        correo += linea

    # Interpretamos el correo electrónico
    mensaje = BytesParser(policy=policy.default).parsebytes(correo)

    # Mostramos las cabeceras solicitadas
    print("\nASUNTO:", mensaje["Subject"])
    print("REMITENTE:", mensaje["From"])

else:
    print("No hay correos disponibles")


# Cerramos la sesión POP3
sc.sendall(b"QUIT\r\n")
RecvReply(sc)

sc.close()

print("Conexión cerrada")
