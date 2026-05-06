
# Fichier de Vann Sovannthanant
# -------------------- Importation --------------------
import flet as ft
from pathlib import Path
from Partie import Personnage,Hero,Ennemi,Combat,Action, lire_stats_json

# -------------------- DemoFlet --------------------

# 'lambda' permet d'appeler une fonction sur un 'on_click'.

def interface_combat(page:ft.Page):
    page.theme_mode = 'dark'
    page.window.width = 1500
    page.window.height = 750
    # Empêche l'étirement de la fenêtre.
    page.window.resizable = False
    # Pour le moment le jeu ne sera pas en plein écran.
    page.window.full_screen = False

    # +-+-+-+-+-+- Fonction lier à DemoFlet. +-+-+-+-+-+-
    def systeme_tours(Combat, deja_jouer):
        """Fonction qui créer une fonction qui donne une liste de deja_jouer."""
        nombre_personnage = len(Combat.placement_hero)
        nombre_personnage += len(Combat.placement_ennemi)
        tours_combat = 0
        for act in range(nombre_personnage):
            ordres_personnage = Combat.evaluation_agilite_personnage()
            for personnage in ordres_personnage:
                if personnage not in deja_jouer:
                    deja_jouer.append(personnage.nom)
                return deja_jouer

    def tour_de(deja_jouer):
        """ Retourne à qui est le tour de jouer"""
        index_de = len(deja_jouer)
        return deja_jouer[index_de-1] #nom_index

    def changer_bordure(nom_index, nom):
        if nom_index == nom: ft.Border.all(2, ft.Colors.GREEN),
        if nom_index != nom:
            if nom.type == "HERO":
                ft.Border.all(2, ft.Colors.BLUE),
            if nom.type == "ENNEMI":
                ft.Border.all(2, ft.Colors.RED),

    def test_bouton():
        print("1")

    # +-+-+-+-+-+- Container de tout l'écran. +-+-+-+-+-+-
    # 'padding' est l'espacement depuis les coins et 'border_radius' est
    # l'arrondissement des coins. 'bgcolor' est la couleur d'arrière-plan.
    page.add(ft.SafeArea(expand=True, content=ft.Container(
        border = ft.Border.all(2, ft.Colors.BLUE),
        bgcolor = ft.Colors.BLACK,
        content = ft.Column(expand=True, controls=[
            # +-+-+-+-+-+- Container du haut. +-+-+-+-+-+-
            ft.Container(
                expand = 3,
                padding = 5,
                alignment = ft.Alignment.BOTTOM_CENTER,
                bgcolor = ft.Colors.BLACK_87,
                content = ft.Stack(controls = [
                        # +-+-+- Arrière-plan. +-+-+-
                        ft.Container(
                            expand = 1,
                            alignment = ft.Alignment.TOP_CENTER,
                            border = ft.Border.all(2, ft.Colors.WHITE),
                            border_radius = 00,
                            bgcolor = ft.Colors.TRANSPARENT,
                            content = ft.Image(expand = True, src = "https://"
                            "unblast.com/wp-content/uploads/2021/01/Space-Background"
                            "-Image-4-1024x682.jpg")),
                        # +-+-+- Emplacement des placements. +-+-+-
                        ft.Container(
                            alignment = ft.Alignment.BOTTOM_CENTER, content = (
                            ft.Row(height = 400,controls = [
                                # Container d'espacement.
                                ft.Container(expand=1,height=400),
                                # +-+-+- Emplacement hero.
                                ft.Container(
                                expand = 4,
                                height = 400,
                                border = ft.Border.all(2, ft.Colors.BLUE),
                                content = (
                                    ft.Row(controls = [
                                        # Espace pour presentation du hero.
                                        # +-+-+- Placement hero de la position quatre.
                                        ft.Column(
                                        expand = 1,
                                        height = 400,
                                        controls = [
                                            ft.Container(
                                            expand = 9,
                                            height = 380,
                                            alignment = ft.Alignment.CENTER,
                                            border = ft.Border.all(2, ft.Colors.BLUE_600),
                                            content = ft.Text(nom_hero3)),
                                            ft.Container(
                                            expand = 1,
                                            alignment = ft.Alignment.CENTER,
                                            border = ft.Border.all(2, ft.Colors.BLUE_600),
                                            content = ft.Text(vie_hero3))
                                        ]),
                                        # +-+-+- Placement hero de la position trois.
                                        ft.Column(
                                        expand=1,
                                        height=400,
                                        controls=[
                                            ft.Container(
                                            expand=9,
                                            height=380,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.BLUE_600),
                                            content = ft.Text(nom_hero2)),
                                            ft.Container(
                                            expand=1,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.BLUE_600),
                                            content = ft.Text(vie_hero2))
                                        ]),
                                        # +-+-+- Placement hero de la position deux.
                                        ft.Column(
                                        expand=1,
                                        height=400,
                                        controls=[
                                            ft.Container(
                                            expand=9,
                                            height=380,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.BLUE_600),
                                            content = ft.Text(nom_hero1)),
                                            ft.Container(
                                            expand=1,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.BLUE_600),
                                            content= ft.Text(vie_hero1))
                                        ]),
                                        # +-+-+- Placement hero de la position un.
                                        ft.Column(
                                        expand=1,
                                        height=400,
                                        controls=[
                                            ft.Container(
                                            expand=9,
                                            height=380,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.BLUE_600),
                                            content = ft.Text(nom_hero0)),
                                            ft.Container(
                                            expand=1,
                                            alignment=ft.Alignment.CENTER,
                                            border = ft.Border.all(2, ft.Colors.BLUE_600),
                                            content = ft.Text(vie_hero0),
                                            )
                                            ]),
                                        ])
                                    )),
                                # Container d'espacement.
                                ft.Container(expand = 1,height = 400),
                                # +-+-+- Emplacement ennemi.
                                ft.Container(
                                expand = 4,
                                height = 400,
                                border = ft.Border.all(2, ft.Colors.RED),
                                content = (
                                    ft.Row(
                                    controls = [
                                        # Espace pour presentation de l'ennemi.
                                        # +-+-+- Placement ennemi de la position un.
                                        ft.Column(
                                        expand=1,
                                        height=400,
                                        controls=[
                                            ft.Container(
                                            expand=9,
                                            height=380,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                            content=ft.Text(nom_ennemi0)),
                                            # Espace pour les points de vie de l'ennemi.
                                            ft.Container(
                                            expand=1,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                            content=ft.Text(vie_ennemi0))
                                        ]),
                                        # +-+-+- Placement ennemi de la position deux.
                                        ft.Column(
                                        expand=1,
                                        height=400,
                                        controls=[
                                            ft.Container(
                                            expand=9,
                                            height=380,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                            content=ft.Text(nom_ennemi1)),
                                            ft.Container(
                                            expand=1,
                                            alignment = ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                            content = ft.Text(vie_ennemi1))
                                        ]),
                                        # +-+-+- Placement ennemi de la position trois.
                                        ft.Column(
                                        expand=1,
                                        height=400,
                                        controls=[
                                            ft.Container(
                                            expand=9,
                                            height=380,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                            content=ft.Text(nom_ennemi2)),
                                            ft.Container(
                                            expand=1,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                            content=ft.Text(vie_ennemi2))
                                        ]),
                                        # +-+-+- Placement ennemi de la position quatre.
                                        ft.Column(
                                        expand=1,
                                        height=400,
                                        controls=[
                                            ft.Container(
                                            expand=9,
                                            height=380,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                            content=ft.Text(nom_ennemi3)),
                                            ft.Container(
                                            expand=1,
                                            alignment=ft.Alignment.CENTER,
                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                            content=ft.Text(vie_ennemi3))
                                        ]),
                                    ])
                                )),
                                # Container d'espacement.
                                ft.Container(expand=1,height=400),
                            ])
                        )),
                        # +-+-+-+-+-+- Indicateur de tour +-+-+-+-+-+-.
                        ft.Container( alignment = ft.Alignment.TOP_CENTER, content = (
                            ft.Row(controls = [
                                # Container pour balance.
                                ft.Container(expand=5,height=150),
                                ft.Container(
                                    expand=1,
                                    height=150,
                                    border=ft.Border.all(2, ft.Colors.GREEN),
                                    alignment = ft.Alignment.CENTER,
                                    content = ft.Text("1", size =100)),
                                # Container pour balance.
                                ft.Container(expand=5,height=150)
                                ])
                        ))
                    ]),
                ),
            # +-+-+-+-+-+- Container du bas +-+-+-+-+-+-
            ft.Container(
                expand = 2,
                padding = 5,
                border_radius = 00,
                bgcolor = ft.Colors.GREY_900,
                content = (ft.Row(controls = [
                # Container d'espacement.
                ft.Container(expand = 1,border=ft.Border.all(2, ft.Colors.BLACK)),
                # +-+-+- Container en bas à gauche
                ft.Container(
                    expand = 2,
                    padding = 10,
                    border = ft.Border.all(2, ft.Colors.BLACK),
                    border_radius = 0,
                    bgcolor = ft.Colors.GREY_900,
                    content = ft.Column(controls = [
                    # +-+-+- Boutons d'actions
                        ft.Row(expand = 1, controls=[
                            ft.Container(
                            expand = 1,
                            alignment = ft.Alignment.CENTER,
                            border = ft.Border.all(2, ft.Colors.BLACK),
                            content = ft.Text("Déplacer")),
                            ft.Container(
                            expand = 1,
                            alignment=ft.Alignment.CENTER,
                            border = ft.Border.all(2, ft.Colors.BLACK),
                            content = ft.Text("Attaque de Base")),
                            ft.Container(
                            expand=1,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(2, ft.Colors.BLACK),
                            content = ft.Text("Abilité 1")),
                            ft.Container(
                            expand=1,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(2, ft.Colors.BLACK),
                            content = ft.Text("Abilité 2")),
                            ft.Container(
                            expand=1,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(2, ft.Colors.BLACK),
                            content = ft.Text("Abilité 3")),
                            ft.Container(
                            expand=1,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(2, ft.Colors.BLACK),
                            content = ft.Text("Abilité 4")),
                            ft.Container(
                            expand=1,
                            alignment=ft.Alignment.CENTER,
                            border=ft.Border.all(2, ft.Colors.BLACK),
                            content=ft.Text("Passer"),
                            on_click=test_bouton)
                        ]),
                        ft.Row(expand = 4, controls=[
                            ft.Container(
                            expand=True,
                            alignment = ft.Alignment.TOP_CENTER,
                            border = ft.Border.all(2, ft.Colors.BLACK),
                            border_radius = 00,
                            bgcolor = ft.Colors.GREY_900,
                            content = ft.Text("Description d'abilité"))
                        ]),
                    ])),
                # +-+-+- Container en bas à droite.
                ft.Container(
                expand = 2,
                alignment = ft.Alignment.TOP_CENTER,
                border = ft.Border.all(2, ft.Colors.BLACK),
                border_radius = 00,
                bgcolor = ft.Colors.GREY_900,
                content = ft.Row(controls = [
                    ft.Text("tour_personnage")
                ])),
                # Container d'espacement.
                ft.Container(expand=1,border=ft.Border.all(2, ft.Colors.BLACK)),
            ])
        ))
    ]))))

