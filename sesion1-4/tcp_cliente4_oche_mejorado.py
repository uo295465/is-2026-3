
import socket

def recibe_mensaje(sd):
    buffer = []

    while True:
        byte = sd.recv(1)

        if byte == b"":
            return b"".join(buffer)

        buffer.append(byte)

        if byte == b"\n" and len(buffer) >= 2 and buffer[-2] == b"\r":
            return b"".join(buffer)


# Crear socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar con el servidor
cliente.connect(("localhost", 9999))

# Mensajes de prueba
mensajes = ["HOLA", "ADIOS", "TCP", "ABCDE"]

# Enviar todos los mensajes seguidos
for mensaje in mensajes:
    cliente.sendall((mensaje + "\r\n").encode("utf8"))

# Recibir las respuestas
for mensaje in mensajes:
    respuesta = recibe_mensaje(cliente)
    print("Respuesta del servidor:", respuesta.decode("utf8").strip())

# Cerrar conexión
cliente.close()
