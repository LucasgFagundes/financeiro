import flet as ft
from modules.auth import autenticar_usuario, registrar_usuario
from modules.data_manager import adicionar_compra, carregar_compras

def main(page: ft.Page):
    page.title = 'CashMind'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.resizable = False
    page.window.maximized = True
    page.padding = ft.padding.all(0)
    page.bgcolor = ft.colors.GREEN_200

    # Funções de navegação
    def logar(e: ft.ControlEvent):
        if autenticar_usuario(usuario.value, senha.value):
            page.clean()
            page.add(menu_principal)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Usuário ou senha inválidos!"))
            page.snack_bar.open = True
            page.update()

    def registrar(e: ft.ControlEvent):
        if registrar_usuario(nome.value, senha1.value, senha2.value):
            page.clean()
            page.add(login)
        else:
            page.snack_bar = ft.SnackBar(ft.Text("Erro ao registrar. Verifique os dados!"))
            page.snack_bar.open = True
            page.update()

    # Login
    usuario = ft.TextField(label="Usuário")
    senha = ft.TextField(label="Senha", password=True, can_reveal_password=True)

    login = ft.Column(
        controls=[
            ft.Text("Login", size=20, weight="bold"),
            usuario,
            senha,
            ft.ElevatedButton(text="Entrar", on_click=logar),
            ft.TextButton("Registrar nova conta", on_click=lambda e: page.clean() or page.add(register)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Registro
    nome = ft.TextField(label="Nome")
    senha1 = ft.TextField(label="Senha", password=True, can_reveal_password=True)
    senha2 = ft.TextField(label="Repita a senha", password=True, can_reveal_password=True)

    register = ft.Column(
        controls=[
            ft.Text("Registro", size=20, weight="bold"),
            nome,
            senha1,
            senha2,
            ft.ElevatedButton(text="Registrar", on_click=registrar),
            ft.TextButton("Já tenho uma conta", on_click=lambda e: page.clean() or page.add(login)),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Menu Principal
    menu_principal = ft.Column(
        controls=[
            ft.Text("Bem-vindo ao CashMind!", size=20, weight="bold"),
            ft.ElevatedButton(text="Adicionar Compra", on_click=lambda e: page.clean() or page.add(adicionar)),
            ft.ElevatedButton(text="Sair", on_click=lambda e: page.clean() or page.add(login)),
        ]
    )

    # Adicionar compra
    categoria = ft.Dropdown(
        options=[
            ft.dropdown.Option("alimentacao"),
            ft.dropdown.Option("higiene"),
            ft.dropdown.Option("transporte"),
            ft.dropdown.Option("roupa"),
            ft.dropdown.Option("lazer"),
        ],
        label="Categoria",
    )
    valor = ft.TextField(label="Valor")

    adicionar = ft.Column(
        controls=[
            ft.Text("Adicionar Compra", size=20, weight="bold"),
            categoria,
            valor,
            ft.ElevatedButton(
                text="Salvar",
                on_click=lambda e: adicionar_compra(usuario.value, categoria.value, float(valor.value)),
            ),
            ft.TextButton("Voltar", on_click=lambda e: page.clean() or page.add(menu_principal)),
        ]
    )

    page.add(login)

if __name__ == "__main__":
    ft.app(target=main)
