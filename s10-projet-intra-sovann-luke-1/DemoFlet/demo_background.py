
import flet as ft


def main(page: ft.Page):
    # La version que t'avait vu était hors date, mais fonctionne encore.
    # Il fallait juste mettre les fonctions en majuscule.
    page.foreground_decoration = ft.BoxDecoration(
        gradient=ft.LinearGradient(
            colors=[
                ft.Colors.with_opacity(0.2, ft.Colors.RED),  # use lightly transparent colors instead of solid ones
                ft.Colors.with_opacity(0.2, ft.Colors.BLUE),
            ],
            stops=[0.0, 1.0],
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
        ),
        image=ft.DecorationImage(
            src="https://images.unsplash.com/photo-1547721064-da6cfb341d50",
            # fit=ft.ImageFit.COVER,
            opacity=0.2,
        ),
    )

    page.add(
        ft.Text("Jiraphe", size=55),
    )


ft.app(main)