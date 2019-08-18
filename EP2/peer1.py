import socket, os, time, random
from threading import Thread


estado = ''

def converterLista(lista):
    lista = lista[1:-1]
    listaPorts = []
    listaPorts = lista.split(',')
    i = 0
    lista = []
    while i < len(listaPorts):
        lista.append(int(listaPorts[i]))
        i+=1
    return lista

def obterMetadados():
    global estado
    estado = os.listdir('PEER1/')

def consultarArquivo(arquivo):
    global estado
    i = 0
    while (i<len(estado)):
        if arquivo == estado[i]:
            return True
        i+=1
    return False

def verificarArquivo():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 4091
    s.bind((host, port))
    while True:
        s.listen()
        cliente, address = s.accept()
        msg = cliente.recv(1024)
        arquivo, porta, str_ttl, listaPorts = msg.decode().split('#')
        ttl = int(str_ttl)
        if ttl > 2:
            print("Tempo excedido\n")
            cliente.send('0'.encode())
        else:
            ttl = ttl + 1
            if consultarArquivo(arquivo):
                cliente.send('1'.encode())
                enviarArquivo(int(porta)+1, arquivo)
            else:
                lista = converterLista(listaPorts)
                peer = lista[0]
                del(lista[0])
                print("Repassando consulta para outro peer\n")
                retorno = repassarConsulta(arquivo, porta, ttl, peer, lista)
                cliente.send(retorno)
    s.close()

def repassarConsulta(arquivo, cliente, ttl, peer, listaPorts):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    s.connect((host, peer))
    msg = str(arquivo)+"#"+str(cliente)+"#"+str(ttl)+"#"+str(listaPorts)
    s.send(msg.encode())
    retorno = s.recv(1024)
    s.close()
    return retorno

def enviarArquivo(cliente, arquivo): #porta do cliente, nome do arquivo
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    time.sleep(2)
    s.connect((host, cliente))
    file = open('PEER1/'+arquivo, 'rb')
    print("Enviando arquivo...\n")
    part = file.read(1024)
    while True:
        s.send(part)
        part = file.read(1024)
        if not part:
            break
    print("Arquivo enviado\n")
    file.close()
    s.close()

if __name__ == "__main__":
    obterMetadados()
    ThreadEstado = Thread(target=obterMetadados)
    ThreadEstado.start()
    ThreadVerificarArquivo = Thread(target=verificarArquivo)
    ThreadVerificarArquivo.start()
