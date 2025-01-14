import flet as ft
from cashmind_app import CashMindApp

def main(page: ft.Page):
    app = CashMindApp()
    app.build(page)

if __name__ == "__main__":
    ft.app(target=main)
