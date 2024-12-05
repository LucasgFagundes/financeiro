import json
from datetime import date
import os

class Operacoes:
    def __init__(self, nome):
        self.nome = nome
        self.compras_arquivo = "data/compras.json"

    def _load_compras(self):
        try:
            with open(self.compras_arquivo, "r") as arquivo:
                return json.load(arquivo)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _save_compras(self, compras):
        os.makedirs(os.path.dirname(self.compras_arquivo), exist_ok=True)
        with open(self.compras_arquivo, "w") as arquivo:
            json.dump(compras, arquivo, indent=4)

    def add_compra(self, valor, categoria):
        compras = self._load_compras()
        user_compras = next((u for u in compras if u["nome"] == self.nome), None)

        if not user_compras:
            user_compras = {"nome": self.nome, "compras": []}
            compras.append(user_compras)

        user_compras["compras"].append({
            "valor": valor,
            "categoria": categoria,
            "date": str(date.today())
        })

        self._save_compras(compras)
        print("Compra adicionada com sucesso!")

    def lista_compras(self):
        compras = self._load_compras()
        user_compras = next((u for u in compras if u["nome"] == self.nome), None)

        if not user_compras or not user_compras["compras"]:
            print("Nenhuma compra encontrada.")
        else:
            print(f"--- Compras de {self.nome} ---")
            for compra in user_compras["compras"]:
                print(f"Valor: {compra['valor']}, Categoria: {compra['categoria']}, Data: {compra['date']}")
