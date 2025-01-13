import flet as ft
from auth import Auth
import json
import os

COMPRAS_FILE = "../data/compras.json"

class CompraManager:
    
    def __init__(self, current_user, page: ft.Page, menu_principal:ft.Column):
        self.initialize_compras_file()
        self.current_user = current_user
        self.page = page
        self.menu_principal = menu_principal
    # Inicializa o arquivo de compras, se necessário
    def initialize_compras_file(self):
        if not os.path.exists(COMPRAS_FILE):
            with open(COMPRAS_FILE, "w") as f:
                json.dump([], f)

    # Carrega os dados de compras
    def load_compras(self):
        self.initialize_compras_file()
        with open(COMPRAS_FILE, "r") as f:
            return json.load(f)

    # Salva os dados de compras
    def save_compras(self, compras):
        with open(COMPRAS_FILE, "w") as f:
            json.dump(compras, f, indent=4)

    # Adicionar compra
    def compra(self, e):
        # Função chamada após escolher uma categoria
        def handle_categoria(categoria):
            def add_valor(e):
                valor = valor_compra.value
                if not valor or not valor.isdigit():
                    self.show_snackbar("Digite um valor válido.", success=False)
                    return
                
                compras = self.load_compras()
                
                # Verifica se o usuário já possui registro no JSON
                usuario_existente = next((u for u in compras if u["nome"] == self.current_user), None)

                if not usuario_existente:
                    # Cria estrutura inicial para o usuário
                    usuario_existente = {
                        "nome": self.current_user,
                        "compras": [
                            {"alimentacao": [], "higiene": [], "transporte": [], "roupa": [], "lazer": []}
                        ]
                    }
                    compras.append(usuario_existente)

                # Adiciona o valor à categoria do usuário
                usuario_existente["compras"][0][categoria].append(float(valor))
                self.save_compras(compras)

                self.show_snackbar(f"Compra adicionada em {categoria}!", success=True)
                self.page.clean()
                self.page.add(self.menu_principal)

                compras[categoria].append(float(valor))
                self.save_compras(compras)
                self.show_snackbar(f"Compra adicionada em {categoria}!", success=True)
                self.page.clean()
                self.page.add(self.menu_principal)

            # Tela para adicionar o valor da compra
            self.page.clean()
            self.page.add(
                ft.Column(
                    controls=[
                        ft.Container(
                            bgcolor=ft.colors.WHITE,
                            border_radius=10,
                            width=400,
                            padding=ft.padding.all(10),
                            content=ft.Column(
                                [
                                    ft.Text(f"Adicionar valor para {categoria}", size=20, weight="bold"),
                                    valor_compra,
                                    ft.ElevatedButton("Salvar", on_click=add_valor, bgcolor=ft.colors.GREEN),
                                    ft.TextButton("Cancelar", on_click=lambda _: self.page.clean() or self.page.add(self.menu_principal)),
                                ],
                                spacing=15,
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # Tela para escolher a categoria
        self.page.clean()
        valor_compra = ft.TextField(hint_text="Digite o valor", prefix_icon=ft.icons.MONEY)
        self.page.add(
            ft.Column(
                controls=[
                    ft.Container(
                        bgcolor=ft.colors.WHITE,
                        border_radius=10,
                        width=400,
                        padding=ft.padding.all(10),
                        content=ft.Column(
                            [
                                ft.Text("Escolha a categoria", size=20, weight="bold"),
                                ft.ElevatedButton("Alimentação", on_click=lambda _: handle_categoria("alimentacao"), bgcolor=ft.colors.BLUE),
                                ft.ElevatedButton("Higiene", on_click=lambda _: handle_categoria("higiene"), bgcolor=ft.colors.BLUE),
                                ft.ElevatedButton("Transporte", on_click=lambda _: handle_categoria("transporte"), bgcolor=ft.colors.BLUE),
                                ft.ElevatedButton("Roupa", on_click=lambda _: handle_categoria("roupa"), bgcolor=ft.colors.BLUE),
                                ft.ElevatedButton("Lazer", on_click=lambda _: handle_categoria("lazer"), bgcolor=ft.colors.BLUE),
                                ft.TextButton("Cancelar", on_click=lambda _: self.page.clean() or self.page.add(self.menu_principal)),
                            ],
                            spacing=15,
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )
