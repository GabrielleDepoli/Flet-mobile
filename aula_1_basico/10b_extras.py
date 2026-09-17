
import flet as ft

# Cores de prioridade
PRIORITY_COLOR = {
    "alta": "#FF6B6B",
    "media": "#F2C94C",
    "baixa": "#6FCF97"
}

PRIORITY_LABEL = {
    "alta": "Alta",
    "media": "Média",
    "baixa": "Baixa"
}

# Cores das telas
BG_LISTA = "#161B33"
BG_NOVA = "#241B3D"
BG_DETALHE = "#1B2E3D"
BG_DESTAQUE = "#5C7CFA"


def main(page: ft.Page):
    page.title = "App de Tarefas"

    tasks = [
        {
            "id": 1,
            "title": "Estudar Flet",
            "description": "Terminar os mini-exercícios da Aula 1.",
            "priority": "alta",
            "done": False
        },
        {
            "id": 2,
            "title": "Revisar POO em Python",
            "description": "Classes, atributos e métodos.",
            "priority": "media",
            "done": False
        },
    ]

    next_id = [3]

    # ---------- Tela: Lista de tarefas ----------

    def build_task_row(t):
        def ir_para_detalhe(e):
            page.go(f"/tarefa/{t['id']}")

        def alternar_concluida(e):
            t["done"] = e.control.value
            atualizar_lista()

        titulo = ft.Text(
            t["title"],
            expand=True,
            color="#6E7695" if t["done"] else "#E9ECFB",
            max_lines=1,
            overflow=ft.TextOverflow.ELLIPSIS,
        )

        return ft.Container(
            padding=12,
            border_radius=10,
            bgcolor="#232A4D",
            content=ft.Row(
                controls=[
                    ft.Checkbox(
                        value=t["done"],
                        on_change=alternar_concluida,
                        active_color=BG_DESTAQUE,
                    ),
                    ft.Container(
                        width=10,
                        height=10,
                        border_radius=5,
                        bgcolor=PRIORITY_COLOR[t["priority"]],
                    ),
                    titulo,
                    ft.Icon(
                        ft.Icons.CHEVRON_RIGHT,
                        color="#8892C4",
                    ),
                ]
            ),
            on_click=ir_para_detalhe,
        )

    # Campo de busca
    busca = ft.TextField(
        label="Buscar tarefa pelo título",
        prefix_icon=ft.Icons.SEARCH,
        width=340,
        color="#FFFFFF",
        label_style=ft.TextStyle(color="#B7A9E0"),
        border_color="#4A3F7A",
        focused_border_color=BG_DESTAQUE,
        on_change=lambda e: atualizar_lista(),
    )

    # Contador de tarefas
    contador = ft.Text(
        color="#D8CFF2",
        size=16,
        weight=ft.FontWeight.BOLD,
    )

    # Lista visual
    lista_view = ft.ListView(
        expand=True,
        spacing=8,
        width=340,
    )

    def atualizar_lista():
        # Conta todas as tarefas, não apenas as filtradas
        concluidas = sum(1 for t in tasks if t["done"])
        total = len(tasks)

        contador.value = f"{concluidas} de {total} tarefas concluídas"

        # Filtra pelo título
        termo = (busca.value or "").strip().lower()

        tarefas_filtradas = [
            t for t in tasks
            if termo in t["title"].lower()
        ]

        # Ordena: alta → média → baixa
        ordem = {
            "alta": 0,
            "media": 1,
            "baixa": 2
        }

        tarefas_filtradas.sort(
            key=lambda t: ordem[t["priority"]]
        )

        # Atualiza as linhas
        lista_view.controls.clear()

        for t in tarefas_filtradas:
            lista_view.controls.append(build_task_row(t))

        page.update()

    def view_lista():
        return ft.View(
            route="/",
            appbar=ft.AppBar(
                title=ft.Text("Minhas Tarefas")
            ),
            bgcolor=BG_LISTA,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=ft.Padding(
                top=30,
                bottom=60,
                left=0,
                right=0,
            ),
            controls=[
                contador,
                busca,
                lista_view,
            ],
            floating_action_button=ft.FloatingActionButton(
                icon=ft.Icons.ADD,
                on_click=lambda e: page.go("/nova"),
                bgcolor=BG_DESTAQUE,
            ),
        )

    # ---------- Tela: Nova tarefa / Editar tarefa ----------

    def view_nova(task_id=None):
        # Se recebeu um ID, procura a tarefa para editar
        tarefa = None

        if task_id is not None:
            tarefa = next(
                (t for t in tasks if t["id"] == task_id),
                None
            )

        titulo = ft.TextField(
            label="Título",
            width=300,
            color="#FFFFFF",
            label_style=ft.TextStyle(color="#B7A9E0"),
            border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
            value=tarefa["title"] if tarefa else "",
        )

        descricao = ft.TextField(
            label="Descrição",
            multiline=True,
            min_lines=3,
            width=300,
            color="#FFFFFF",
            label_style=ft.TextStyle(color="#B7A9E0"),
            border_color="#4A3F7A",
            focused_border_color=BG_DESTAQUE,
            value=tarefa["description"] if tarefa else "",
        )

        prioridade = ft.RadioGroup(
            value=tarefa["priority"] if tarefa else "media",
            content=ft.Row(
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Radio(
                        value="alta",
                        label="Alta",
                        label_style=ft.TextStyle(color="#D8CFF2"),
                        fill_color=BG_DESTAQUE,
                    ),
                    ft.Radio(
                        value="media",
                        label="Média",
                        label_style=ft.TextStyle(color="#D8CFF2"),
                        fill_color=BG_DESTAQUE,
                    ),
                    ft.Radio(
                        value="baixa",
                        label="Baixa",
                        label_style=ft.TextStyle(color="#D8CFF2"),
                        fill_color=BG_DESTAQUE,
                    ),
                ],
            ),
        )

        def salvar(e):
            if not titulo.value or not titulo.value.strip():
                titulo.error_text = "Informe um título"
                page.update()
                return

            if tarefa:
                # Atualiza a tarefa existente
                tarefa["title"] = titulo.value.strip()
                tarefa["description"] = descricao.value or ""
                tarefa["priority"] = prioridade.value
            else:
                # Cria uma nova tarefa
                tasks.append({
                    "id": next_id[0],
                    "title": titulo.value.strip(),
                    "description": descricao.value or "",
                    "priority": prioridade.value,
                    "done": False,
                })

                next_id[0] += 1

            # Atualiza a lista e volta para ela
            atualizar_lista()
            page.go("/")

            page.snack_bar = ft.SnackBar(
                ft.Text(
                    "Tarefa atualizada com sucesso!"
                    if tarefa
                    else "Tarefa criada com sucesso!"
                )
            )
            page.snack_bar.open = True
            page.update()

        return ft.View(
            route=f"/editar/{task_id}" if tarefa else "/nova",
            appbar=ft.AppBar(
                title=ft.Text(
                    "Editar tarefa" if tarefa else "Nova tarefa"
                )
            ),
            bgcolor=BG_NOVA,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=ft.Padding(
                top=60,
                bottom=60,
                left=0,
                right=0,
            ),
            controls=[
                titulo,
                descricao,
                ft.Text("Prioridade:", color="#D8CFF2"),
                prioridade,
                ft.ElevatedButton(
                    "Salvar alterações" if tarefa else "Salvar",
                    on_click=salvar,
                    bgcolor=BG_DESTAQUE,
                    color="#161B33",
                ),
            ],
        )

    # ---------- Tela: Detalhe da tarefa ----------

    def view_detalhe(task_id):
        tarefa = next(
            (t for t in tasks if t["id"] == task_id),
            None
        )

        if tarefa is None:
            return ft.View(
                route=f"/tarefa/{task_id}",
                appbar=ft.AppBar(
                    title=ft.Text("Tarefa não encontrada")
                ),
                bgcolor=BG_DETALHE,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        "Essa tarefa não existe (ou já foi excluída).",
                        color="#D6E8F0",
                    )
                ],
            )

        def editar(e):
            page.go(f"/editar/{task_id}")

        def excluir_confirmado(e):
            tasks.remove(tarefa)
            dialogo.open = False

            atualizar_lista()
            page.go("/")

            page.snack_bar = ft.SnackBar(
                ft.Text("Tarefa excluída.")
            )
            page.snack_bar.open = True
            page.update()

        def cancelar(e):
            dialogo.open = False
            page.update()

        dialogo = ft.AlertDialog(
            title=ft.Text("Excluir tarefa?"),
            content=ft.Text(
                "Essa ação não pode ser desfeita."
            ),
            actions=[
                ft.TextButton(
                    "Cancelar",
                    on_click=cancelar,
                ),
                ft.TextButton(
                    "Excluir",
                    on_click=excluir_confirmado,
                ),
            ],
        )

        def abrir_dialogo_exclusao(e):
            page.dialog = dialogo
            dialogo.open = True
            page.update()

        return ft.View(
            route=f"/tarefa/{task_id}",
            appbar=ft.AppBar(
                title=ft.Text("Detalhe da tarefa")
            ),
            bgcolor=BG_DETALHE,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            padding=ft.Padding(
                top=60,
                bottom=60,
                left=0,
                right=0,
            ),
            controls=[
                ft.Text(
                    tarefa["title"],
                    size=24,
                    weight=ft.FontWeight.BOLD,
                    color="#D6E8F0",
                ),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Container(
                            width=12,
                            height=12,
                            border_radius=6,
                            bgcolor=PRIORITY_COLOR[tarefa["priority"]],
                        ),
                        ft.Text(
                            f"Prioridade {PRIORITY_LABEL[tarefa['priority']]}",
                            color="#A9C7D6",
                        ),
                    ],
                ),
                ft.Text(
                    tarefa["description"] or "(sem descrição)",
                    color="#D6E8F0",
                    text_align=ft.TextAlign.CENTER,
                ),
                ft.ElevatedButton(
                    "Editar",
                    icon=ft.Icons.EDIT,
                    on_click=editar,
                    bgcolor=BG_DESTAQUE,
                    color="#161B33",
                ),
                ft.ElevatedButton(
                    "Excluir",
                    icon=ft.Icons.DELETE,
                    on_click=abrir_dialogo_exclusao,
                    bgcolor="#FF6B6B",
                    color="#1B2E3D",
                ),
            ],
        )

    # ---------- Roteamento ----------

    def route_change(e):
        page.views.clear()
        page.views.append(view_lista())

        if page.route == "/nova":
            page.views.append(view_nova())

        elif page.route.startswith("/editar/"):
            task_id = int(page.route.split("/")[-1])
            page.views.append(view_nova(task_id))

        elif page.route.startswith("/tarefa/"):
            task_id = int(page.route.split("/")[-1])
            page.views.append(view_detalhe(task_id))

        page.update()

    def view_pop(e):
        if len(page.views) > 1:
            page.views.pop()
            page.go(page.views[-1].route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    atualizar_lista()
    route_change(None)


ft.app(main)