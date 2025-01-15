import json
import os

class ComprasManager:
    """Classe para gerenciar compras dos usuários."""


    def __init__(self):
        self.compras_file = "data/compras.json"
        self.categorias_file = "data/categorias.json"
        self._initialize_compras_file()

    def _initialize_compras_file(self):
        if not os.path.exists(self.compras_file):
            with open(self.compras_file, "w") as f:
                json.dump([], f)

    def _load_compras(self):
        with open(self.compras_file, "r") as f:
            return json.load(f)

    def _save_compras(self, compras):
        with open(self.compras_file, "w") as f:
            json.dump(compras, f, indent=4)

    def _load_categorias(self):
        with open(self.categorias_file, "r") as f:
            return json.load(f)["categorias"]

    def add_compra(self, username, categoria, valor):

        categorias = self._load_categorias()
        compras_data = self._load_compras()

        usuario = next((u for u in compras_data if u["nome"] == username), None)
        if not usuario:
            usuario = {
                "nome": username,
                "compras": [{cat: [] for cat in categorias}],
            }
            compras_data.append(usuario)

        usuario["compras"][0][categoria].append(float(valor))
        self._save_compras(compras_data)

    def get_compras(self, username):
        compras_data = self._load_compras()
        usuario = next((u for u in compras_data if u["nome"] == username), None)
        if not usuario:
            return []
        return usuario["compras"][0]