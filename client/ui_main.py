"""
    DESCRIPTION: 
        CLIENTE
            --> RESPONSAVEL POR ENVIAR AO SERVIDOR OPCOES ESCOLHIDAS PELO USARIO NO BANCO,
            --> ATRAVES DE INTERFACE GRAFICA. 
"""
 
"""
    Autor: David Pereira
    Data: 23/05/2021
    Disciplina: POO2
"""

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtCore import QCoreApplication

import socket
import json


from tela_autenticar import Tela_autenticar
from tela_cadastro import Tela_cadastro
from tela_deposito import Tela_deposito
from tela_extrato import Tela_extrato
from tela_inicial import Tela_inicial
from tela_menu import Tela_menu
from tela_sacar import Tela_sacar
from tela_transferir import Tela_transferir


class Ui_Main(QtWidgets.QWidget):
    def setupUi(self, Main):
        Main.setObjectName('Main')
        Main.resize(640, 480)

        self.QtStack = QtWidgets.QStackedLayout()

        self.stack0 = QtWidgets.QMainWindow()
        self.stack1 = QtWidgets.QMainWindow()
        self.stack2 = QtWidgets.QMainWindow()
        self.stack3 = QtWidgets.QMainWindow()
        self.stack4 = QtWidgets.QMainWindow()
        self.stack5 = QtWidgets.QMainWindow()
        self.stack6 = QtWidgets.QMainWindow()
        self.stack7 = QtWidgets.QMainWindow()

        self.tela_inicial = Tela_inicial()
        self.tela_inicial.setupUi(self.stack0)

        self.tela_cadastro = Tela_cadastro()
        self.tela_cadastro.setupUi(self.stack1)

        self.tela_autenticar = Tela_autenticar()
        self.tela_autenticar.setupUi(self.stack2)

        self.tela_menu = Tela_menu()
        self.tela_menu.setupUi(self.stack3)

        self.tela_sacar = Tela_sacar()
        self.tela_sacar.setupUi(self.stack4)
        
        self.tela_deposito = Tela_deposito()
        self.tela_deposito.setupUi(self.stack5)

        self.tela_transferir = Tela_transferir()
        self.tela_transferir.setupUi(self.stack6)

        self.tela_extrato = Tela_extrato()
        self.tela_extrato.setupUi(self.stack7)

        self.QtStack.addWidget(self.stack0)
        self.QtStack.addWidget(self.stack1)
        self.QtStack.addWidget(self.stack2)
        self.QtStack.addWidget(self.stack3)
        self.QtStack.addWidget(self.stack4)
        self.QtStack.addWidget(self.stack5)
        self.QtStack.addWidget(self.stack6)
        self.QtStack.addWidget(self.stack7)


