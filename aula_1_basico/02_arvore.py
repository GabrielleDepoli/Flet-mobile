import flet as ft

def main(page: ft.Page):
    page.title = "Árvore de controles"

    # Cor de fundo
    page.bgcolor = "#16BA4A"

    # Define o tamanho da tela 
    page.window.width = 320
    page.window.height = 600

    # Centalizar elementos
    page.horizontal_alignment=ft.CrossAxisAlignment.CENTER

    # Padding
    page.padding = ft.Padding(top=60, bottom=60, left=0, right=0)

    # Container principal que representa o "cartão" visual
    cartao = ft.Container(
        content=ft.Column(
            horizontal_alignment = ft.CrossAxisAlignment.CENTER,
            controls=[
                # Título do Cartão: texto maior, negrito e cor de destaque
                ft.Text(
                    "Título do Cartão",
                    size=20,
                    weight=ft.FontWeight.BOLD,
                    color= "#1FE0C4",
                ), 
                # Texto descritivo (abaixo do título)
                ft.Text("Descrição do cartão", color="#CFEFE9"),

                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.ElevatedButton(
                            "Ação 1",
                            bgcolor= "#1FE0C4",
                            color= "#0B3D3A"                           
                        ), # Botão de destaque
                        ft.OutlinedButton("Ação 2"), # Botão secundário
                    ]
                ),
            ]
        ),
    
        padding=16, #Espaçamento interno entre o conteúdo
        bgcolor="#123C3C", # Cor de fundo ("Row" - Arranjo em linha)
        border_radius=12, # Arredondamento de canto
    )
    #Adicionando cartão à página
    page.add(cartao)

ft.run(main)