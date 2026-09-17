import flet as ft

def main(page: ft.Page):
    page.title = "Modo Claro/Escuro"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def alternar_tema(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        construir_tela()

    def construir_tela():
        page.controls.clear()
        escuro = page.theme_mode == ft.ThemeMode.DARK
        
        icone = ft.Icon(
            ft.Icons.LIGHT_MODE if escuro else ft.Icons.DARK_MODE,
            size=60,
            color=ft.Colors.AMBER if escuro else ft.Colors.BLUE_200,
        )
        texto = ft.Text(
            "Modo Escuro Ativado" if escuro else "Modo Claro Ativado",
            size=20,
            weight=ft.FontWeight.BOLD,
            color=ft.Colors.WHITE if escuro else ft.Colors.BLACK,
        )
        botao = ft.ElevatedButton(
            "Ativar Modo Claro" if escuro else "Ativar Modo Escuro",
            on_click=alternar_tema,
        )
        
        page.bgcolor = ft.Colors.BLACK if escuro else ft.Colors.WHITE
        
        page.add(
            ft.Column(
                [ft.Container(height=60), icone, texto, botao],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            )
        )
        page.update()

    construir_tela()

# Chame a função oficial ft.app
ft.app(target=main) 