class Main(QMainWindow, Ui_Main):
    """
        DESCRIPTION: 
            --> Responsavel por as operacoes escolhidas na interface.
    """
    
    def __init__(self, parent=None):
        """
            DESCRIPTION: 
                --> este metodo realiza a conexão com o servidor.
        """

        super(Main, self).__init__(parent)
        self.setupUi(self)

        ip = "localhost"
        port = 8000
        addr = ((ip, port))  
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(addr)  

        self.tela_inicial.pushButton.clicked.connect(self.Abrir_TelaCadastro)
        self.tela_inicial.pushButton_2.clicked.connect(self.Abrir_TelaAutenticar)


    def Abrir_TelaCadastro(self):
        """
            DESCRIPTIONS: 
                --> duas opcoes estarao disponiveis:
                    --> chama o metodo botao_cadastrar;
                    --> sair da tela de cadastro.
        """
        self.QtStack.setCurrentIndex(1)
        self.tela_cadastro.pushButton.clicked.connect(self.botao_cadastrar)
        self.tela_cadastro.pushButton_2.clicked.connect(self.Sair_telaCadastro)


    def botao_cadastrar(self):
        """
            DESCRIPTIONS: 
                --> metodo responsavel por receber os dados do cliente (atraves da interface, botao CADASTRAR) e enviar para o servidor com a biblioteca json
                
                --> a variavel received retornara uma mensagem contendo o resultado do envio dos dados, se o cliente foi cadastrado ou nao.
        """

        nome = self.tela_cadastro.lineEdit.text()
        sobrenome = self.tela_cadastro.lineEdit_2.text()
        cpf = self.tela_cadastro.lineEdit_3.text()

        if not ((nome == '') or (sobrenome == '') or (cpf == '')):
            dicionario = {"action": "cadastro", "nome": nome, "sobrenome": sobrenome, "cpf": cpf}
            dicionario = json.dumps(dicionario)
            self.client_socket.send(dicionario.encode())
            
            received = self.client_socket.recv(1024).decode()

            if (received):
                QMessageBox.information(None, "POOII", received)
        
        self.Sair_telaCadastro()
        

    def Sair_telaCadastro(self):
        """
            DESCRIPTION: 
                --> este metodo fica responsavel por sair da tela de cadastro quando cliente seleciona botao de sair.
        """
        self.QtStack.setCurrentIndex(0)
        
        self.tela_cadastro.lineEdit.setText("")
        self.tela_cadastro.lineEdit_2.setText("")
        self.tela_cadastro.lineEdit_3.setText("")


    def Abrir_TelaAutenticar(self):
        """
            DESCRIPTIONS:
                --> duas opcoes estarao disponiveis:
                    --> chama o metodo entrar em conta;
                    --> sair da tela autentificar.
        """
        self.QtStack.setCurrentIndex(2)
        self.tela_autenticar.pushButton.clicked.connect(self.Entrar_conta)
        self.tela_autenticar.pushButton_2.clicked.connect(self.Sair_TelaAutenticar)

    
    def Entrar_conta(self):
        """
            DESCRIPTIONS:
                --> cliente so entrara na conta atraves do seu cpf.

                --> o primeiro envio de informacoes pro servidor e para verificar se o cpf que o cliente informou se encontra na lista.

                --> se cliente foi autentificado:
                        servidor recebera uma mensagem que o cliente entrou em sua conta
                        apos isso abrira a tela menu para o cliente.
                --> senao:
                        cliente recebera uma mensagem sendo informado que o cpf digitado existe no sistema.
        """
        cpf = self.tela_autenticar.lineEdit.text()

        dicionario = {"action": "autenticar", "cpf": cpf}
        dicionario = json.dumps(dicionario)
        self.client_socket.send(dicionario.encode())

        
        received = self.client_socket.recv(1024).decode()
        received = json.loads(received)

        if (received["autenticado"] == True):
            self.abrir_Menu()

        QMessageBox.information(None, "POOII", received["msg"])
        

    def Sair_TelaAutenticar(self):
        """
            DESCRIPTION:  
                --> sai da tela de autentificacao se o cliente selecionar a opcao de voltar/sair.
        """
        self.tela_autenticar.lineEdit.setText("")
        self.QtStack.setCurrentIndex(0)
    

    # Menu
    def abrir_Menu(self):
        """
            DESCRIPTIONS:
                --> responsavel por todas as operacoes que o cliente deseja no menu do banco.
                
                --> aqui redireciona para as funcionalidades do banco de acordo com o que o cliente selecionar.
        """
        self.QtStack.setCurrentIndex(3)
        self.tela_autenticar.lineEdit.setText("")
        self.tela_menu.pushButton.clicked.connect(self.Abrir_telaSaque)
        self.tela_menu.pushButton_2.clicked.connect(self.Abrir_telaDeposito)
        self.tela_menu.pushButton_3.clicked.connect(self.Abrir_telaTransferir)
        self.tela_menu.pushButton_4.clicked.connect(self.Abrir_telaExtrato)

        self.tela_menu.pushButton_5.clicked.connect(self.Sair_Menu)


    def Sair_Menu(self):
        """
            DESCRIPTION:  
                --> Se selecionado esse botao, saira da conta e o servidor recebera uma mensagem que cliente saiu de sua conta.
        """
        self.conta = None
        self.tela_autenticar.lineEdit.setText("")
        dicionario = {"action": "sair"}
        dicionario = json.dumps(dicionario)
        self.client_socket.send(dicionario.encode())

        received = self.client_socket.recv(1024).decode()
        self.QtStack.setCurrentIndex(0)

    
    def Abrir_telaSaque(self):
        """
            DESCRIPTIONS:
                --> Selecionado o botao de SAQUE, duas opcoes estarao disponiveis:
                    --> redirecionara para o metodo SACAR;
                    -->  saira da tela de SAQUE e abrira o menu.
        """
        self.QtStack.setCurrentIndex(4)
        self.tela_sacar.pushButton.clicked.connect(self.botao_sacar)
        self.tela_sacar.pushButton_2.clicked.connect(self.abrir_Menu)


    def botao_sacar(self):
        """
            DESCRIPTIONS:
                --> Responsavel pelo saque, recebera primeiramente o valor do saque atraves da variavel SAQUE.

                --> Envia para o servidor a opcao de saque e o valor do saque.

                --> Servidor retorna uma mensagem informando se o saque foi realizado com sucesso ou nao.

                --> Apos isso, saira da tela de saque e voltara para o menu. 
        """
        saque = self.tela_sacar.lineEdit.text()

        if (saque != ""):
            saque = float(saque)
            dicionario = {"action": "saque", "valor": saque}
            dicionario = json.dumps(dicionario)
            self.client_socket.send(dicionario.encode())

            received = self.client_socket.recv(1024).decode()

            QMessageBox.information(None, "POOII", received)
            self.tela_sacar.lineEdit.setText("")

        self.abrir_Menu()


    def Abrir_telaDeposito(self):
        """
        DESCRIPTIONS: 
            --> Selecionado o botao de DEPOSITO, duas opcoes estarao disponiveis:
                --> redirecionara para o metodo DEPOSITAR;
                --> saira da tela de DEPOSITO e abrira o menu.
        """
        self.QtStack.setCurrentIndex(5)
        self.tela_deposito.pushButton.clicked.connect(self.botao_depositar)
        self.tela_deposito.pushButton_2.clicked.connect(self.abrir_Menu)


    def botao_depositar(self):
        """
            DESCRIPTIONS: 
                --> Responsavel pelo deposito, recebera primeiramente o valor do deposito atraves da variavel DEPOSITO.

                --> Envia para o servidor a opcao de deposito e o valor do deposito.

                --> Servidor retorna uma mensagem informando que o deposito foi realizado com sucesso.

                --> Apos isso, saira da tela de deposito e voltara para o menu.
        """
        deposito = self.tela_deposito.lineEdit.text()

        if (deposito != ""):
            deposito = float(deposito)
            dicionario = {"action": "deposito", "valor": deposito}
            dicionario = json.dumps(dicionario)
            self.client_socket.send(dicionario.encode())

            received = self.client_socket.recv(1024).decode() 

            QMessageBox.information(None, "POOII", received)        
        
        self.tela_deposito.lineEdit.setText("")
        self.abrir_Menu()


    def Abrir_telaTransferir(self):
        """
            DESCRIPTIONS: 
                --> Selecionado o botao de TRANSFERIR, duas opcoes estarao disponiveis:
                    --> redirecionara para o metodo TRANSFERIR;
                    --> saira da tela de TRANSFERIR e abrira o menu.
        """
        self.QtStack.setCurrentIndex(6)
        self.tela_transferir.pushButton.clicked.connect(self.botao_transferir)
        self.tela_transferir.pushButton_2.clicked.connect(self.abrir_Menu)


    def botao_transferir(self):
        """
            DESCRIPTIONS:
                --> Responsavel pela transferencia, recebera primeiramente recebe o cpf da conta que sera transferida o valor atraves da variavel CPF e em seguida o valor da transferencia com a variavel VALOR.
                
                --> Envia para o servidor a opcao de transferir juntamente com o cpf da conta do que ira receber a transferencia e o valor.
                
                --> Servidor retorna uma mensagem informando que se a transferencia foi realizada ou se o saldo e insuficiente.
                
                --> Apos isso, saira da tela de transferir e voltara para o menu.
        """
        cpf = self.tela_transferir.lineEdit.text()
        valor = float(self.tela_transferir.lineEdit_2.text())

        dicionario = {"action": "transferir", "cpf": cpf, "valor": valor}   
        dicionario = json.dumps(dicionario)
        self.client_socket.send(dicionario.encode())

        received = self.client_socket.recv(1024).decode()

        flag = 0
 
        if not ((cpf == "") or (valor == "")):
            QMessageBox.information(None, "POOII", received)

        self.tela_transferir.lineEdit.setText("")
        self.abrir_Menu()


    def Abrir_telaExtrato(self):
        """
            DESCRIPTION:
                --> Abrira a tela de extrato exibindo todas as informacoes bancarias do cliente.
        """
        self.QtStack.setCurrentIndex(7)

        dicionario = {"action": "extrato"}
        dicionario = json.dumps(dicionario)
        self.client_socket.send(dicionario.encode())        

        received = self.client_socket.recv(1024).decode()
        received = json.loads(received)

        self.tela_extrato.lineEdit.setText(received["nome"])
        self.tela_extrato.lineEdit_2.setText(received["cpf"])
        self.tela_extrato.lineEdit_3.setText(received["numero"])
        self.tela_extrato.lineEdit_4.setText(str(received["saldo"]))
        self.tela_extrato.lineEdit_5.setText(str(received["limite"]))

        self.tela_extrato.pushButton.clicked.connect(self.sair_telaExtrato)


    def sair_telaExtrato(self):
        """
        DESCRIPTION:
            Metodo responsavel somente pra sair da tela de extrato se o cliente assim desejar.
        """
        self.QtStack.setCurrentIndex(3)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    show_main = Main()
    sys.exit(app.exec_())
