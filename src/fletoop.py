import flet as ft
import json
import os


#Exemplo de OOP gerado pelo chat, não funciona, só pra se basear

# Constants
COMPRAS_FILE = "../data/compras.json"
USERS_FILE = "../data/usuarios.json"


class Auth:
    """Classe responsável pela autenticação e registro de usuários."""
    @staticmethod
    def authenticate_user(username, password):
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            return False

        for user in users:
            if user["username"] == username and user["password"] == password:
                return True
        return False

    @staticmethod
    def register_user(username, password):
        try:
            with open(USERS_FILE, "r") as f:
                users = json.load(f)
        except FileNotFoundError:
            users = []

        if any(user["username"] == username for user in users):
            return False

        users.append({"username": username, "password": password})
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=4)
        return True


class CompraManager:
    """Classe para gerenciar compras do usuário."""
    def __init__(self):
        self._initialize_compras_file()

    def _initialize_compras_file(self):
        if not os.path.exists(COMPRAS_FILE):
            with open(COMPRAS_FILE, "w") as f:
                json.dump([], f)

    def load_compras(self):
        with open(COMPRAS_FILE, "r") as f:
            return json.load(f)

    def save_compras(self, compras):
        with open(COMPRAS_FILE, "w") as f:
            json.dump(compras, f, indent=4)

    def add_compra(self, user, categoria, valor):
        compras = self.load_compras()

        # Verifica se o usuário já possui registro no JSON
        usuario_existente = next((u for u in compras if u["nome"] == user), None)
        if not usuario_existente:
            usuario_existente = {
                "nome": user,
                "compras": {
                    "alimentacao": [], "higiene": [], "transporte": [], "roupa": [], "lazer": []
                }
            }
            compras.append(usuario_existente)

        # Adiciona a compra na categoria
        usuario_existente["compras"][categoria].append(float(valor))
        self.save_compras(compras)


class CashMindApp:
    """Classe principal que gerencia a interface do aplicativo."""
    def __init__(self):
        self.current_user = None
        self.compra_manager = CompraManager()

    def main(self, page: ft.Page):
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

        # Handlers
        def handle_login(e):
            username = login_username.value
            password = login_password.value

            if Auth.authenticate_user(username, password):
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
            elif Auth.register_user(username, password):
                show_snackbar("Conta criada com sucesso!", success=True)
                page.clean()
                page.add(login)
            else:
                show_snackbar("Usuário já existe.", success=False)

        def add_compra(categoria):
            def save_compra(e):
                valor = valor_compra.value
                if not valor or not valor.isdigit():
                    show_snackbar("Digite um valor válido.", success=False)
                    return

                self.compra_manager.add_compra(self.current_user, categoria, valor)
                show_snackbar(f"Compra adicionada em {categoria}!", success=True)
                page.clean()
                page.add(menu_principal)

            page.clean()
            valor_compra = ft.TextField(hint_text="Digite o valor", prefix_icon=ft.icons.MONEY)
            page.add(
                ft.Column(
                    controls=[
                        ft.Text(f"Adicionar valor para {categoria}", size=20, weight="bold"),
                        valor_compra,
                        ft.ElevatedButton("Salvar", on_click=save_compra, bgcolor=ft.colors.GREEN),
                        ft.TextButton("Cancelar", on_click=lambda _: page.clean() or page.add(menu_principal)),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

        # Layouts
        login_username = ft.TextField(hint_text="Digite seu usuário", prefix_icon=ft.icons.PERSON)
        login_password = ft.TextField(hint_text="Digite sua senha", prefix_icon=ft.icons.LOCK, password=True)
        login = ft.Column(
            controls=[
                ft.Text("Login", size=20, weight="bold"),
                login_username,
                login_password,
                ft.ElevatedButton("Login", on_click=handle_login, bgcolor=ft.colors.BLUE),
                ft.TextButton("Criar nova conta", on_click=lambda _: page.clean() or page.add(register)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        register_username = ft.TextField(hint_text="Nome de usuário", prefix_icon=ft.icons.PERSON)
        register_password = ft.TextField(hint_text="Senha", prefix_icon=ft.icons.LOCK, password=True)
        confirm_register_password = ft.TextField(hint_text="Confirmar senha", prefix_icon=ft.icons.LOCK, password=True)
        register = ft.Column(
            controls=[
                ft.Text("Registrar", size=20, weight="bold"),
                register_username,
                register_password,
                confirm_register_password,
                ft.ElevatedButton("Registrar", on_click=handle_register, bgcolor=ft.colors.GREEN),
                ft.TextButton("Já tenho uma conta", on_click=lambda _: page.clean() or page.add(login)),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        menu_principal = ft.Column(
            controls=[
                ft.Text("Menu Principal", size=20, weight="bold"),
                ft.ElevatedButton("Adicionar compra", on_click=lambda _: add_compra("alimentacao"), bgcolor=ft.colors.GREEN),
                ft.ElevatedButton("Logout", on_click=lambda _: page.clean() or page.add(login), bgcolor=ft.colors.RED),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # Inicializa com a tela de login
        page.add(login)


if __name__ == "__main__":
    app = CashMindApp()
    ft.app(target=app.main)
