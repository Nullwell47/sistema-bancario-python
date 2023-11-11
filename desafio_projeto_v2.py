import textwrap
from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime

# Classe base representando um Cliente
class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []  # Lista de contas associadas ao cliente

    # Realiza uma transação em uma conta específica
    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    # Adiciona uma nova conta para o cliente
    def adicionar_conta(self, conta):
        self.contas.append(conta)

# Classe para representar uma Pessoa Física que é um cliente
class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf

# Classe representando uma conta genérica
class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()  # Instância para manter o histórico de transações

    # Método de classe para criar uma nova conta
    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    # Propriedades para acessar informações da conta
    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    # Realiza um saque na conta
    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")

        return False

    # Realiza um depósito na conta
    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\n=== Depósito realizado com sucesso! ===")
        else:
            print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
            return False

        return True

# Classe que representa uma Conta Corrente, um tipo específico de conta
class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self._limite = limite
        self._limite_saques = limite_saques

    # Sobrescreve o método de sacar para uma conta corrente
    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self._limite
        excedeu_saques = numero_saques >= self._limite_saques

        if excedeu_limite:
            print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")

        elif excedeu_saques:
            print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

        else:
            return super().sacar(valor)

        return False

    # Retorna uma representação em string da conta corrente
    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """

# Classe para manter o histórico de transações
class Historico:
    def __init__(self):
        self._transacoes = []  # Lista de transações

    @property
    def transacoes(self):
        return self._transacoes

    # Adiciona uma nova transação ao histórico
    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%s"),
            }
        )

# Classe abstrata para representar uma transação
class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass

# Classe que representa um saque, uma subclasse de Transacao
class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    # Registra um saque na conta
    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Classe que representa um depósito, uma subclasse de Transacao
class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    # Registra um depósito na conta
    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

# Função para exibir o menu
def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [nu]\tNovo usuário
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

# Função para filtrar cliente por CPF
def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

# Função para recuperar a conta de um cliente
def recuperar_conta_cliente(cliente):
    if not cliente.contas:
        print("\n@@@ Cliente não possui conta! @@@")
        return

    # FIXME: não permite cliente escolher a conta
    return cliente.contas[0]

# Função para realizar um depósito na conta do cliente
def depositar(clientes):
    # Solicita o CPF do cliente para identificação
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)  # Busca o cliente com base no CPF fornecido

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")  # Se o cliente não for encontrado, exibe uma mensagem de erro
        return

    valor = float(input("Informe o valor do depósito: "))  # Solicita o valor a ser depositado
    transacao = Deposito(valor)  # Cria uma instância de transação de depósito com o valor fornecido

    conta = recuperar_conta_cliente(cliente)  # Recupera a conta associada ao cliente
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)  # Realiza a transação de depósito na conta do cliente

# Função para realizar um saque na conta do cliente
def sacar(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    valor = float(input("Informe o valor do saque: "))
    transacao = Saque(valor)

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    cliente.realizar_transacao(conta, transacao)

# Função para exibir o extrato da conta do cliente
def exibir_extrato(clientes):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado! @@@")
        return

    conta = recuperar_conta_cliente(cliente)
    if not conta:
        return

    print("\n================ EXTRATO ================")
    transacoes = conta.historico.transacoes

    extrato = ""
    if not transacoes:
        extrato = "Não foram realizadas movimentações."
    else:
        for transacao in transacoes:
            extrato += f"\n{transacao['tipo']}:\n\tR$ {transacao['valor']:.2f}"

    print(extrato)
    print(f"\nSaldo:\n\tR$ {conta.saldo:.2f}")
    print("==========================================")

# Função para criar um novo cliente
def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\n@@@ Já existe cliente com esse CPF! @@@")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    cliente = PessoaFisica(nome=nome, data_nascimento=data_nascimento, cpf=cpf, endereco=endereco)

    clientes.append(cliente)  # Adiciona o novo cliente à lista de clientes

    print("\n=== Cliente criado com sucesso! ===")

# Função para criar uma nova conta
def criar_conta(numero_conta, clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\n@@@ Cliente não encontrado, fluxo de criação de conta encerrado! @@@")
        return

    conta = ContaCorrente.nova_conta(cliente=cliente, numero=numero_conta)
    contas.append(conta)  # Adiciona a nova conta à lista de contas
    cliente.contas.append(conta)  # Associa a nova conta ao cliente

    print("\n=== Conta criada com sucesso! ===")

# Função para listar as contas disponíveis
def listar_contas(contas):
    for conta in contas:
        print("=" * 100)
        print(textwrap.dedent(str(conta)))

# Função principal para executar o programa
def main():
    clientes = []  # Lista de clientes
    contas = []  # Lista de contas

    while True:
        opcao = menu()  # Exibe o menu e obtém a opção escolhida pelo usuário

        if opcao == "d":
            depositar(clientes)  # Chama a função para realizar um depósito

        elif opcao == "s":
            sacar(clientes)  # Chama a função para realizar um saque

        elif opcao == "e":
            exibir_extrato(clientes)  # Chama a função para exibir o extrato da conta

        elif opcao == "nu":
            criar_cliente(clientes)  # Chama a função para criar um novo cliente

        elif opcao == "nc":
            numero_conta = len(contas) + 1
            criar_conta(numero_conta, clientes, contas)  # Chama a função para criar uma nova conta

        elif opcao == "lc":
            listar_contas(contas)  # Chama a função para listar as contas

        elif opcao == "q":
            break  # Encerra o loop, finalizando o programa

        else:
            print("\n@@@ Operação inválida, por favor selecione novamente a operação desejada. @@@")

main()  # Inicia a execução do programa

