import json
import os

class Usuario:
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha

    def criar_usuario(self):
        return {
            "nome": self.nome,
            "senha": self.senha
        }

    def salvar_usuario_json(self, nome_arquivo="assets/settings/usuario.json"):
        try:
            usuario_dados = self.criar_usuario()
            os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)

            try:
                with open(nome_arquivo, 'r') as f:
                    dados = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                dados = {}

            if "usuarios" not in dados:
                dados["usuarios"] = []

            if any(u["nome"] == usuario_dados["nome"] for u in dados["usuarios"]):
                print(f"O usuário {usuario_dados['nome']} já existe.")
                return

            dados["usuarios"].append(usuario_dados)
            with open(nome_arquivo, 'w') as f:
                json.dump(dados, f, indent=4)

            print(f"Usuário {usuario_dados['nome']} salvo com sucesso")

        except Exception as e:
            print(f"Erro ao salvar o usuário: {e}")


nome_usuario = input("Digite o nome do usuário: ")
senha_usuario = input("Digite a senha do usuário: ")

novo_usuario = Usuario(nome_usuario, senha_usuario)
novo_usuario.salvar_usuario_json()
