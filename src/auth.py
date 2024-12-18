import json
import os

DATA_FILE = "data/usuarios.json"

# Carrega os dados existentes
def load_users():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"usuarios": []}, f)
    with open(DATA_FILE, "r") as f:
        return json.load(f)

# Salva os dados no arquivo
def save_users(users):
    with open(DATA_FILE, "w") as f:
        json.dump(users, f, indent=4)

# Adiciona um novo usuário (registrar)
def register_user(username, password):
    data = load_users()
    for user in data["usuarios"]:
        if user["nome"] == username:
            return False  # Usuário já existe
    data["usuarios"].append({"nome": username, "senha": password})
    save_users(data)
    return True

# Verifica o login
def authenticate_user(username, password):
    data = load_users()
    for user in data["usuarios"]:
        if user["nome"] == username and user["senha"] == password:
            return True
    return False

