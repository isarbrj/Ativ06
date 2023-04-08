import xmlrpc.client
import threading
import time
from enum import Enum

class Recurso(Enum):
    CortarCabelo = 3
    CortarBarba = 4
    CortarBigode = 5

class Cliente:
    def __init__(self, id):
        self.id = id
        self.pendente = 0
        self.clock = 0
        self.ciclosTerminados = 0
        self.cicloAtual = Recurso.CortarCabelo
        self.finalizado = False

    def Concorrer(self, id, rc, cont, last):

        print(f"[CON] {self.id}:{id}:{last}:{self.cicloAtual.value}:{rc.value}:{self.clock}:{cont}")

        if last == self.id:
            return True

        if self.cicloAtual.value > rc.value:
            return True

        if self.clock == cont:
            if self.id < id:
                return False
            else:
                return True

        return False

    def terminar_ciclo(self):
        if self.ciclosTerminados == 20:
            print(f"Cliente {self.id} finalizou todos os seus ciclos.")
            self.finalizado = True

        if self.cicloAtual == Recurso.CortarCabelo:
            self.cicloAtual = Recurso.CortarBarba
        elif self.cicloAtual == Recurso.CortarBarba:
            self.cicloAtual = Recurso.CortarBigode
        elif self.cicloAtual == Recurso.CortarBigode:
            self.ciclosTerminados += 1
            self.cicloAtual = Recurso.CortarCabelo

class ExMutua:
    def __init__(self):
        self.clients = [Cliente(id) for id in range(5)]
        self.last = None
        self.sessaoCritica = None

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/")

def processo(id, exMut):
    clienteA = exMut.clients[id]

    while not clienteA.finalizado:

        clienteA = exMut.clients[id]
        time.sleep(3)

        oks = [True] * 5

        for i in range(5):
            if i != id:
                oks[i] = exMut.clients[i].Concorrer(id, clienteA.cicloAtual, clienteA.clock, exMut.last)
                if exMut.sessaoCritica == i:
                    oks[i] = False

        allOk = True
        for i in range(5):
            if oks[i] is False:
                allOk = False


        if allOk and exMut.last != clienteA.id:
            exMut.sessaoCritica = clienteA.id
            exMut.last = clienteA.id
            clienteA.atual = True
            if clienteA.cicloAtual == Recurso.CortarCabelo:
                print(proxy.cortarCabelo(clienteA.id))
            elif clienteA.cicloAtual == Recurso.CortarBarba:
                print(proxy.cortarBarba(clienteA.id))
            elif clienteA.cicloAtual == Recurso.CortarBigode:
                print(proxy.cortarBigode(clienteA.id))

            clienteA.terminar_ciclo()
            clienteA.atual = False
            exMut.sessaoCritica = None

for i in range(5):
    exMut = ExMutua()
    t = threading.Thread(target=processo, args=(i,exMut))
    t.start()

