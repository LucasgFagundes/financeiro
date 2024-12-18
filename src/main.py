import flet as ft
from auth import register_user, authenticate_user
import json
import os

current_user = None

COMPRAS_FILE = "data/compras.json"

def main(page: ft.Page):
    page.title = 'CashMind'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.resizable = False
    page.window.maximized = True
    page.padding = ft.padding.all(0)
    page.bgcolor = ft.colors.GREEN_200

    # Alertas de erro e sucesso
    def show_snackbar(message, success=True):
        color = ft.colors.GREEN if success else ft.colors.RED
        page.snack_bar = ft.SnackBar(ft.Text(message, color=ft.colors.WHITE), bgcolor=color)
        page.snack_bar.open = True
        page.update()

    # Login handler
    def handle_login(e):
        global current_user  # Permite modificar a variável global
        username = login_username.value
        password = login_password.value

        if authenticate_user(username, password):
            current_user = username  # Armazena o nome do usuário logado
            show_snackbar("Login bem-sucedido!", success=True)
            page.clean()
            page.add(menu_principal)
        else:
            show_snackbar("Usuário ou senha incorretos.", success=False)

    # Register handler
    def handle_register(e):
        username = register_username.value
        password = register_password.value
        confirm_password = confirm_register_password.value

        if not username or not password:
            show_snackbar("Preencha todos os campos.", success=False)
        elif password != confirm_password:
            show_snackbar("As senhas não coincidem.", success=False)
        elif register_user(username, password):
            show_snackbar("Conta criada com sucesso!", success=True)
            page.clean()
            page.add(login)
        else:
            show_snackbar("Usuário já existe.", success=False)

    

    

    # Inicializa o arquivo de compras, se necessário
    def initialize_compras_file():
        if not os.path.exists(COMPRAS_FILE):
            with open(COMPRAS_FILE, "w") as f:
                json.dump([], f)

    # Carrega os dados de compras
    def load_compras():
        initialize_compras_file()
        with open(COMPRAS_FILE, "r") as f:
            return json.load(f)

    # Salva os dados de compras
    def save_compras(compras):
        with open(COMPRAS_FILE, "w") as f:
            json.dump(compras, f, indent=4)

    # Adicionar compra
    def compra(e):
        # Função chamada após escolher uma categoria
        def handle_categoria(categoria):
            def add_valor(e):
                valor = valor_compra.value
                if not valor or not valor.isdigit():
                    show_snackbar("Digite um valor válido.", success=False)
                    return
                
                compras = load_compras()
                
                # Verifica se o usuário já possui registro no JSON
                usuario_existente = next((u for u in compras if u["nome"] == current_user), None)

                if not usuario_existente:
                    # Cria estrutura inicial para o usuário
                    usuario_existente = {
                        "nome": current_user,
                        "compras": [
                            {"alimentacao": [], "higiene": [], "transporte": [], "roupa": [], "lazer": []}
                        ]
                    }
                    compras.append(usuario_existente)

                # Adiciona o valor à categoria do usuário
                usuario_existente["compras"][0][categoria].append(float(valor))
                save_compras(compras)

                show_snackbar(f"Compra adicionada em {categoria}!", success=True)
                page.clean()
                page.add(menu_principal)

                compras[categoria].append(float(valor))
                save_compras(compras)
                show_snackbar(f"Compra adicionada em {categoria}!", success=True)
                page.clean()
                page.add(menu_principal)

            # Tela para adicionar o valor da compra
            page.clean()
            page.add(
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
                                    ft.TextButton("Cancelar", on_click=lambda _: page.clean() or page.add(menu_principal)),
                                ],
                                spacing=15,
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # Tela para escolher a categoria
        page.clean()
        valor_compra = ft.TextField(hint_text="Digite o valor", prefix_icon=ft.icons.MONEY)
        page.add(
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
                                ft.TextButton("Cancelar", on_click=lambda _: page.clean() or page.add(menu_principal)),
                            ],
                            spacing=15,
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
        )

        



    # Controles do login
    login_username = ft.TextField(hint_text="Digite seu usuário", prefix_icon=ft.icons.PERSON)
    login_password = ft.TextField(hint_text="Digite sua senha", prefix_icon=ft.icons.LOCK, password=True)
    login = ft.Column(
        controls=[
            ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                width=400,
                padding=ft.padding.all(10),
                content=ft.Column(
                    [
                        ft.Text("Login", size=20, weight="bold"),
                        login_username,
                        login_password,
                        ft.ElevatedButton("Login", on_click=handle_login, bgcolor=ft.colors.BLUE),
                        ft.TextButton("Criar nova conta", on_click=lambda _: page.clean() or page.add(register)),
                    ],
                    spacing=15,
                ),
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Controles do registro
    register_username = ft.TextField(hint_text="Nome de usuário", prefix_icon=ft.icons.PERSON)
    register_password = ft.TextField(hint_text="Senha", prefix_icon=ft.icons.LOCK, password=True)
    confirm_register_password = ft.TextField(hint_text="Confirmar senha", prefix_icon=ft.icons.LOCK, password=True)
    register = ft.Column(
        controls=[
            ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                width=400,
                padding=ft.padding.all(10),
                content=ft.Column(
                    [
                        ft.Text("Registrar", size=20, weight="bold"),
                        register_username,
                        register_password,
                        confirm_register_password,
                        ft.ElevatedButton("Registrar", on_click=handle_register, bgcolor=ft.colors.GREEN),
                        ft.TextButton("Já tenho uma conta", on_click=lambda _: page.clean() or page.add(login)),
                    ],
                    spacing=15,
                ),
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Menu principal
    menu_principal = ft.Column(
        controls=[
            ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                width=400,
                padding=ft.padding.all(10),
                content=ft.Column(
                    [
                        ft.Text("Menu Principal", size=20, weight="bold"),
                        ft.ElevatedButton("Adicionar compra", on_click=compra, bgcolor=ft.colors.GREEN),
                        ft.ElevatedButton("Logout", on_click=lambda _: page.clean() or page.add(login), bgcolor=ft.colors.RED),
                    ],
                    spacing=15,
                ),
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    

    # Inicializa com a tela de login
    page.add(login)


if __name__ == '__main__':
    ft.app(target=main)
