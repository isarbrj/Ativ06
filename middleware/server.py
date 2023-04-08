import xmlrpc.server
import time

class Barbeiro:

    def cortarCabelo(self, id):
        print(f"Começando corte do Cabelo do cliente {id}.")
        time.sleep(3)
        return "Cabelo do cliente {} Cortado.".format(id)

    def cortarBarba(self, id):
        print(f"Começando corte da Barba do cliente {id}.")
        time.sleep(4)
        return "Barba do cliente {} Cortada.".format(id)

    def cortarBigode(self, id):
        print(f"Começando corte do Bigode do cliente {id}.")
        time.sleep(5)
        return "Bigode do cliente {} Cortado.".format(id)


barbeiro = Barbeiro()

server = xmlrpc.server.SimpleXMLRPCServer(("localhost", 8000))

server.register_function(barbeiro.cortarCabelo, "cortarCabelo")
server.register_function(barbeiro.cortarBarba, "cortarBarba")
server.register_function(barbeiro.cortarBigode, "cortarBigode")

print("Servidor Iniciado")
server.serve_forever()
