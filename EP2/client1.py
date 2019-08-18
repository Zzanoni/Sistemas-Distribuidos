import random, socket, time

def consultar(arquivo):#nome do arquivo
    s = socket.socket()
    host = socket.gethostname()
    listaPorts =  escolherPeers() #escolha aleatoria do peer

    s.connect((host, listaPorts[0]))
    del(listaPorts[0])
    msg = arquivo+"#"+str(12345)+"#"+str(0)+"#"+str(listaPorts)
    s.send(msg.encode())
    retorno = (s.recv(1024)).decode()
    s.close()
    if retorno == '0':
        print("\nArquivo não encontrado\n")
    elif retorno == '1':
        print("\nArquivo encontrado\n")
        baixarArquivo(arquivo)

def baixarArquivo(arquivo): #nome do arquivo
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12346
    s.bind((host, port))
    while True:
        s.listen()
        peer, address = s.accept()
        file = open('CLIENTE1/'+arquivo, 'wb')
        print("Recebendo arquivo...\n")
        while True:
            part = peer.recv(1024)
            if not part:
                break
            file.write(part)
        file.close()
        print("Arquivo recebido\n")
        peer.close()
        break


def escolherPeers(): #escolha aleatoria do peer
    listaPeers = [4090, 4091, 4092, 4093, 4094, 4095, 4096, 4097, 4098, 4099]
    lista = []
    i = 0
    while i < 4:
        index = random.randint(0, 9-i)
        lista.append(listaPeers[index])
        del(listaPeers[index])
        i+=1
    return lista

if __name__ == "__main__":
    while True:
        arquivo = input("Digite o arquivo desejado: ")
        consultar(arquivo)
