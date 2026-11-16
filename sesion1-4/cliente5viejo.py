
import socket

# Crear socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar con el servidor
cliente.connect(("localhost", 9999))

# Convertir socket en fichero
f = cliente.makefile(encoding="utf8", newline="\r\n")

# Mensajes de prueba
mensajes = ["HOLA", "ADIOS", "TCP", "ABCDE"]

# Enviar todos los mensajes seguidos
for mensaje in mensajes:
    cliente.sendall((mensaje + "\r\n").encode("utf8"))

# Recibir las respuestas
for mensaje in mensajes:
    respuesta = f.readline()
    print("Respuesta del servidor:", respuesta.strip())

# Cerrar recursos
f.close()
cliente.close()

