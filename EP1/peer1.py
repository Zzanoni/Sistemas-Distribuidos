#PEER 4096

import glob, random, socket, time
from threading import Thread

cache4096 = ''
cache4097 = ''
cache4098 = ''
cache4099 = ''
cache4100 = ''
contador = 0
contadorRemove = 0

def estadoAntigo(novoEstado, antigoEstado):
    if novoEstado != '' and antigoEstado == '':
        return True
    elif novoEstado != '' and antigoEstado != '':
        peer1, contador1, estado1 = separarMsg(novoEstado.encode())
        peer2, contador2, estado2 = separarMsg(antigoEstado.encode())
        if contador1 > contador2:
            return True
    return False

def resetCache(porta):
    global cache4096, cache4097, cache4098, cache4099, cache4100
    id =  idPeer(str(porta))
    if id == 1:
        cache4096 = ''
    elif id == 2:
        cache4097 = ''
    elif id == 3:
        cache4098 = ''
    elif id == 4:
        cache4099 = ''
    else:
        cache4100 = ''

def removerEstadosAntigos():
    global cache4096, cache4097, cache4098, cache4099, cache4100, contadorRemove
    caches = [4097, 4098, 4099, 4100]
    while True:
        time.sleep(60)
        contadorRemove += 1
        i = 0;
        while i < (len(caches)-1):
            if identificarPeer(caches[i]) != '':
                peer, cont, estado = separarMsg(identificarPeer(caches[i]).encode())
                if int(cont) < contadorRemove:
                    resetCache(caches[i])
                    print("\n4:Removendo estado antigo do peer",idPeer(peer))
            i +=1

def idPeer(peer):
    id = int((peer[::-1])[0])
    if id == 6:
        return 1
    elif id == 7:
        return 2
    elif id == 8:
        return 3
    elif id ==9:
        return 4
    else:
        return 5

def construirMsg(peer, status):
    global contador
    return str(peer)+"#"+str(contador)+"#"+status

def separarMsg(estado):
    peer, contador, estado = (estado.decode()).split('#')
    return peer, contador, estado

def estado(porta):
    while True:
        time.sleep(20)
        global cache4096
        status = glob.glob("/home/zanoni/PEER1/*")
        msg = construirMsg(porta, ''.join(status))
        cache4096 = msg.encode()
        print("\n1:Estado do peer atualizado")

def escolherPeer():
    lista = [4097, 4098, 4099, 4100]
    return random.choice(lista)

def identificarPeer(peer):
    global cache4096, cache4097, cache4098, cache4099, cache4100
    if peer == 4097:
        return cache4097
    elif peer == 4098:
        return cache4098
    elif peer == 4099:
        return cache4099
    else:
        return cache4100

def enviarMetadados():
    global cache4096, contador
    while True:
        time.sleep(30)
        contador += 1
        peer = escolherPeer()
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server_address = ('localhost', peer)
        try:
            sent = s.sendto(cache4096, server_address)
            print("\n2:Enviando dados para o peer",idPeer(str(peer)))
        finally:
            s.close()

def enviarMetadadosTerceiros():
    while True:
        time.sleep(40)
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        peer1 = escolherPeer()
        peer2 = escolherPeer()
        while peer1 == peer2:
            peer2 = escolherPeer()
        server_address = ('localhost', peer1)
        estado = identificarPeer(peer2)
        if estado == '':
            estado = construirMsg(peer2, estado)
        try:
            sent = s.sendto(estado.encode(), server_address)
            print("\n3:Enviando estado do peer",idPeer(str(peer2)),"para o peer",
                    idPeer(str(peer1)))
        finally:
            s.close()

def receberMetadados(port, port_rcv):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = ('localhost', port)
    s.bind(server_address)
    while True:
        data, address = s.recvfrom(port_rcv)
        peer, contador, estado = separarMsg(data)
        print("\nRecebendo estado do peer",idPeer(peer),"\nDados:",estado)
        guardarMetadados(data.decode(), peer)

def guardarMetadados(dados, peer):
    global cache4096, cache4097, cache4098, cache4099, cache4100
    estadoAtual = identificarPeer(int(peer))
    if estadoAntigo(dados, estadoAtual):
        peer = idPeer(peer)
        if peer == 1:
            if dados!= cache4096:
                cache4096 = dados
        elif peer == 2:
            if dados!= cache4097:
                cache4097 = dados
        elif peer == 3:
            if dados!= cache4098:
                cache4098 = dados
        elif peer == 4:
            if dados!= cache4099:
                cache4099 = dados
        elif peer == 5:
            if dados!= cache4100:
                cache4100 = dados

if __name__ == "__main__":

    ThreadEstado = Thread(target=estado, args=[4096])
    ThreadEstado.start()
    ThreadEnviarMetadados = Thread(target=enviarMetadados)
    ThreadEnviarMetadados.start()
    ThreadEnviarMetadadosTerceiros = Thread(target=enviarMetadadosTerceiros)
    ThreadEnviarMetadadosTerceiros.start()
    ThreadReceberMetadados1 = Thread(target=receberMetadados, args=(14096,4097))
    ThreadReceberMetadados1.start()
    ThreadReceberMetadados1 = Thread(target=receberMetadados, args=(24096,4098))
    ThreadReceberMetadados1.start()
    ThreadReceberMetadados1 = Thread(target=receberMetadados, args=(34096,4099))
    ThreadReceberMetadados1.start()
    ThreadReceberMetadados1 = Thread(target=receberMetadados, args=(44096,4100))
    ThreadReceberMetadados1.start()
    ThreadRemoverEstados = Thread(target=removerEstadosAntigos)
    ThreadRemoverEstados.start()
