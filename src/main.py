from usuarioo import Usuario
from operacoes import Operacoes
import json

def main():
    print("--- Bem-vindo ao Sistema de Controle Financeiro ---")
    
    while True:
        print("\nMenu:")
        print("1. Criar usuário")
        print("2. Fazer login")
        print("3. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            nome_usuario = input("Digite o nome do usuário: ")
            senha_usuario = input("Digite a senha do usuário: ")
            novo_usuario = Usuario(nome_usuario, senha_usuario)
            Usuario.salvar_usuario_json(novo_usuario.criar_usuario())

        elif opcao == "2":
            nome_usuario = input("Digite o nome do usuário: ")
            senha_usuario = input("Digite a senha do usuário: ")

            try:
                with open("data/usuarios.json", "r") as f:
                    dados = json.load(f)

                usuario_valido = any(
                    u["nome"] == nome_usuario and u["senha"] == senha_usuario
                    for u in dados.get("usuarios", [])
                )

                if usuario_valido:
                    print(f"Bem-vindo, {nome_usuario}!")
                    operacoes = Operacoes(nome_usuario)

                    while True:
                        print("\n--- Menu de Compras ---")
                        print("1. Adicionar compra")
                        print("2. Listar compras")
                        print("3. Logout")
                        escolha = input("Escolha uma opção: ")

                        if escolha == "1":
                            valor = float(input("Digite o valor da compra: "))
                            categoria = input("Digite a categoria da compra: ")
                            operacoes.add_compra(valor, categoria)
                        elif escolha == "2":
                            operacoes.lista_compras()
                        elif escolha == "3":
                            break
                        else:
                            print("Opção inválida!")
                else:
                    print("Usuário ou senha incorretos!")
            except FileNotFoundError:
                print("Nenhum usuário cadastrado ainda.")
        elif opcao == "3":
            print("Saindo... Até mais!")
            break
        else:
            print("Opção inválida!")

if __name__ == "__main__":
    main()
