
import socket

# Crear socket TCP
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Conectar con el servidor
cliente.connect(("localhost", 9999))

# Convertir socket en fichero
f = cliente.makefile(encoding="utf8", newline="\n")

# Mensajes de prueba
mensajes = ["HOLA", "ADIOS", "TCP", "ABCDE"]

# Enviar mensajes
for mensaje in mensajes:
    # Calcular longitud en bytes
    longitud = len(mensaje.encode("utf8"))

    # Enviar longitud y contenido
    cliente.sendall(("%d\n%s" % (longitud, mensaje)).encode("utf8"))

# Recibir respuestas
for mensaje in mensajes:
    # Leer longitud
    longitud_texto = f.readline()
    longitud = int(longitud_texto.strip())

    # Leer contenido
    respuesta = f.read(longitud)

    print("Respuesta del servidor:", respuesta)

# Cerrar recursos
f.close()
cliente.close()
