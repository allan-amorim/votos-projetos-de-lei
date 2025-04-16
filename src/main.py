import flet as ft
from views import tela_menu #, tela_despesa, tela_visao_casal, tela_visao_individual, tela_resumo_individual
from utils import strings

def main(page: ft.Page):
    page.title = strings.titulo
    page.theme_mode = "light"  # ou "dark"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # Configuração das rotas
    def route_change(route):
        page.views.clear()
        if page.route == strings.menu:
            page.views.append(tela_menu(page))
        elif page.route == strings.projetos:
            page.views.append(tela_despesa(page))
        # elif page.route == strings.visao_individual:
        #     page.views.append(tela_visao_individual(page))
        # elif page.route == strings.resumo_individual:
        #     page.views.append(tela_resumo_individual(page))
        # elif page.route == strings.visao_casal:
        #     page.views.append(tela_visao_casal(page)) 
        page.update()

    # Configuração do gerenciador de rotas
    page.on_route_change = route_change
    page.go(strings.menu)

# Inicia o aplicativo
ft.app(target=main)