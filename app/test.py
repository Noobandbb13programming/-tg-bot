import flet as ft
import pandas as pd


# Функция обработки загрузки файла
def upload_file(e, page, table):
    if not e.files:
        return

    file = e.files[0]
    df = pd.read_excel(file.path)
    table.rows = [ft.DataRow(cells=[ft.DataCell(ft.Text(str(df[col][i]))) for col in df.columns]) for i in
                  range(len(df))]
    page.update()


# Основная функция приложения
def main(page: ft.Page):
    page.title = "Карго-перевозки"
    page.bgcolor = ft.colors.GREY_200
    page.padding = 20

    # Заголовок
    header = ft.Text("Система управления карго-перевозками", size=24, weight=ft.FontWeight.BOLD, color=ft.colors.BLUE)

    # Таблица для грузов
    table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Трекинг ID")),
            ft.DataColumn(ft.Text("Описание")),
            ft.DataColumn(ft.Text("Статус")),
        ],
        rows=[],
        border=ft.border.all(1, ft.colors.BLACK),
        heading_row_color=ft.colors.BLUE_100,
        data_row_color=ft.colors.WHITE,
        border_radius=10,
        divider_thickness=1,
    )

    # Поля для добавления нового груза
    tracking_id = ft.TextField(label="Трекинг ID", bgcolor=ft.colors.WHITE, border_radius=10)
    description = ft.TextField(label="Описание", bgcolor=ft.colors.WHITE, border_radius=10)
    status = ft.TextField(label="Статус", bgcolor=ft.colors.WHITE, border_radius=10)

    def add_cargo(e):
        table.rows.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(tracking_id.value)),
                    ft.DataCell(ft.Text(description.value)),
                    ft.DataCell(ft.Text(status.value)),
                ]
            )
        )
        tracking_id.value = description.value = status.value = ""
        page.update()

    add_button = ft.ElevatedButton("Добавить груз", on_click=add_cargo, bgcolor=ft.colors.GREEN, color=ft.colors.WHITE)

    # Кнопка для загрузки Excel-файла
    file_picker = ft.FilePicker(on_result=lambda e: upload_file(e, page, table))
    upload_button = ft.ElevatedButton("Загрузить Excel",
                                      on_click=lambda _: file_picker.pick_files(allow_multiple=False),
                                      bgcolor=ft.colors.ORANGE, color=ft.colors.WHITE)

    # Основной макет
    page.add(
        file_picker,
        header,
        ft.Container(
            content=ft.Column([
                ft.Row([tracking_id, description, status, add_button], alignment=ft.MainAxisAlignment.CENTER,
                       spacing=10),
                ft.Row([upload_button], alignment=ft.MainAxisAlignment.CENTER),
                table
            ], spacing=20, alignment=ft.MainAxisAlignment.CENTER),
            padding=20,
            border_radius=10,
            bgcolor=ft.colors.WHITE,
            shadow=ft.BoxShadow(blur_radius=10, spread_radius=2, color=ft.colors.GREY_500)
        )
    )


ft.app(target=main)