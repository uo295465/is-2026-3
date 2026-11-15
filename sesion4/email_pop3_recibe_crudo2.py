
import socket
import ssl
import sys
import getpass
from email import policy
from email.parser import BytesParser


# Función para recibir y comprobar respuestas POP3
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


# Recibimos el mensaje inicial
RecvReply(sc)


# Enviamos usuario
sc.sendall(("USER " + username + "\r\n").encode("ascii"))
RecvReply(sc)


# Enviamos contraseña
sc.sendall(("PASS " + password + "\r\n").encode("utf8"))
RecvReply(sc)


# Consultamos el número de correos
sc.sendall(b"STAT\r\n")
respuesta = RecvReply(sc)

datos = respuesta.decode().split()
num_correos = int(datos[1])

print("Número de correos disponibles:", num_correos)


# Recorremos todos los correos disponibles
for i in range(1, num_correos + 1):

    print("\nCORREO", i)

    # Solicitamos el correo correspondiente
    sc.sendall(("RETR " + str(i) + "\r\n").encode("ascii"))
    RecvReply(sc)

    # Recibimos el contenido completo
    correo = b""

    while True:
        linea = b""

        while not linea.endswith(b"\r\n"):
            dato = sc.recv(1)

            if not dato:
                print("ERROR: Conexión cerrada durante la recepción")
                sys.exit()

            linea += dato

        # Fin del correo
        if linea == b".\r\n":
            break

        # Desescapamos los puntos duplicados
        if linea.startswith(b".."):
            linea = linea[1:]

        correo += linea

    # Interpretamos el mensaje
    mensaje = BytesParser(policy=policy.default).parsebytes(correo)

    # Mostramos asunto y remitente
    print("ASUNTO:", mensaje["Subject"])
    print("REMITENTE:", mensaje["From"])


# Cerramos la sesión POP3
sc.sendall(b"QUIT\r\n")
RecvReply(sc)

sc.close()

print("Conexión cerrada")
