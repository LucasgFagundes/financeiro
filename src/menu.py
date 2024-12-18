import flet as ft

def main(page: ft.Page):
    page.title = 'CashMind - Tela Principal'
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.resizable = False
    page.window.maximized = True
    page.padding = ft.padding.all(0)
    page.bgcolor = ft.colors.GREEN_200

    def adicionar_compra(e):
        # Aqui você pode implementar a lógica para abrir uma nova tela ou adicionar compras
        print("Botão 'Adicionar Compra' clicado.")

    def listar_compras(e):
        # Aqui você pode implementar a lógica para abrir uma tela de listagem de compras
        print("Botão 'Listar Compras' clicado.")

    def logout(e):
        # Aqui você pode implementar a lógica para voltar à tela de login
        print("Botão 'Logout' clicado.")
        page.clean()
        page.add(login)

    # Tela principal após login
    tela_principal = ft.Column(
        controls=[
            ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                width=400,
                height=300,
                padding=ft.padding.all(20),
                content=ft.Column(
                    controls=[
                        ft.Text(
                            value="Bem-vindo ao CashMind",
                            size=24,
                            weight="bold",
                            color=ft.colors.BLACK,
                        ),
                        ft.Divider(
                            height=1,
                            color=ft.colors.with_opacity(0.25, ft.colors.GREY),
                            thickness=1,
                        ),
                        ft.ElevatedButton(
                            text="Adicionar Compra",
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE,
                            width=200,
                            height=40,
                            on_click=adicionar_compra,
                        ),
                        ft.ElevatedButton(
                            text="Listar Compras",
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.GREEN,
                            width=200,
                            height=40,
                            on_click=listar_compras,
                        ),
                        ft.ElevatedButton(
                            text="Logout",
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.RED,
                            width=200,
                            height=40,
                            on_click=logout,
                        ),
                    ],
                    spacing=20,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    # Tela de login (simplesmente simulando a troca de telas)
    login = ft.Column(
        controls=[
            ft.Container(
                bgcolor=ft.colors.WHITE,
                border_radius=10,
                width=400,
                height=300,
                padding=ft.padding.all(20),
                content=ft.Column(
                    controls=[
                        ft.Text(
                            value="CashMind Login",
                            size=20,
                            weight="bold",
                            color=ft.colors.BLACK,
                        ),
                        ft.ElevatedButton(
                            text="Login",
                            color=ft.colors.WHITE,
                            bgcolor=ft.colors.BLUE,
                            width=200,
                            height=40,
                            on_click=lambda e: [page.clean(), page.add(tela_principal)],
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
            )
        ],
        alignment=ft.MainAxisAlignment.CENTER,
    )

    page.add(login)

if __name__ == "__main__":
    ft.app(target=main)
