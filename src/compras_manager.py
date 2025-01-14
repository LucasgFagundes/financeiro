import json
import os

class ComprasManager:
    """Classe para gerenciar compras dos usuários."""

    COMPRAS_FILE = "data/compras.json"

    def __init__(self):
        self._initialize_compras_file()

    def _initialize_compras_file(self):
        if not os.path.exists(self.COMPRAS_FILE):
            with open(self.COMPRAS_FILE, "w") as f:
                json.dump([], f)

    def _load_compras(self):
        with open(self.COMPRAS_FILE, "r") as f:
            return json.load(f)

    def _save_compras(self, compras):
        with open(self.COMPRAS_FILE, "w") as f:
            json.dump(compras, f, indent=4)

    def add_compra(self, username, categoria, valor):
        compras_data = self._load_compras()

        usuario = next((u for u in compras_data if u["nome"] == username), None)
        if not usuario:
            usuario = {
                "nome": username,
                "compras": [
                    {"alimentacao": [], "higiene": [], "transporte": [], "roupa": [], "lazer": []}
                ],
            }
            compras_data.append(usuario)

        usuario["compras"][0][categoria].append(float(valor))
        self._save_compras(compras_data)