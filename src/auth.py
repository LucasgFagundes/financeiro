import json
import os

class AuthManager:
    """Classe para gerenciar autenticação e registro de usuários."""

    DATA_FILE = "data/usuarios.json"

    def __init__(self):
        self._initialize_data_file()

    def _initialize_data_file(self):
        if not os.path.exists(self.DATA_FILE):
            with open(self.DATA_FILE, "w") as f:
                json.dump({"usuarios": []}, f)

    def _load_users(self):
        with open(self.DATA_FILE, "r") as f:
            return json.load(f)

    def _save_users(self, users):
        with open(self.DATA_FILE, "w") as f:
            json.dump(users, f, indent=4)

    def register_user(self, username, password):
        users_data = self._load_users()
        for user in users_data["usuarios"]:
            if user["nome"] == username:
                return False  # Usuário já existe
        users_data["usuarios"].append({"nome": username, "senha": password})
        self._save_users(users_data)
        return True

    def authenticate_user(self, username, password):
        users_data = self._load_users()
        for user in users_data["usuarios"]:
            if user["nome"] == username and user["senha"] == password:
                return True
        return False