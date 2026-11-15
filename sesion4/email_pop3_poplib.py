
import poplib
import getpass


# Configuración del servidor POP3
server = "pop.gmail.com"

# Pedimos usuario y contraseña
username = input("Usuario: ")
password = getpass.getpass("Contraseña de aplicación: ")


# Creamos la conexión segura POP3
pop3_mail = poplib.POP3_SSL(server, 995)

# Activamos la depuración del protocolo
pop3_mail.set_debuglevel(2)


# Enviamos usuario y contraseña
pop3_mail.user(username)
pop3_mail.pass_(password)


# Consultamos el número de mensajes
num_mensajes, tamano = pop3_mail.stat()

print("\nNúmero de mensajes:", num_mensajes)
print("Tamaño total:", tamano, "bytes")


# Si hay mensajes, recibimos el primero
if num_mensajes > 0:

    # Recuperamos el primer mensaje
    numero, contenido, tamano = pop3_mail.retr(1)

    print("\nCONTENIDO DEL PRIMER CORREO:\n")

    # Mostramos las líneas recibidas
    for linea in contenido:
        print(linea.decode("utf8", errors="replace"))

else:
    print("No hay mensajes disponibles")


# Cerramos la conexión
pop3_mail.quit()

print("\nConexión cerrada")
