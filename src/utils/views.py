import flet as ft
from utils import strings
from utils.formats import formatar_valor
from utils.icons import icon_add_modalidade, icon_logout
from components.snackbar import show_snackbar

# Função para mudar de tela
def mudar_tela(page: ft.Page, route: str):
    page.go(route)

def voltar_menu(page: ft.Page):
    page.data = {strings.nm_usuario: page.data.get(strings.nm_usuario)}
    mudar_tela(page, strings.menu)

def voltar_login(page: ft.Page):
    page.data = None
    mudar_tela(page, strings.login)

def fechar_dialog(page: ft.Page, dialog: ft.AlertDialog):
    dialog.open = False
    page.update()

def limpar_field(e):
    e.control.value = ""
    e.control.update()

def on_blur_dinheiro(e, gz=False):
    """Formata o campo apenas ao perder o foco."""
    valor_atual = e.control.value
    valor_atual = formatar_valor(valor_atual, 'number') if valor_atual else 0
    e.control.value = formatar_valor(valor_atual, 'string')
    if gz and not valor_atual:
        e.control.error_text = "É necessário adicionar um valor total maior que zero"
    elif gz and valor_atual:
        e.control.error_text = ""
    e.control.update()

# Função para criar um RadioButton personalizado com ícone
def create_radio_with_icon(value, icon_name, label_text):
    return ft.Row(
        controls=[
            ft.Icon(name=icon_name, color=ft.colors.BLACK),
            ft.Radio(value=value),
            ft.Text(label_text),
        ],
        spacing=10,  # Espaço entre os elementos
    )

# Função para criar o MenuBar
def criar_menubar(page):
    return ft.PopupMenuButton(
        icon=ft.icons.SETTINGS,
        tooltip="Configurações",
        items=[
            ft.PopupMenuItem(
                text="Editar Modalidades de Pagamento",
                icon=icon_add_modalidade,
                on_click=lambda e: voltar_login(page)  # Chama a função para adicionar modalidade
            ),
            ft.PopupMenuItem(
                text="Logout",
                icon=icon_logout,
                on_click=lambda e: voltar_login(page)  # Chama a função para adicionar modalidade
            )
        ]
    )

def appbar(page: ft.Page, titulo: str):
    return ft.AppBar(
        title=ft.Text(titulo),
        actions=[criar_menubar(page)],  # Adiciona o MenuBar no AppBar
    )