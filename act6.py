import flet as ft

def main(page: ft.Page):
    # Configuración inicial de la página
    page.title = "Hello world with Flet"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK  # Modo oscuro

    # Diálogo para mostrar error
    def open_dlg_modal():
        dlg_error = ft.AlertDialog(
            title=ft.Text("Unable to login", size=24),
            content=ft.Text("User or Password incorrect!"),
            actions=[ft.TextButton("Ok", on_click=lambda e: cerrar_dlg(dlg_error))],
        )
        page.dialog = dlg_error
        dlg_error.open = True
        page.update()

    def cerrar_dlg(dialogo):
        dialogo.open = False
        page.update()


    # Función para actualizar el estado del botón
    def actualizar_estado_boton(e):
        boton_login.disabled = not (text_nom.value.strip() and text_preu.value.strip() and text_categoria.value.strip() )
        page.update()

    def btn_click(e):
        Noms.controls.append(ft.Text(text_nom.value))
        preus.controls.append(ft.Text(text_preu.value))
        Categories.controls.append(ft.Text(text_categoria.value))
        text_nom.value = ""
        text_preu.value = ""
        text_categoria.value = ""
        page.update()
        text_nom.focus()
    # Campos de entrada
    text_nom = ft.TextField(label="Nom del Producte", width=300, on_change=actualizar_estado_boton)
    text_preu = ft.TextField(label="Preu", width=300, on_change=actualizar_estado_boton)
    text_categoria = ft.TextField(label="Categoria", width=300, on_change=actualizar_estado_boton)
    
    # Botón de login (inicia deshabilitado)
    boton_login = ft.ElevatedButton("Afegir", on_click=btn_click, disabled=True)
    text = ft.Text("Producte    Preu    tCategoria")
    Noms = ft.Column()
    preus= ft.Column()
    Categories=ft.Column()

    row= ft.Row(
        controls=[Noms,preus,Categories]
    )

    # Agregar elementos a la página
    page.add(
        ft.Column(
            [
                text_nom,
                text_preu,
                text_categoria,
                boton_login,
                text,
                row,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    )

# Ejecutar la aplicación
ft.app(target=main, view="web_browser", port=8080)