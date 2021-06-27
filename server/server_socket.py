import socket
import json
import threading

from pessoa import Pessoa
from conta import Conta


class ClientThreading(threading.Thread):

    def __init__(self, clientAddress, clientsocket, sinc):
        threading.Thread.__init__(self)

        self._clientAddress = clienteAddress
        self._csocket = clientsocket
        self._sinc = sinc
        print("Nova conexão: ", clientAddress)
        
        self._contas = Conta()
        self._cpf_autenticado = None


    def run(self):
        while True:
            received = json.loads(self._csocket.recv(1024).decode())
            
            if received["action"] == "cadastro":
                self.registrar(received)
            elif received["action"] == "autenticar":        
                self.autenticar(received)
            elif received["action"] == "saque":
                self._sinc.acquire()
                self.saque(received)
                self._sinc.release()
            elif received["action"] == "deposito":
                self._sinc.acquire()
                self.deposito(received)
                self._sinc.release()
            elif received["action"] == "transferir":
                self._sinc.acquire()
                self.transferir(received)
                self._sinc.release()
            elif received["action"] == "extrato":
                self.extrato()
            elif received["action"] == "sair":
                self.sair()


    def registrar(self, received):
        cliente = Pessoa(received["nome"], received["sobrenome"], received["cpf"])
                
        if self._contas.cadastra(cliente):
            msg = "Cadastro realizado com sucesso!"
        else:
            msg = "Este CPF já foi cadastrado antes"

        print(msg)
        self._csocket.send(msg.encode())


    def autenticar(self, received):
        dicionario = {}
        conta = self._contas.busca(received["cpf"])

        if (conta):
            self._contas.atualizar_conta(True, conta[0])
            self._cpf_autenticado = conta[4]
            
            dicionario["autenticado"] = True
            dicionario["msg"] = f"{conta[2]} autenticado com sucesso!"
        else:
            dicionario["autenticado"] = False
            dicionario["msg"] = f"Esse CPF ainda não foi cadastrado!" 

        print(dicionario["msg"])
        dicionario = json.dumps(dicionario)
        self._csocket.send(dicionario.encode())

    
    def saque(self, received):
        saque = self._contas.sacar(self._cpf_autenticado, received["valor"]) 
        
        if (saque):
            msg = "Saque efetuado com sucesso!"
        else:
            msg = "Saldo insuficiente!"
        
        print(msg)
        self._csocket.send(msg.encode())


    def deposito(self, received):
        
        self._contas.deposito(self._cpf_autenticado, received["valor"])
        msg = "Depósito efetuado com sucesso!"

        print(msg)
        self._csocket.send(msg.encode())


    def transferir(self, received):
        conta = self._contas.busca(received["cpf"])

        if conta:
            if self._contas.transferir(self._cpf_autenticado, received["cpf"], received["valor"]):
                msg = "Transferência efetuada com sucesso!"
            else:
                msg = "Saldo para transferência insuficiente"
        else:
            msg = "CPF não encontrado!"
        
        print(msg)
        self._csocket.send(msg.encode())


    def extrato(self):
        dicionario = dict()

        conta = self._contas.busca(self._cpf_autenticado)
        dicionario["numero"] = conta[1]
        dicionario["nome"] = f"{conta[2]} {conta[3]}"
        dicionario["cpf"] = conta[4]
        dicionario["saldo"] = conta[5]
        dicionario["limite"] = conta[6]

        dicionario = json.dumps(dicionario)
        self._csocket.send(dicionario.encode())


    def sair(self):
        conta = self._contas.busca(self._cpf_autenticado)
        self._contas.atualizar_conta(False, conta[0])
        
        self._cpf_autenticado = None

        msg = f"{conta[2]} saiu da conta!"
        print(msg)
        self._csocket.send(msg.encode())
        self._contas.mostrar_contas()


if __name__ == "__main__":
    host = "localhost"
    port = 8000
    addr = (host, port)
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  
    serv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)    
    serv_socket.bind(addr)
    sinc = threading.Lock()
    print("servidor iniciando")
    print("Aguardando nova conexão")

    while True:
        serv_socket.listen(10)  

        clientSocket, clienteAddress = serv_socket.accept()  
        newthread = ClientThreading(clienteAddress, clientSocket, sinc)
        newthread.start()
