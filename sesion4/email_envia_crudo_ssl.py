
import socket
import ssl
import sys
import base64
import getpass


# Función para recibir y comprobar las respuestas SMTP
def RecvReply(sock, code):
    respuesta = b""

    while True:
        linea = sock.recv(1024)
        if not linea:
            print("ERROR: El servidor ha cerrado la conexión")
            sys.exit()

        respuesta += linea

        # Comprobamos si la respuesta SMTP ha terminado
        lineas = respuesta.splitlines()
        if lineas and len(lineas[-1]) >= 4:
            if lineas[-1][3:4] == b" ":
                break

    print(respuesta.decode("utf8", errors="replace"))

    if not respuesta.startswith(str(code).encode()):
        print("ERROR: Respuesta inesperada del servidor")
        sys.exit()

    return respuesta


# Configuración del servidor SMTP
server = "smtp.gmail.com"
port = 587

# Creamos el socket y conectamos con Gmail
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((server, port))

# Recibimos la respuesta inicial (220)
RecvReply(s, 220)


# Enviamos EHLO
s.sendall(b"EHLO localhost\r\n")
RecvReply(s, 250)


# Solicitamos iniciar el cifrado TLS
s.sendall(b"STARTTLS\r\n")
RecvReply(s, 220)


# Creamos la conexión segura
context = ssl.create_default_context()
sc = context.wrap_socket(s, server_hostname=server)

print("Conexión TLS establecida correctamente")


# Autenticación SMTP mediante AUTH LOGIN
sc.sendall(b"AUTH LOGIN\r\n")
RecvReply(sc, 334)


# Solicitamos usuario y contraseña
username = input("Usuario (correo Gmail): ")
password = getpass.getpass("Contraseña de aplicación: ")


# Enviamos el usuario codificado en Base64
sc.sendall(base64.b64encode(username.encode("ascii")) + b"\r\n")
RecvReply(sc, 334)


# Enviamos la contraseña codificada en Base64
sc.sendall(base64.b64encode(password.encode("utf8")) + b"\r\n")
RecvReply(sc, 235)


# Introducimos los datos del correo
remitente = username
destinatario = input("Destinatario: ")
asunto = input("Asunto: ")
mensaje = input("Mensaje: ")


# Indicamos el remitente
sc.sendall(("MAIL FROM:<" + remitente + ">\r\n").encode("ascii"))
RecvReply(sc, 250)


# Indicamos el destinatario
sc.sendall(("RCPT TO:<" + destinatario + ">\r\n").encode("ascii"))
RecvReply(sc, 250)


# Comenzamos el contenido del mensaje
sc.sendall(b"DATA\r\n")
RecvReply(sc, 354)


# Construimos el mensaje
contenido = (
    "From: " + remitente + "\r\n"
    "To: " + destinatario + "\r\n"
    "Subject: " + asunto + "\r\n"
    "\r\n"
    + mensaje + "\r\n"
)

# Escapamos los puntos al inicio de línea según SMTP
contenido = contenido.replace("\r\n.", "\r\n..")

# Enviamos el mensaje y terminamos DATA con un punto
sc.sendall(contenido.encode("utf8") + b".\r\n")
RecvReply(sc, 250)


# Cerramos la sesión SMTP
sc.sendall(b"QUIT\r\n")
RecvReply(sc, 221)

sc.close()

print("Correo enviado correctamente")
