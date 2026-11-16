
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

# Enviar cinco mensajes de 5 bytes
for i in range(5):
    mensaje = "ABCDE"
    cliente.sendall(mensaje.encode("ascii"))

# Enviar mensaje de finalización
cliente.sendall("FINAL".encode("ascii"))

# Cerrar conexión
cliente.close()
