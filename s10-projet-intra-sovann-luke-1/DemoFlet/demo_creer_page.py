
# -------------------- Importation --------------------
import flet as ft


# -------------------- DemoFlet --------------------
def principal(page_: ft.Page) -> None:
    # Taille de la page.
    page_.window.width = 1000
    page_.window.height = 500

    COULEURS: list[tuple[str, str]] = [
        ("🔴 Rouge", ft.Colors.RED_100),
        ("🟡 Jaune", ft.Colors.YELLOW_100),
        ("🟢 Vert", ft.Colors.GREEN_100),
        ("🔵 Bleu", ft.Colors.BLUE_100),
    ]

    def changer_fond(couleur_hex: str) -> None:
        """Modifie la couleur de fond de la page."""
        page_.bgcolor = couleur_hex
        page_.update()

    boutons: list[ft.Control] = [
        ft.FilledButton(
            nom,
            # Lambda avec argument par défaut pour figer la valeur dans la boucle
            on_click=lambda e, c=valeur: changer_fond(c),
        )
        for nom, valeur in COULEURS
    ]

    page_.add(ft.Row(boutons, wrap=True))

    def gerer_message(evenement: ft.Event[ft.Switch]) -> None:
        if ma_switch.value:
            afficher_message(evenement)
        else:
            effacer_message(evenement)

    # Gestionnaires d'évènements.
    def afficher_message(e: ft.Event[ft.Button] | ft.Event[ft.Switch]) -> None:
        message.value = "Bonjour"
        page_.update()

    def effacer_message(e: ft.Event[ft.Button] | ft.Event[ft.Switch]) -> None:
        message.value = ""
        page_.update()

    # Assemblage du UI.
    page_.add(
        message := ft.Text(""),
        ft.FilledButton(content="effacer_message", on_click=effacer_message),
        ft.FilledButton(content="afficher_message", on_click=afficher_message),
        ft.Slider(label="On/Off message", value=0),
        ma_switch := ft.Switch(label="Afficher/Effacer", value=False, on_change=gerer_message)
    )




    def basculer_acceptation(evenement: ft.Event[ft.Checkbox]) -> None:
        pass


ft.run(principal)