if __name__ == "__main__":
    dict_ennemi = lire_stats_json("Partie/Fichiers/Type_ennemi.json")
    dict_scene = lire_stats_json("Partie/Fichiers/Dictionnaire_scenario.json")
    dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
    dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
    chem_heros = "Partie/Fichiers/Type_Hero.json"

    dossier_parent = Path(__file__).parent

    combat = Combat([], [], "FORET")
    combat.inserer_heros(dict_heros, dict_type_hero)
    nom_hero0 = combat.placement_hero[0].nom
    nom_hero1 = combat.placement_hero[1].nom
    nom_hero2 = combat.placement_hero[2].nom
    nom_hero3 = combat.placement_hero[3].nom
    vie_hero0 = f"{combat.placement_hero[0].stats["point_vie"]}/{combat.placement_hero[0].stats["point_vie_max"]}"
    vie_hero1 = f"{combat.placement_hero[1].stats["point_vie"]}/{combat.placement_hero[1].stats["point_vie_max"]}"
    vie_hero2 = f"{combat.placement_hero[2].stats["point_vie"]}/{combat.placement_hero[2].stats["point_vie_max"]}"
    vie_hero3 = f"{combat.placement_hero[3].stats["point_vie"]}/{combat.placement_hero[3].stats["point_vie_max"]}"
    combat.generer_ennemis(dict_scene, dict_ennemi)
    nom_ennemi0 = combat.placement_ennemi[0].stats_ajouter
    nom_ennemi1 = combat.placement_ennemi[1].stats_ajouter
    nom_ennemi2 = combat.placement_ennemi[2].stats_ajouter
    nom_ennemi3 = combat.placement_ennemi[3].stats_ajouter
    vie_ennemi0 = f"{combat.placement_ennemi[0].stats["point_vie"]}/{combat.placement_ennemi[0].stats["point_vie_max"]}"
    vie_ennemi1 = f"{combat.placement_ennemi[1].stats["point_vie"]}/{combat.placement_ennemi[1].stats["point_vie_max"]}"
    vie_ennemi2 = f"{combat.placement_ennemi[2].stats["point_vie"]}/{combat.placement_ennemi[2].stats["point_vie_max"]}"
    vie_ennemi3 = f"{combat.placement_ennemi[3].stats["point_vie"]}/{combat.placement_ennemi[3].stats["point_vie_max"]}"

    ordre_personnage = combat.evaluation_agilite_personnage()

    ft.run(interface_combat)