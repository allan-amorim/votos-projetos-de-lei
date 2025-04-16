import flet as ft

# Função para exibir Snackbar
def show_snackbar(page: ft.Page, message: str):
    page.snack_bar = ft.SnackBar(content=ft.Text(message))
    page.snack_bar.open = True
    page.overlay.append(page.snack_bar)
    page.update()

def show_coming_soon(page):
    page.snack_bar = ft.SnackBar(
        content=ft.Text("Funcionalidade em desenvolvimento!"),
        action="OK",
        duration=2000
    )
    page.snack_bar.open = True
    page.overlay.append(page.snack_bar)
    page.update()