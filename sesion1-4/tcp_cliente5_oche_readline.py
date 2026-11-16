
import socket
import sys

# Dirección IP y puerto por defecto
if len(sys.argv) < 3:
    ip = "localhost"
    puerto = 9999
else:
    ip = sys.argv[1]
    puerto = int(sys.argv[2])

# Crear socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar con el servidor
cliente.connect((ip, puerto))

# Convertir socket en fichero
f = cliente.makefile(encoding="utf8", newline="\r\n")

# Mensajes de prueba
mensajes = ["HOLA", "ADIOS", "TCP", "ABCDE"]

# Enviar todos los mensajes
for mensaje in mensajes:
    cliente.sendall((mensaje + "\r\n").encode("utf8"))

# Recibir respuestas
for mensaje in mensajes:
    respuesta = f.readline()
    print("Respuesta del servidor:", respuesta.strip())

# Cerrar recursos
f.close()
cliente.close()
