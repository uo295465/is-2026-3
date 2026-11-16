
import socket

# Crear socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar con el servidor
cliente.connect(("localhost", 9999))

# Mensajes de prueba
mensajes = ["HOLA", "ADIOS", "TCP", "ABCDE"]

for mensaje in mensajes:
    # Enviar mensaje terminado en CRLF
    cliente.sendall((mensaje + "\r\n").encode("utf8"))

    # Recibir respuesta
    respuesta = cliente.recv(80)

    # Mostrar respuesta
    print("Respuesta del servidor:", respuesta.decode("utf8").strip())

# Cerrar conexión
cliente.close()
