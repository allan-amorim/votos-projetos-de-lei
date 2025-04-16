import flet as ft
from utils.views import mudar_tela, appbar
from utils import strings
from components.snackbar import show_coming_soon

# Tela de Menu
def tela_menu(page: ft.Page):
        
        title = ft.Text("Câmara dos Deputados - Dados Abertos", 
                       size=28, weight="bold", text_align=ft.TextAlign.CENTER)
        
        subtitle = ft.Text("Selecione uma opção:", 
                           size=16, color=ft.colors.GREY_600)
        
        btn_projetos = ft.ElevatedButton(
            "Projetos de Lei",
            icon=ft.icons.ARTICLE,
            on_click=lambda e: mudar_tela(page, "/projetos"),
            width=300,
            height=60,
            style=ft.ButtonStyle(
                padding=20,
                elevation=8
            )
        )
        
        btn_deputados = ft.ElevatedButton(
            "Deputados",
            icon=ft.icons.PEOPLE,
            on_click=lambda e: show_coming_soon(page),
            width=300,
            height=60,
            style=ft.ButtonStyle(
                padding=20,
                elevation=8
            )
        )

        btn_partidos = ft.ElevatedButton(
            "Partidos",
            icon=ft.icons.FLAG,
            on_click=lambda e: show_coming_soon(page),
            width=300,
            height=60,
            style=ft.ButtonStyle(
                padding=20,
                elevation=8
            )
        )
        
        btn_sair = ft.ElevatedButton(
            "Sair",
            icon=ft.icons.EXIT_TO_APP,
            on_click=lambda e: page.window_close(),
            width=300,
            height=60,
            style=ft.ButtonStyle(
                padding=20,
                elevation=8
            )
        )

        return ft.View(
            strings.menu,
            [
            appbar(page, "Menu"),
                ft.Column([
                    title,
                    subtitle,
                    ft.Container(height=40),
                    ft.Column([
                        btn_projetos,
                        ft.Container(height=20),
                        btn_deputados,
                        ft.Container(height=20),
                        btn_partidos,
                        ft.Container(height=20),
                        btn_sair
                    ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ],
        )