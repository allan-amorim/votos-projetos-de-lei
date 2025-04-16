import flet as ft
from utils.views import mudar_tela
from components.snackbar import show_snackbar
from utils import strings

def login(page, user):
    page.data = {strings.nm_usuario: user}
    show_snackbar(page, f"Bem-vindo(a), {user}!")
    mudar_tela(page, route=strings.menu)

# Tela de Login
def tela_login(page: ft.Page):
    return ft.View(
        strings.login,
        [
            ft.AppBar(title=ft.Text("Login")),
            ft.Column(
                [
                    ft.Text("Escolha o usuário:", size=24, weight="bold", color="blue"),
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ft.GestureDetector(
                                content=ft.Image(
                                    src="assets/images/pic_allan.jpg",
                                    width=100,
                                    height=100,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                on_tap=lambda e: login(page, user="Allan")
                            ),
                            ft.ElevatedButton(
                                text="Login como Allan",
                                on_click=lambda e: login(page, user="Allan"),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Row(
                        [
                            ft.GestureDetector(
                                content=ft.Image(
                                    src="assets/images/pic_melanie.jpg",
                                    width=100,
                                    height=100,
                                    fit=ft.ImageFit.CONTAIN,
                                ),
                                on_tap=lambda e: login(page, user="Melanie")
                            ),
                            ft.ElevatedButton(
                                text="Login como Melanie",
                                on_click=lambda e: login(page, user="Melanie"),
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                    ),
                    ft.Container(expand=True),
                    ft.Text(
                        strings.copyright,
                        size=12,
                        color="grey",
                    ),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
        ],
    )
