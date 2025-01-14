import flet as ft
from auth import AuthManager
from compras_manager import ComprasManager

class CashMindApp:
    def __init__(self):
        self.auth_manager = AuthManager()
        self.compras_manager = ComprasManager()
        self.current_user = None

    def build(self, page: ft.Page):
        page.title = "CashMind"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.window.resizable = False
        page.window.maximized = True
        page.padding = ft.padding.all(0)
        page.bgcolor = ft.colors.GREEN_200

        def show_snackbar(message, success=True):
            color = ft.colors.GREEN if success else ft.colors.RED
            page.snack_bar = ft.SnackBar(ft.Text(message, color=ft.colors.WHITE), bgcolor=color)
            page.snack_bar.open = True
            page.update()

        def handle_login(e):
            username = login_username.value
            password = login_password.value

            if self.auth_manager.authenticate_user(username, password):
                self.current_user = username
                show_snackbar("Login bem-sucedido!", success=True)
                page.clean()
                page.add(menu_principal)
            else:
                show_snackbar("Usuário ou senha incorretos.", success=False)

        def handle_register(e):
            username = register_username.value
            password = register_password.value
            confirm_password = confirm_register_password.value

            if not username or not password:
                show_snackbar("Preencha todos os campos.", success=False)
            elif password != confirm_password:
                show_snackbar("As senhas não coincidem.", success=False)
            elif self.auth_manager.register_user(username, password):
                show_snackbar("Conta criada com sucesso!", success=True)
                page.clean()
                page.add(login)
            else:
                show_snackbar("Usuário já existe.", success=False)

        def compra(e):
            def handle_categoria(categoria):
                def add_valor(e):
                    valor = valor_compra.value
                    if not valor or not valor.isdigit():
                        show_snackbar("Digite um valor válido.", success=False)
                        return

                    self.compras_manager.add_compra(self.current_user, categoria, valor)
                    show_snackbar(f"Compra adicionada em {categoria}!", success=True)
                    page.clean()
                    page.add(menu_principal)

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
                                        ft.TextButton(
                                            "Cancelar",
                                            on_click=lambda _: page.clean() or page.add(menu_principal),
                                        ),
                                    ],
                                    spacing=15,
                                ),
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    )
                )

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
                                    ft.TextButton(
                                        "Cancelar",
                                        on_click=lambda _: page.clean() or page.add(menu_principal),
                                    ),
                                ],
                                spacing=15,
                            ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        login_username = ft.TextField(hint_text="Digite seu usuário", prefix_icon=ft.icons.PERSON)
        login_password = ft.TextField(hint_text="Digite sua senha", prefix_icon=ft.icons.LOCK, password=True)
        login = ft.Column(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_600,
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

        register_username = ft.TextField(hint_text="Nome de usuário", prefix_icon=ft.icons.PERSON)
        register_password = ft.TextField(hint_text="Senha", prefix_icon=ft.icons.LOCK, password=True)
        confirm_register_password = ft.TextField(hint_text="Confirmar senha", prefix_icon=ft.icons.LOCK, password=True)
        register = ft.Column(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_500,
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

        def ver_compras(e):
            compras = self.compras_manager.get_compras(self.current_user)
            total_compras = {categoria: sum(map(int, valores)) for categoria, valores in compras.items()}
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
                            ft.Text("Compras", size=20, weight="bold"),
                            ft.Text(f"Alimentação: {total_compras['alimentacao']}", color=ft.colors.BLACK),
                            ft.Text(f"Higiene: {total_compras['higiene']}", color=ft.colors.BLACK),
                            ft.Text(f"Transporte: {total_compras['transporte']}", color=ft.colors.BLACK),
                            ft.Text(f"Roupa: {total_compras['roupa']}", color=ft.colors.BLACK),
                            ft.Text(f"Lazer: {total_compras['lazer']}", color=ft.colors.BLACK),
                            ft.TextButton(f"Total: {sum(total_compras.values())}", on_click=lambda _: None),
                            ft.TextButton(
                            "Voltar",
                            on_click=lambda _: page.clean() or page.add(menu_principal),
                            ),
                        ],
                        spacing=15,
                        ),
                    )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        menu_principal = ft.Column(
            controls=[
                ft.Container(
                    bgcolor=ft.colors.BLUE_GREY_500,
                    border_radius=10,
                    width=400,
                    padding=ft.padding.all(10),
                    content=ft.Column(
                        [
                            ft.Text("Menu Principal", size=20, weight="bold"),
                            ft.ElevatedButton("Ver compras", on_click=ver_compras, bgcolor=ft.colors.BLUE),
                            ft.ElevatedButton("Adicionar compra", on_click=compra, bgcolor=ft.colors.GREEN),
                            ft.ElevatedButton("Logout", on_click=lambda _: page.clean() or page.add(login), bgcolor=ft.colors.RED),
                        ],
                        spacing=15,
                    ),
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        

        page.add(login)




