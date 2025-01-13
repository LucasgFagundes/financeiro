import json
import os

DATA_FILE = "../data/usuarios.json"

# Carrega os dados existentes

class Auth:

    def __init__(self, username, password):
        self.username = username
        self.password = password
    """Classe responsável pela autenticação e registro de usuários."""
    def load_users(self):
        if not os.path.exists(DATA_FILE):
            with open(DATA_FILE, "w") as f:
                json.dump({"usuarios": []}, f)
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    
    # Salva os dados no arquivo
    def save_users(self, users):
        with open(DATA_FILE, "w") as f:
            json.dump(users, f, indent=4)

    # Adiciona um novo usuário (registrar)
    def register_user(self):
        data = self.load_users()
        for user in data["usuarios"]:
            if user["nome"] == self.username:
                return False  # Usuário já existe
        data["usuarios"].append({"nome": self.username, "senha": self.password})
        self.save_users(data)
        return True

    # Verifica o login
    def authenticate_user(self):
        data = self.load_users()
        for user in data["usuarios"]:
            if user["nome"] == self.username and user["senha"] == self.password:
                return True
        return False
