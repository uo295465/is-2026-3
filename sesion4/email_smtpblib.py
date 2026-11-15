
import smtplib
import ssl
import getpass
from email.message import EmailMessage
from email.utils import formatdate, make_msgid


# Configuración del servidor SMTP
server = "smtp.gmail.com"
port = 587

# Pedimos las credenciales
username = input("Usuario (correo Gmail): ")
password = getpass.getpass("Contraseña de aplicación: ")

# Pedimos los datos del correo
destinatario = input("Destinatario: ")
asunto = input("Asunto: ")
texto = input("Mensaje: ")


# Creamos el mensaje
mensaje = EmailMessage()

mensaje["From"] = username
mensaje["To"] = destinatario
mensaje["Subject"] = asunto
mensaje["Date"] = formatdate(localtime=True)
mensaje["Message-ID"] = make_msgid()

mensaje.set_content(texto)


# Creamos el contexto SSL
context = ssl.create_default_context()

# Conectamos con el servidor SMTP
s = smtplib.SMTP(server, port)

# Activamos la depuración del protocolo
s.set_debuglevel(1)

try:
    # Iniciamos la comunicación
    s.ehlo()

    # Activamos el cifrado TLS
    s.starttls(context=context)

    # Volvemos a identificarnos después de STARTTLS
    s.ehlo()

    # Autenticación
    s.login(username, password)

    # Enviamos el correo
    s.sendmail(
        username,
        [destinatario],
        mensaje.as_bytes()
    )

    print("Correo enviado correctamente")

finally:
    # Cerramos la conexión
    s.quit()
