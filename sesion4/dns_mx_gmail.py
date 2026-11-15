
import dns.resolver

# Consultar los registros MX de gmail.com
respuesta = dns.resolver.resolve('gmail.com', 'MX')

# Ordenar los servidores según su prioridad
servidores = sorted(respuesta, key=lambda registro: registro.preference)

# Recorrer los servidores MX
for registro in servidores:

    prioridad = registro.preference
    servidor = str(registro.exchange)

    # Consultar la dirección IPv4 del servidor
    respuesta_ip = dns.resolver.resolve(servidor, 'A')

    # Mostrar todas las IP asociadas al servidor
    for ip in respuesta_ip:
        print(prioridad, servidor, ip.address)
