from pessoa import Pessoa
import psycopg2


class Conta:

    def __init__ (self):
        self._connection = psycopg2.connect(database="usuarios", user="ulyana", password="123", host="localhost", port=5432)

        self.cursor = self._connection.cursor()

        sql_table = """CREATE TABLE IF NOT EXISTS usuarios(
                       id serial PRIMARY KEY,
                       numero text NOT NULL, 
                       nome text NOT NULL,
                       sobrenome text NOT NULL,
                       cpf text NOT NULL,
                       saldo float NOT NULL,
                       limite float NOT NULL,
                       conta_autenticada bool);"""

        self.cursor.execute(sql_table)


    def cadastra(self, cliente):
        existe_conta = self.busca(cliente.cpf)

        if not existe_conta:
            self.cursor.execute("INSERT INTO usuarios (numero, nome, sobrenome, cpf, saldo, limite, conta_autenticada) VALUES (%s, %s, %s, %s, %s, %s, %s)", ("123-4", cliente.nome, cliente.sobrenome, cliente.cpf, 10, 1000, False))

            self._connection.commit()
            return True
        else:
            return False
    

    def busca(self, cpf):
        self.cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf))
        
        for conta in self.cursor:
            return conta


    def mostrar_contas(self):
        self.cursor.execute("SELECT * FROM usuarios")

        for conta in self.cursor:
            print(conta)


    def sacar(self, cpf, valor):  
        self.cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", cpf)
        
        for c in self.cursor:
            if c[5] >= valor:
                self.cursor.execute("UPDATE usuarios SET saldo = %s WHERE id = %s", (c[5] - valor, c[0]))
                self._connection.commit()
                return True
            else:
                return False


    def deposito(self, cpf, valor):  
        self.cursor.execute("SELECT * FROM usuarios WHERE cpf = %s", (cpf))

        for c in self.cursor:
            new_valor = c[5]

        self.cursor.execute("UPDATE usuarios SET saldo = %s WHERE id = %s", (new_valor + valor, c[0]))
        self._connection.commit()


    def transferir(self, cpf_origem, cpf_destino, valor):
        if (self.sacar(cpf_origem, valor)):
            self.deposito(cpf_destino, valor)
            return True
        else:
            return False


    def atualizar_conta(self, valor, id):
        self.cursor.execute("UPDATE usuarios SET conta_autenticada = %s WHERE id = %s", (valor, id))
        self._connection.commit()
