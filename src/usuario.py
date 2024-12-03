
import json
import os

class Usuario:
    def __init__(self, nome: str, senha: str):
        self.nome = nome
        self.senha = senha

    def criar_usuario(self):
        """Cria um dicionário representando um usuário."""
        usuario = {
            "nome": self.nome,
            "senha": self.senha
        }
        return usuario

    def salvar_usuario_json(usuario, nome_arquivo="../assets/settings/usuario.json"):
        try:
            os.makedirs(os.path.dirname(nome_arquivo), exist_ok=True)

            try:
                with open(nome_arquivo, 'r') as f:
                    dados = json.load(f)
            except (FileNotFoundError, json.JSONDecodeError):
                dados = {} 

            
            if "usuarios" not in dados:
                dados["usuarios"] = []


            if any(u["nome"] == usuario["nome"] for u in dados["usuarios"]):
                print(f"O usuário {usuario['nome']} já existe.")
                return

            dados["usuarios"].append(usuario)

            with open(nome_arquivo, 'w') as f:
                json.dump(dados, f, indent=4)

            print(f"Usuário {usuario['nome']} salvo com sucesso")

        except Exception as e:
            print(f"Erro ao salvar o usuário: {e}")

nome_usuario = input("Digite o nome do usuário:")
senha_usuario = input("Digite a senha do usuário:")

novo_usuario = criar_usuario(nome_usuario, senha_usuario)
salvar_usuario_json(novo_usuario)
