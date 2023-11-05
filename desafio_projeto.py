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

# Função principal que gerencia as operações bancárias.
def main():
    # Variáveis
    LIMITE_SAQUES = 3  # Número máximo de saques permitidos
    AGENCIA = "0001"

    saldo = 0  # Saldo inicial
    limite = 500  # Limite de saque
    extrato = ""  # Registro das transações
    numero_saques = 0  # Contador de saques
    usuarios = [] 
    contas = []

    # Loop principal do programa
    while True:
        opcao = menu()

        # Opção 1: Depositar
        if opcao == "1":
            valor = float(input("Informe o valor do depósito: "))
            
            if valor > 0:
                saldo += valor  # Incrementa o saldo
                extrato += f"Depósito: R$ {valor:.2f}\n"  # Adiciona registro no extrato
            else:
                print("Operação falhou! O valor informado é inválido.")

        # Opção 2: Sacar
        elif opcao == "2":
            valor = float(input("Informe o valor do saque: "))

            excedeu_saldo = valor > saldo  # Verifica se o valor do saque excede o saldo disponível
            excedeu_limite = valor > limite  # Verifica se o valor do saque excede o limite
            excedeu_saques = numero_saques >= LIMITE_SAQUES  # Verifica se excedeu o número máximo de saques

            if excedeu_saldo:
                print("Operação falhou! Você não tem saldo suficiente.")
            
            elif excedeu_limite:
                print("Operação falhou! O valor do saque excede o limite.")
            
            elif excedeu_saques:
                print("Operação falhou! Número máximo de saques excedido.")

            elif valor > 0:
                saldo -= valor  # Decrementa o saldo
                extrato += f"Saque: R$ {valor:.2f}\n"  # Adiciona registro no extrato
                numero_saques += 1  # Incrementa o contador de saques
            
            else:
                print("Operação falhou! O valor informado é inválido.")

        # Opção 3: Extrato
        elif opcao == "3":
            print("\n================ EXTRATO ================")
            print("Não foram realizados movimentações." if not extrato else extrato)
            print(f"\nSaldo: R$ {saldo:.2f}")
            print("==========================================")

        # Opção 0: Sair
        elif opcao == "0":
            break

        # Opção inválida
        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")

main()
