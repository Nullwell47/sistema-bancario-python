import textwrap

# Função que exibe o menu e retorna a opção selecionada pelo usuário.
def menu():
    menu = """
    ================ MENU ================
    [1]\tDepositar 
    [2]\tSacar 
    [3]\tExtrato
    [4]\tNova conta
    [5]\tListar contas
    [6]\tNovo usuário
    [0]\tSair
    ==> """
    return input(textwrap.dedent(menu))

# Função para realizar um depósito em uma conta.
def depositar(saldo, valor, extrato, /):
    if valor > 0:
        saldo += valor  # Incrementa o saldo
        extrato += f"Depósito: R$ {valor:.2f}\n"  # Adiciona registro no extrato
        print("\n=== Depósito realizado com sucesso! ===")
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

# Função para realizar um saque em uma conta.
def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    excedeu_saldo = valor > saldo  # Verifica se o valor do saque excede o saldo disponível
    excedeu_limite = valor > limite  # Verifica se o valor do saque excede o limite
    excedeu_saques = numero_saques >= limite_saques  # Verifica se excedeu o número máximo de saques

    if excedeu_saldo:
        print("\n@@@ Operação falhou! Você não tem saldo suficiente. @@@")
    
    elif excedeu_limite:
        print("\n@@@ Operação falhou! O valor do saque excede o limite. @@@")
    
    elif excedeu_saques:
        print("\n@@@ Operação falhou! Número máximo de saques excedido. @@@")

    elif valor > 0:
        saldo -= valor  # Decrementa o saldo
        extrato += f"Saque: R$ {valor:.2f}\n"  # Adiciona registro no extrato
        numero_saques += 1  # Incrementa o contador de saques
        print("\n=== Saque realizado com sucesso! ===")
    
    else:
        print("\n@@@ Operação falhou! O valor informado é inválido. @@@")
    return saldo, extrato

# Função para exibir o extrato de uma conta.
def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    print("Não foram realizados movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

# Função para criar um novo usuário e adicioná-lo à lista de usuários.
def criar_usuario(usuarios):
    cpf = input("Informe o CPF (somente números): ")
    usuario = filtrar_usuario(cpf, usuarios) # Verifica se já existe um usuário com o CPF informado.

    if usuario:
        print("\n@@@ Já existe usuário com esse CPF! @@@")
        return
    
    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereco (logradouro, nro - bairro - cidade/sigla estado): ")
    
    # Cria um dicionário com as informações do usuário e o adiciona à lista de usuários.
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco}) 

    print("=== Usuário criado com sucesso! ===")

# Função para filtrar um usuário com base no CPF.
def filtrar_usuario(cpf, usuarios):
    # Cria uma lista de usuários filtrados, que contém todos os usuários com o CPF especificado.
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    # Retorna o primeiro usuário da lista filtrada, se houver algum, ou retorna None se não houver nenhum.
    return usuarios_filtrados[0] if usuarios_filtrados else None

# Função para criar uma nova conta e associá-la a um usuário.
def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if usuario:
        print("\n=== Conta criada com sucesso! ===")
        return {"agencia": agencia, "numero_conta": numero_conta, "usuario": usuario}
    
    print("\n@@@ Usuário não encontrado, fluxo de criação de conta encerrado! @@@")

# Função para listar todas as contas.
def listar_contas(contas):
    for conta in contas: 
# Monta uma linha formatada com informações da conta, incluindo agência, número da conta e o nome do titular da conta, usando a sintaxe de f-string.
        linha = f"""\
            Agência:\t{conta['agencia']}
            C/C:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
        """
        print("=" * 100) # Imprime uma linha de igual (===) para separar as informações de cada conta.
        print(textwrap.dedent(linha)) # Imprime as informações da conta, usando textwrap.dedent para formatar corretamente a string.

# Função principal que gerencia as operações bancárias.
def main():
    # Variáveis
    LIMITE_SAQUES = 3  # Número máximo de saques permitidos
    AGENCIA = "0001"

    saldo = 0  # Saldo inicial
    limite = 500  # Limite de saque
    extrato = ""  # Registro das transações
    numero_saques = 0  # Contador de saques
    usuarios = [] # Armazena usuário
    contas = [] # Armazena conta

    # Loop principal do programa
    while True:
        opcao = menu()

        # Opção 1: Depositar
        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            
            saldo, extrato = depositar(saldo, valor, extrato)

        # Opção 2: Sacar
        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            saldo, extrato = sacar(
                saldo=saldo,
                valor=valor,
                extrato=extrato,
                limite=limite,
                numero_saques=numero_saques,
                limite_saques=LIMITE_SAQUES,
            )           

        # Opção 3: Extrato
        elif opcao == "3":
            exibir_extrato(saldo, extrato=extrato)

        # Opção 6: Novo usuário
        elif opcao == "6":
            criar_usuario(usuarios)

        # Opção 4: Nova conta
        elif opcao == "4":
            numero_conta = len(contas) + 1
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)

        # Opção 5: Listar Contas
        elif opcao == "5":
            listar_contas(contas)

        # Opção 0: Sair
        elif opcao == "0":
            break

        # Opção inválida
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
