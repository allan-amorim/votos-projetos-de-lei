import flet as ft
import requests
import time
import pandas as pd
from datetime import datetime

class MainMenu:
    def __init__(self, page: ft.Page):
        self.page = page
    
    def build(self):
        title = ft.Text("Câmara dos Deputados - Dados Abertos", 
                       size=28, weight="bold", text_align=ft.TextAlign.CENTER)
        
        subtitle = ft.Text("Selecione uma opção:", 
                           size=16, color=ft.colors.GREY_600)
        
        # Botões do menu
        btn_projetos = ft.ElevatedButton(
            "Projetos de Lei",
            icon=ft.icons.ARTICLE,
            on_click=lambda e: self.page.go("/projetos"),
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
            on_click=lambda e: self.show_coming_soon(),
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
            on_click=lambda e: self.show_coming_soon(),
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
            on_click=lambda e: self.page.window_close(),
            width=300,
            height=60,
            style=ft.ButtonStyle(
                padding=20,
                elevation=8
            )
        )
        
        # Layout do menu
        return ft.Column([
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
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    def show_coming_soon(self):
        self.page.snack_bar = ft.SnackBar(
            content=ft.Text("Funcionalidade em desenvolvimento!"),
            action="OK",
            duration=2000
        )
        self.page.snack_bar.open = True
        self.page.overlay.append(self.page.snack_bar)
        self.page.update()

class ProjetosDeLeiApp:
    def __init__(self, page: ft.Page):
        self.page = page
        self.setup_page()
        self.create_ui()
        self.base_url = "https://dadosabertos.camara.leg.br/api/v2"
        self.df_proposicoes = pd.DataFrame()
        self.df_votacoes = pd.DataFrame()
        self.df_votos = pd.DataFrame()
        self.df_completo = pd.DataFrame()

    def setup_page(self):
        self.page.title = "Câmara dos Deputados - Projetos de Lei"
        self.page.theme_mode = ft.ThemeMode.LIGHT
        self.page.padding = 20
        self.page.window_width = 1000
        self.page.window_height = 700
        self.page.scroll = ft.ScrollMode.AUTO

    def create_ui(self):
        # Botão de voltar ao menu
        self.btn_voltar = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            on_click=lambda e: self.page.go("/"),
            tooltip="Voltar ao menu"
        )
        
        # Elementos da UI
        self.title = ft.Row([
            self.btn_voltar,
            ft.Text("Consulta de Projetos de Lei", size=24, weight="bold")
        ], spacing=10)
        
        self.progress_bar = ft.ProgressBar(width=400, visible=False)
        self.status_text = ft.Text("", color=ft.colors.GREY_600)
        
        # Controles de entrada
        self.ano_input = ft.TextField(
            label="Ano",
            value='2023',
            width=65,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        self.tipos_input = ft.Dropdown(
            label="Tipo",
            options=[
                ft.dropdown.Option("PEC"),
                ft.dropdown.Option("PL"),
                ft.dropdown.Option("PLN"),
                ft.dropdown.Option("PDL"),
                ft.dropdown.Option("MPV"),
            ],
            value="PEC",
            width=90
        )
        
        self.limite_input = ft.TextField(
            label="Limite de itens",
            value="1",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER
        )
        
        # Botões
        self.buscar_btn = ft.ElevatedButton(
            "Buscar Dados",
            icon=ft.icons.SEARCH,
            on_click=self.buscar_dados
        )
        
        self.exportar_btn = ft.ElevatedButton(
            "Exportar para CSV",
            icon=ft.icons.DOWNLOAD,
            on_click=self.exportar_csv,
            disabled=True
        )
        
        # Tabelas de resultados
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Proposições"),
                ft.Tab(text="Votações"),
                ft.Tab(text="Votos"),
            ],
            expand=1,
            on_change=self.tab_changed
        )
        
        self.tabela_container = ft.Column([], scroll=ft.ScrollMode.AUTO)
        
        # Layout principal
        self.page.add(
            ft.Column([
                self.title,
                ft.Row([
                    self.ano_input,
                    self.tipos_input,
                    self.limite_input,
                ], spacing=20, scroll=ft.ScrollMode.AUTO),
                ft.Row([
                    self.buscar_btn,
                    self.exportar_btn,
                ], spacing=20),
                self.progress_bar,
                self.status_text,
                self.tabs,
                ft.Container(
                    ft.Row(
                        [self.tabela_container], 
                        scroll=ft.ScrollMode.AUTO
                    ),
                    border=ft.border.all(1, ft.colors.GREY_400),
                    border_radius=5,
                    padding=10,
                    expand=True,
                )
            ], spacing=20, expand=True)
        )

    def buscar_dados(self, e):
        try:
            # Ativar indicador de progresso
            self.progress_bar.visible = True
            self.status_text.value = "Buscando dados da API..."
            self.status_text.color = ft.colors.BLUE
            self.buscar_btn.disabled = True
            self.page.update()
            
            # Obter parâmetros da interface
            ano = int(self.ano_input.value)
            tipos = [tipo for tipo in self.tipos_input.value] if isinstance(self.tipos_input.value, list) else [self.tipos_input.value]
            limite = int(self.limite_input.value)
            
            # Buscar dados
            self._buscar_proposicoes(ano, tipos, limite)
            self._buscar_votacoes()
            self._buscar_votos()
            
            # Atualizar interface com resultados
            self._atualizar_tabelas()
            
            self.status_text.value = f"Dados obtidos com sucesso! {len(self.df_proposicoes)} proposições encontradas."
            self.status_text.color = ft.colors.GREEN
            self.exportar_btn.disabled = False
            
        except Exception as ex:
            print(f'Chaves: {self.df_proposicoes}')
            self.status_text.value = f"Erro: {str(ex)}"
            self.status_text.color = ft.colors.RED
        finally:
            self.progress_bar.visible = False
            self.buscar_btn.disabled = False
            self.page.update()

    def tab_changed(self, e):
        self._atualizar_tabelas()

    def _buscar_proposicoes(self, ano, tipos, limite):
        url = f"{self.base_url}/proposicoes"
        params = {
            "ano": ano,
            "siglaTipo": tipos,
            "itens": limite
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        self.df_proposicoes = pd.DataFrame(r.json()['dados'])
        self.df_proposicoes.rename(columns={i: 'proposicao_' + i for i in self.df_proposicoes.columns}, inplace=True)

    def _buscar_votacoes(self):
        self.df_votacoes = pd.DataFrame()
        for i in self.df_proposicoes['proposicao_id']:
            proposicao_id = int(i)
            url = f"{self.base_url}/proposicoes/{proposicao_id}/votacoes"
            r = requests.get(url)
            r.raise_for_status()
            dados = r.json()['dados']
            print(url)
            df_votacoes_temp = pd.DataFrame(dados)
            if not df_votacoes_temp.empty:
                df_votacoes_temp.rename(columns={i: 'votacao_' + i for i in df_votacoes_temp.columns}, inplace=True)
                df_votacoes_temp['proposicao_id'] = proposicao_id
                self.df_votacoes = pd.concat([self.df_votacoes, df_votacoes_temp])
            
            # Atualizar status
            self.status_text.value = f"Buscando votações... {len(self.df_votacoes)} encontradas"
            self.page.update()
            time.sleep(0.3)

    def _buscar_votos(self):
        self.df_votos = pd.DataFrame()
        for i in self.df_votacoes['votacao_id']:
            votacao_id = str(i)
            url = f"{self.base_url}/votacoes/{votacao_id}/votos"
            r = requests.get(url)
            r.raise_for_status()
            df_votos_temp = pd.DataFrame(r.json()['dados'])
            if not df_votos_temp.empty:
                df_votos_temp.rename(columns={i: 'voto_' + i for i in df_votos_temp.columns}, inplace=True)
                df_votos_temp['votacao_id'] = votacao_id
                df_deputados_temp = pd.DataFrame(df_votos_temp['voto_deputado_'].to_list())
                df_votos_temp[['deputado_' + i for i in df_deputados_temp.columns]] = df_deputados_temp
                df_votos_temp.drop(columns=['voto_deputado_'], inplace=True)
                self.df_votos = pd.concat([self.df_votos, df_votos_temp])
            
            # Atualizar status
            self.status_text.value = f"Buscando votos... {len(self.df_votos)} encontrados"
            self.page.update()
            time.sleep(0.5)

    def _atualizar_tabelas(self):
        # Criar DataTable para cada aba
        self.tabela_container.controls = []
        
        if self.tabs.selected_index == 0 and not self.df_proposicoes.empty:
            self.tabela_container.controls.append(self._criar_data_table(self.df_proposicoes))
        elif self.tabs.selected_index == 1 and not self.df_votacoes.empty:
            self.tabela_container.controls.append(self._criar_data_table(self.df_votacoes))
        elif self.tabs.selected_index == 2 and not self.df_votos.empty:
            self.tabela_container.controls.append(self._criar_data_table(self.df_votos))
        else:
            self.tabela_container.controls.append(ft.Text("Nenhum dado disponível para esta visualização."))
        
        self.page.update()

    def _criar_data_table(self, df):
        # Limitar a 100 colunas para performance
        df_display = df.iloc[:, :100].copy()
        
        # Converter todos os valores para string
        df_display = df_display.astype(str)
        
        # Criar colunas da tabela
        columns = [ft.DataColumn(ft.Text(col)) for col in df_display.columns]
        
        # Criar linhas da tabela (limitado a 100 linhas para performance)
        rows = []
        for _, row in df_display.head(100).iterrows():
            cells = [ft.DataCell(ft.Text(str(item))) for item in row]  # Limitar texto para caber na célula
            rows.append(ft.DataRow(cells))
        
        return ft.DataTable(
            columns=columns,
            rows=rows,
            heading_row_color=ft.colors.BLUE_GREY_100,
            heading_row_height=40,
            data_row_min_height=30,
            data_row_max_height=60,
            column_spacing=20,
            horizontal_margin=10,
            divider_thickness=1,
            show_bottom_border=True,
            expand=True,
        )

    def exportar_csv(self, e):
        if not self.df_proposicoes.empty:
            self.df_completo = self.df_proposicoes.merge(
                self.df_votacoes, how='left', on='proposicao_id'
            ).merge(
                self.df_votos, how='left', on='votacao_id'
            )
            
            file_name = f"proposicoes_{self.ano_input.value}_{'_'.join(self.tipos_input.value)}.csv"
            self.df_completo.to_csv(file_name, index=False)
            
            self.status_text.value = f"Dados exportados para {file_name}"
            self.status_text.color = ft.colors.GREEN
            self.page.update()
        else:
            self.status_text.value = "Nenhum dado para exportar"
            self.status_text.color = ft.colors.RED
            self.page.update()

def main(page: ft.Page):
    def route_change(route):
        page.views.clear()
        
        # Menu principal
        if page.route == "/" or not page.route:
            menu = MainMenu(page)
            page.views.append(ft.View("/", [menu.build()]))
        
        # Tela de projetos de lei
        elif page.route == "/projetos":
            proj = ProjetosDeLeiApp(page)
            page.views.append(ft.View("/projetos", [proj.page.controls[0]]))
#            page.views.append(ft.View("/projetos", [ProjetosDeLeiApp(page)]))
        
        page.update()
    
    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)
    
    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route or "/")

if __name__ == '__main__':
    ft.app(target=main)