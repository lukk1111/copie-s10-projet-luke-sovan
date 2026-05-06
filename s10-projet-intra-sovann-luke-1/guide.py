
# Fichier de Vann Sovannthanant et de Luke Immanuel Legaspina.
# -------------------- Importation --------------------
from Partie import (lire_stats_json, Hero, Ennemi)
from Partie import Personnage, Hero, Ennemi, Combat, Action, CombatControl, UI_COMBAT
from dataclasses import field
from datetime import datetime
from typing import Callable
from pathlib import Path
import flet as ft
import asyncio
import json
import sys
import random

from Partie.CombatControl import CombatController


# -------------------- Interface DemoFlet --------------------
"""
Code de commentaire:
    Page DemoFlet: +-+-+-+-+-+-+-+-+-+-+-+-
    Partie essentiel: =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-"""

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=- La fonction main =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def main(page: ft.Page):
    page.title = "Menu Principal"
    page.width = 1500
    page.height = 750
    page.theme_mode = 'dark'
    # Empêche la page de pouvoir être tirer/rétrécie.
    page.window.resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.update()

    # =-=-=-=-=-=-=-=-=-=-=-=-=-=-=- Navigation entre les pages =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    async def open_creation_heros(e):
        await page.push_route("/creation_heros")

    async def open_jouer_jeu(e):
        await page.push_route("/jouer")

    async def open_combat(e):
        await page.push_route("/jouer/combat")


    # +-+-+-+-+-+-+-+-+-+-+-+- Page du menu principal +-+-+-+-+-+-+-+-+-+-+-+-
    def quitter_app():
        sys.exit(1)

    def menu_principal():
        print("Route change:", page.route)
        page.views.clear()
        page.views.append(
        # Cette partie est pour le fonctionnement.
            ft.View(route="/",controls=[
                ft.SafeArea(expand=True, content=

        # Partie qui apparait sur l'interface.
                    ft.Row(expand=True, controls=[
                        # Container d'espacement.
                        ft.Container(
                            expand = 1),
                        ft.Container(
                            expand=1,
                            border=ft.Border.symmetric(
                                horizontal=ft.BorderSide(8, ft.Colors.GREY)),
                            content=
                            ft.Column(expand=1, controls=[
                                ft.AppBar(
                                    title=ft.Text("⚔️ (TEMU) Darkest Dungeon 🛡️",
                                    align= ft.Alignment.CENTER)),
                                ft.Button(f"Jouer",
                                    on_click=open_jouer_jeu,
                                    align= ft.Alignment.CENTER),
                                ft.Button("Quitter",
                                    on_click= lambda e: quitter_app(),
                                    align = ft.Alignment.CENTER)
                                ])
                            ),
                        # Container d'espacement.
                        ft.Container(
                            expand=1)
                    ])
                )])) # Crochets et parenthèses du fonctionnement.

        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.update()

        # +-+-+-+-+-+-+-+-+-+-+-+- Page pour jouer +-+-+-+-+-+-+-+-+-+-+-+-
        output = ft.Text()
        dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
        date_modif = "Partie/Fichiers/Derniere_date_modification.txt"
        with open(date_modif, mode="r", encoding="utf-8") as fichier:
            dernier_date = fichier.read()
        try:
            texte = ""
            for nom, classes in dict_heros.items():
                for classe, stats in classes.items():
                    texte += f"{nom} ({classe})\n"
                    texte += f"  Vie: {stats['point_vie']}/{stats['point_vie_max']}\n"
                    texte += f"  Mêlée: {stats['degat_melee']} | Distance: {stats['degat_distance']}\n"
                    texte += f"  Agilité: {stats['point_agilite']} | Chance: {stats['point_chance']}\n\n"
            texte += f"\nDernière modification: {dernier_date}"
            output.value = texte if texte else "Aucun héros trouvé."
        except FileNotFoundError:
            output.value = "Fichier heros.json introuvable."
        except Exception as err:
            output.value = f"Error: {err}"
        page.update()

        if page.route == "/jouer" or page.route == "/jouer":
            # Cette partie est pour le fonctionnement.
            page.views.append(
                ft.View(route="/jouer", controls=[
                    ft.SafeArea(expand=True, content=

                    ft.Column(controls=[
                        ft.AppBar(
                            title=ft.Text("Preparation pour jouer", align=ft.Alignment.CENTER_LEFT),
                            bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                        ft.Row(expand=True, controls=[
                            # Container d'espacement.
                            ft.Container(
                                expand=1,
                                border=ft.Border.all(2, ft.Colors.BLACK)),
                            ft.Container(
                                expand=1,
                                padding=20,
                                border=ft.Border.all(2, ft.Colors.GREY),
                                content=(
                                ft.Column(controls=[
                                    ft.Text(
                                        "Avant de commencer vous devriez avoir au moins 1 héro et maximum 4 héros. "
                                        "Le moins d'héros vous avez, le plus difficile seront les combats.:\n\n"
                                        "Votre Équipe: ----->",
                                        align=ft.Alignment.CENTER,
                                        theme_style=ft.TextThemeStyle.BODY_MEDIUM),
                                    ft.Button("Gérer l'équipe d'héros",
                                        on_click=open_creation_heros,
                                        align=ft.Alignment.CENTER),
                                    ft.Button("Commencer le combat",
                                        on_click=open_combat,
                                        align=ft.Alignment.CENTER),
                                ])
                            )),
                            ft.Container(
                                padding=10,
                                expand=True,
                                alignment = ft.Alignment.TOP_CENTER,
                                border_radius=10,
                                border=ft.Border.all(2, ft.Colors.GREY),
                                content=output),
                            # Container d'espacement.
                            ft.Container(
                                expand=1,
                                border=ft.Border.all(2, ft.Colors.BLACK)),
                            ]),
                        ])
                    )]))  # Crochets et paranthèses du fonctionnement.


        # =-=-=-=-=-=-=-=-=- Fonctions pour création Héro =-=-=-=-=-=-=-=-=-
        if page.route == "/creation_heros" or page.route == "/creation_heros/classes_personnages":
            # TextField (Inputs)
            nom_input = ft.TextField(label="Nom de l'héro")
            class_input = ft.TextField(label="Class de l'héro")
            output = ft.Text()

            def afficher_heros(e):
                """Fonction qui affiche tous les héros dans Dictionnaire_hero."""
                dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
                date_modif = "Partie/Fichiers/Derniere_date_modification.txt"
                with open(date_modif, mode="r", encoding="utf-8") as fichier:
                    dernier_date = fichier.read()
                try:
                    texte = ""
                    for nom, classes in dict_heros.items():
                        for classe, stats in classes.items():
                            texte += f"{nom} ({classe})\n"
                            texte += f"  Vie: {stats['point_vie']}/{stats['point_vie_max']}\n"
                            texte += f"  Mêlée: {stats['degat_melee']} | Distance: {stats['degat_distance']}\n"
                            texte += f"  Agilité: {stats['point_agilite']} | Chance: {stats['point_chance']}\n\n"
                    texte += f"\nDernière modification: {dernier_date}"
                    output.value = texte if texte else "Aucun héros trouvé."
                except FileNotFoundError:
                    output.value = "Fichier heros.json introuvable."
                except Exception as err:
                    output.value = f"Error: {err}"
                page.update()


            def afficher_classes(e):
                """Fonction qui affiche tous les classes héros dans /creation_heros."""
                dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
                texte = ""
                les_types_hero = []
                for type_hero, ___ in dict_type_hero.items():
                    les_types_hero.append(type_hero)
                for index, type_hero in enumerate(les_types_hero):
                    texte += f"{index + 1}. {type_hero}\n"
                    for type_heroi, ___ in dict_type_hero.items():
                        if type_hero == type_heroi: texte += f"{___["description"]}\n\n"
                output.value = texte
                page.update()


            def creation_hero(e):
                """Fonction qui créer un hero dans le dictionnaire_hero.json."""
                dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
                dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
                chem_heros = "Partie/Fichiers/Dictionnaire_hero.json"
                date_modif = "Partie/Fichiers/Derniere_date_modification.txt"
                nom = nom_input.value.upper()
                nom = nom.lstrip()  # Enlève l'espace avant.
                nom = nom.rstrip()  # Enlève l'espace arrière.
                def confirmer_creation():
                    try:
                        nom_valide = True
                        if nom == "":
                            output.value = f"Le héro doit avoir un nom."
                            nom_valide = False
                        if nom_valide == True:
                            hero = Hero(nom, "HERO")
                            hero.attribuer_hero()

                            class_hero = class_input.value.upper()
                            hero.attribuer_stat(class_hero, dict_type_hero)
                            hero.ecrire_stats_hero(chem_heros, dict_heros)

                            dernier_date = datetime.today()
                            dernier_date = dernier_date.strftime("%Y-%m-%d %H:%M")
                            with open(date_modif, mode="w", encoding="utf-8") as fichier:
                                fichier.write("\n" + str(dernier_date))

                            output.value = f"Le Héro à été créer\n\n {hero}."
                    except Exception as err:
                        output.value = f"Error: {err}"
                    page.update()

                dialog_choix_creation = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Confirmation"),
                    content=ft.Text(f"Voulez vous vraiment ajouter {nom}"),
                    actions=[
                        ft.TextButton("Oui", on_click=lambda e: (page.pop_dialog(), confirmer_creation()), ),
                        ft.TextButton("Non", on_click=lambda e: (page.pop_dialog()))],
                    actions_alignment=ft.MainAxisAlignment.END,
                    on_dismiss=lambda e: print("dialog_choix_creation enlevé"))
                page.show_dialog(dialog_choix_creation)


            def supprimer_hero(e):
                """ Fonction qui enlève un hero dans le dictionnaire_hero.json."""
                dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
                chem_heros = "Partie/Fichiers/Dictionnaire_hero.json"
                date_modif = "Partie/Fichiers/Derniere_date_modification.txt"
                nom = nom_input.value.upper()
                nom = nom.lstrip()
                nom = nom.rstrip()
                def confirmer_supprimer():
                    for nom_dans_dict, ___ in dict_heros.items():
                        if nom == nom_dans_dict:
                            output.value = f"{nom} à été effacé."
                            contenu_json = lire_stats_json(chem_heros)
                            del dict_heros[nom]
                            del contenu_json[nom]
                            contenu_json.update()
                            with open(chem_heros, mode="w", encoding="utf-8") as fichier:
                                json.dump(contenu_json, fichier, indent=4, ensure_ascii=False)

                            # Création de la dernière date.
                            dernier_date = datetime.today()
                            dernier_date = dernier_date.strftime("%Y-%m-%d %H:%M")
                            with open(date_modif, mode="w", encoding="utf-8") as fichier:
                                fichier.write("\n" + str(dernier_date))

                            break
                        elif nom == "":output.value = f"Entrez un nom à enlevez."
                        else:output.value = f"{nom} n'est pas dans l'équipe."
                    page.update()

                dialog_choix_supprimer = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Confirmation"),
                    content=ft.Text(f"Voulez vous vraiment supprimer {nom}"),
                    actions=[
                        ft.TextButton("Oui", on_click=lambda e: (page.pop_dialog(), confirmer_supprimer()),),
                        ft.TextButton("Non", on_click=lambda e: (page.pop_dialog()))],
                    actions_alignment=ft.MainAxisAlignment.END,
                    on_dismiss=lambda e: print("dialog_choix_supprimer enlevé"))
                page.show_dialog(dialog_choix_supprimer)


            # +-+-+-+-+-+-+-+-+-+-+-+- Page de Création des héros +-+-+-+-+-+-+-+-+-+-+-+-
            # Cette partie est pour le fonctionnement.
            page.views.append(
                ft.View(route="/creation_heros", controls=[
                    ft.SafeArea(expand=True, content=

                        # À partir de cette ligne, tout ce qui est mis s'ajoutera à l'interface.
                        ft.Column(controls=[
                            ft.AppBar(
                                title=ft.Text("Création de vos héros!", align= ft.Alignment.CENTER),
                                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST),
                            ft.Row(expand=True, controls=[
                                # Container d'espacement.
                                ft.Container(
                                    expand=1,
                                    border=ft.Border.all(2, ft.Colors.BLACK)),
                                # Container de création.
                                ft.Container(
                                    padding=20,
                                    expand=2,
                                    border=ft.Border.all(2, ft.Colors.GREY),
                                    content = (
                                    ft.Column(
                                        expand=True,
                                        controls=[
                                        ft.Container(content=ft.Text(
                                            "Pour commencer, il vous faut des héros. (1 minimum et 4 maximum) "
                                            "Attribuer lui un nom et une classe, il n'est pas obligé d'en avoir.",
                                            theme_style=ft.TextThemeStyle.BODY_MEDIUM)),
                                        ft.ElevatedButton("Voir votre équipe", on_click=afficher_heros),

                                        ft.Container(content=ft.Text(f"{"-"*60}\n\tAjouter")),
                                        nom_input, # TextField
                                        class_input, # TextField
                                        ft.ElevatedButton("Voir les classes disponible", on_click=afficher_classes),
                                        ft.ElevatedButton("Confirmer le choix", on_click=creation_hero),
                                        ft.Container(content=ft.Text(
                                            f"Entrez au dessus le nom de l'héro que vous voulez enlever.")),
                                        ft.ElevatedButton("Enlever l'héro", on_click=supprimer_hero),
                                        ])
                                    )),
                                # Container d'information.
                                ft.Container(
                                    padding=50,
                                    expand=2,
                                    border_radius=10,
                                    border=ft.Border.all(2, ft.Colors.GREY),
                                    # OUTPUT ----------------------------
                                    content = output),
                                # Container d'espacement.
                                ft.Container(
                                    expand=1,
                                    border=ft.Border.all(2, ft.Colors.BLACK)),
                            ]),
                        ])
                )])) # Crochets et paranthèses du fonctionnement.


        # +-+-+-+-+-+-+-+-+-+-+-+- Page pour combat (Probablement enlever) +-+-+-+-+-+-+-+-+-+-+-+-
        # TODO COMBAT ---------------------------------------------------------------------------------------------------
        if page.route == "/jouer/combat":
            # -------------------- fichiers nécessaires du jeu --------------------
            dict_ennemi = lire_stats_json("Partie/Fichiers/Type_ennemi.json")
            dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
            dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
            chem_heros = "Partie/Fichiers/Type_Hero.json"
            # -------------------- dict pour Combat
            dict_scene = lire_stats_json("Partie/Fichiers/Dictionnaire_scenario.json")
            # -------------------- dict pour Action
            dict_abilite = lire_stats_json("Partie/Fichiers/Abilite_Hero.json")

            # 1 hero minimum, 4 heros maximum.

            controller = CombatController({
                "heros": dict_heros,
                "ennemi": dict_ennemi,
                "abilite": dict_abilite,
                "scene": dict_scene,
                "type_hero": dict_type_hero
            })

            controller.init_combat()

            tour_actuel = 1

            def refresh():
                page.views[-1] = build_view()
                page.update()

            def on_attack_click(e):
                perso = controller.current()
                type_perso = perso.stats_ajouter

                actions = controller.dict_abilite[type_perso]["ACTION_ATTAQUE"]
                controller.available_actions = list(actions.keys())

                refresh()

            def on_action_select(action_name):
                controller.action = action_name
                refresh()

            def on_enemy_click(index):
                if controller.action is None:
                    return

                cible = controller.combat.placement_ennemi[index]
                controller.do_action(cible)

                refresh()

            hero_columns = []

            for hero in controller.combat.placement_hero:
                actif = controller.current() == hero


            tour_actuel = 1


            # -------------------- BOUCLE DE COMBAT --------------------

            page.views.append(
                ft.View(route="/jouer", controls=[
                    ft.SafeArea(expand=True, content=
                    ft.Container(
                        expand=True,
                        padding=0,
                        border=ft.Border.all(2, ft.Colors.BLUE),
                        border_radius=00,
                        bgcolor=ft.Colors.BLACK,  # Couleur arrière-plan.
                        content=ft.Column(expand=True, height=page.height, controls=[
                            # Container du haut.
                            ft.Container(
                                expand=3,
                                padding=5,
                                alignment=ft.Alignment.BOTTOM_CENTER,
                                bgcolor=ft.Colors.BLACK_87,
                                content=ft.Stack(controls=[
                                    # +-+-+- Arrière-plan. +-+-+-
                                    ft.Container(
                                        expand=1,  # 1 avant
                                        alignment=ft.Alignment.CENTER,  # TOP_CENTER AVANT
                                        border=ft.Border.all(3, ft.Colors.WHITE),
                                        border_radius=00,
                                        bgcolor=ft.Colors.TRANSPARENT,
                                        content=ft.Image(expand=True, width=4000,
                                                         src="https://wallpapers.com/images/hd/pure-black-background-py9pa0f1mlsscm9s.jpg")),
                                    # +-+-+- Emplacement des placements. +-+-+-
                                    ft.Container(
                                        alignment=ft.Alignment.BOTTOM_CENTER, content=(
                                            ft.Row(height=400, controls=[
                                                # Container d'espacement.
                                                ft.Container(expand=1, height=400),
                                                # +-+-+- Emplacement hero.
                                                ft.Container(
                                                    expand=4,
                                                    height=400,
                                                    border=ft.Border.all(2, ft.Colors.BLUE),
                                                    content=(
                                                        ft.Row(controls=[
                                                            # Espace pour presentation du hero.
                                                            # +-+-+- Placement hero de la position quatre.
                                                            ft.Column(
                                                                expand=1,
                                                                height=400,
                                                                controls=[
                                                                    ft.Container(
                                                                        expand=9,
                                                                        height=380,
                                                                        alignment=ft.Alignment.CENTER,
                                                                        border=ft.Border.all(2, ft.Colors.BLUE_600),
                                                                        content=ft.Text(nom_hero3, size=15,
                                                                                        font_family="Verdana")),

                                                                    # IMAGE GUERRIER
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://i.pinimg.com/originals/8d/6f/f3/8d6ff31f94e244db66e9e96bb87dfa70.gif")
                                                                    ) if type_hero3 == "GUERRIER" else ft.Container(),

                                                                    # IMAGE CHASSEUR
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://isaacostlund.io/wp-content/uploads/2018/08/Archer-F-gif.gif")
                                                                    ) if type_hero3 == "CHASSEUR" else ft.Container(),

                                                                    # IMAGE SUPPORT
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://i.pinimg.com/originals/9c/6d/a8/9c6da87a758a7e919f54e564d9930bbe.gif")
                                                                    ) if type_hero3 == "SUPPORT" else ft.Container(),

                                                                    ft.Container(
                                                                        expand=2,
                                                                        alignment=ft.Alignment.CENTER,
                                                                        border=ft.Border.all(2, ft.Colors.BLUE_600),
                                                                        content=ft.Text(vie_hero3))
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
                                                                        content=ft.Text(nom_hero2, size=15,
                                                                                        font_family="Verdana")),

                                                                    # EMOJI GUERRIER
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://i.pinimg.com/originals/8d/6f/f3/8d6ff31f94e244db66e9e96bb87dfa70.gif")
                                                                    ) if type_hero2 == "GUERRIER" else ft.Container(),

                                                                    # IMAGE CHASSEUR
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://isaacostlund.io/wp-content/uploads/2018/08/Archer-F-gif.gif")
                                                                    ) if type_hero2 == "CHASSEUR" else ft.Container(),

                                                                    # IMAGE SUPPORT
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://i.pinimg.com/originals/9c/6d/a8/9c6da87a758a7e919f54e564d9930bbe.gif")
                                                                    ) if type_hero2 == "SUPPORT" else ft.Container(),

                                                                    ft.Container(
                                                                        expand=2,
                                                                        alignment=ft.Alignment.CENTER,
                                                                        border=ft.Border.all(2, ft.Colors.BLUE_600),
                                                                        content=ft.Text(vie_hero2))
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
                                                                        content=ft.Text(nom_hero1, size=15,
                                                                                        font_family="Verdana")),

                                                                    # EMOJI GUERRIER
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://i.pinimg.com/originals/8d/6f/f3/8d6ff31f94e244db66e9e96bb87dfa70.gif")
                                                                    ) if type_hero1 == "GUERRIER" else ft.Container(),

                                                                    # IMAGE CHASSEUR
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://isaacostlund.io/wp-content/uploads/2018/08/Archer-F-gif.gif")
                                                                    ) if type_hero1 == "CHASSEUR" else ft.Container(),

                                                                    # IMAGE SUPPORT
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://i.pinimg.com/originals/9c/6d/a8/9c6da87a758a7e919f54e564d9930bbe.gif")
                                                                    ) if type_hero1 == "SUPPORT" else ft.Container(),

                                                                    ft.Container(
                                                                        expand=2,
                                                                        alignment=ft.Alignment.CENTER,
                                                                        border=ft.Border.all(2, ft.Colors.BLUE_600),
                                                                        content=ft.Text(vie_hero1))
                                                                ]),
                                                            # +-+-+- Placement hero de la position un.
                                                            ft.Column(
                                                                expand=1,
                                                                height=400,
                                                                controls=[
                                                                    ft.Container(
                                                                        expand=9,
                                                                        height=400,
                                                                        alignment=ft.Alignment.CENTER,
                                                                        border=ft.Border.all(2, ft.Colors.BLUE_600),
                                                                        bgcolor=ft.Colors.TRANSPARENT,
                                                                        content=ft.Text(nom_hero0, size=15,
                                                                                        font_family="Verdana")),

                                                                    # IMAGE GUERRIER
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://i.pinimg.com/originals/8d/6f/f3/8d6ff31f94e244db66e9e96bb87dfa70.gif")
                                                                    ) if type_hero0 == "GUERRIER" else ft.Container(),

                                                                    # IMAGE CHASSEUR
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://isaacostlund.io/wp-content/uploads/2018/08/Archer-F-gif.gif")
                                                                    ) if type_hero0 == "CHASSEUR" else ft.Container(),

                                                                    # IMAGE SUPPORT
                                                                    ft.Container(
                                                                        content=ft.Image(expand=True,
                                                                                         src="https://i.pinimg.com/originals/9c/6d/a8/9c6da87a758a7e919f54e564d9930bbe.gif")
                                                                    ) if type_hero0 == "SUPPORT" else ft.Container(),

                                                                    ft.Container(
                                                                        expand=2,
                                                                        alignment=ft.Alignment.CENTER,
                                                                        border=ft.Border.all(2, ft.Colors.BLUE_600),
                                                                        content=ft.Text(vie_hero0),
                                                                    )
                                                                ]),
                                                        ])
                                                    )),
                                                # Container d'espacement.
                                                ft.Container(expand=1, height=400),
                                                # +-+-+- Emplacement ennemi.
                                                ft.Container(
                                                    expand=4,
                                                    height=400,
                                                    border=ft.Border.all(2, ft.Colors.RED),
                                                    content=(
                                                        ft.Row(
                                                            controls=[
                                                                # Espace pour presentation de l'ennemi.
                                                                # +-+-+- Placement ennemi de la position un.
                                                                ft.Column(
                                                                    expand=1,
                                                                    height=400,
                                                                    controls=[
                                                                        ft.Container(
                                                                            expand=9,
                                                                            alignment=ft.Alignment.CENTER,
                                                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                                                            content=ft.Text(nom_ennemi0)
                                                                        ),

                                                                        # IMAGE VOLEUR
                                                                        ft.Container(
                                                                            content=ft.Image(expand=True,
                                                                                             src="https://img.itch.zone/aW1nLzMzMzY4OTguZ2lm/original/0Ut41Y.gif")
                                                                        )if type_ennemi0 == "VOLEUR" or "BRIGAND" else ft.Container(),

                                                                        # IMAGE CHASSEUR
                                                                        ft.Container(
                                                                            content=ft.Image(expand=True,
                                                                                             src="https://i.redd.it/cm1vywqqri021.gif")
                                                                        ) if type_ennemi0 == "CHASSEUR" else ft.Container(),

                                                                        ft.Container(
                                                                            expand=2,
                                                                            alignment=ft.Alignment.CENTER,
                                                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                                                            content=ft.Text(vie_ennemi0)
                                                                        )
                                                                    ]
                                                                ),
                                                                # +-+-+- Placement ennemi de la position deux.
                                                                ft.Column(
                                                                    expand=1,
                                                                    height=400,
                                                                    controls=[
                                                                        ft.Container(
                                                                            expand=9,
                                                                            height=400,
                                                                            alignment=ft.Alignment.CENTER,
                                                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                                                            content=ft.Text(nom_ennemi1)),

                                                                        # IMAGE VOLEUR
                                                                        ft.Container(
                                                                            content=ft.Image(expand=True,
                                                                                             src="https://img.itch.zone/aW1nLzMzMzY4OTguZ2lm/original/0Ut41Y.gif")
                                                                        ) if type_ennemi1 == "VOLEUR" or "BRIGAND" else ft.Container(),

                                                                        # IMAGE CHASSEUR
                                                                        ft.Container(
                                                                            content=ft.Image(expand=True,
                                                                                             src="https://i.redd.it/cm1vywqqri021.gif")
                                                                        ) if type_ennemi1 == "CHASSEUR" else ft.Container(),


                                                                        ft.Container(
                                                                            expand=2,
                                                                            alignment=ft.Alignment.CENTER,
                                                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                                                            content=ft.Text(vie_ennemi1))
                                                                    ]),
                                                                # +-+-+- Placement ennemi de la position trois.
                                                                ft.Column(
                                                                    expand=1,
                                                                    height=400,
                                                                    controls=[
                                                                        ft.Container(
                                                                            expand=9,
                                                                            height=400,
                                                                            alignment=ft.Alignment.CENTER,
                                                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                                                            content=ft.Text(nom_ennemi2)),

                                                                        # IMAGE VOLEUR
                                                                        ft.Container(
                                                                            content=ft.Image(expand=True,
                                                                                             src="https://img.itch.zone/aW1nLzMzMzY4OTguZ2lm/original/0Ut41Y.gif")
                                                                        ) if type_ennemi2 == "VOLEUR" or "BRIGAND" else ft.Container(),

                                                                        # IMAGE CHASSEUR
                                                                        ft.Container(
                                                                            content=ft.Image(expand=True,
                                                                                             src="https://i.redd.it/cm1vywqqri021.gif")
                                                                        ) if type_ennemi2 == "CHASSEUR" else ft.Container(),



                                                                        ft.Container(
                                                                            expand=2,
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
                                                                            height=400,
                                                                            alignment=ft.Alignment.CENTER,
                                                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                                                            content=ft.Text(nom_ennemi3)),

                                                                        # IMAGE VOLEUR
                                                                        ft.Container(
                                                                            content=ft.Image(expand=True,
                                                                                             src="https://img.itch.zone/aW1nLzMzMzY4OTguZ2lm/original/0Ut41Y.gif")
                                                                        ) if type_ennemi2 == "VOLEUR" or "BRIGAND" else ft.Container(),

                                                                        # IMAGE CHASSEUR
                                                                        ft.Container(
                                                                            content=ft.Image(expand=True,
                                                                                             src="https://i.redd.it/cm1vywqqri021.gif")
                                                                        ) if type_ennemi2 == "CHASSEUR" else ft.Container(),



                                                                        ft.Container(
                                                                            expand=2,
                                                                            alignment=ft.Alignment.CENTER,
                                                                            border=ft.Border.all(2, ft.Colors.RED_600),
                                                                            content=ft.Text(vie_ennemi3))
                                                                    ]),
                                                            ])
                                                    )),
                                                # Container d'espacement.
                                                ft.Container(expand=1, height=400),
                                            ])
                                        )),
                                    # +-+-+-+-+-+- Indicateur de tour +-+-+-+-+-+-.
                                    ft.Container(alignment=ft.Alignment.TOP_CENTER, content=(
                                        ft.Row(controls=[
                                            # Container pour balance.
                                            ft.Container(expand=5, height=150),
                                            ft.Container(
                                                expand=1,
                                                height=150,
                                                border=ft.Border.all(1, ft.Colors.GREEN),
                                                alignment=ft.Alignment.CENTER,
                                                content=ft.Text(tour_actuel, size=50)),
                                            # Container pour balance.
                                            ft.Container(expand=5, height=150)
                                        ])
                                    ))
                                ]),
                            ),
                            # +-+-+-+-+-+- Container du bas +-+-+-+-+-+-
                            ft.Container(
                                height=250,
                                expand=2,
                                padding=5,
                                border_radius=00,
                                bgcolor=ft.Colors.GREY_900,
                                content=(ft.Row(controls=[
                                    # Container d'espacement.
                                    ft.Container(expand=1, border=ft.Border.all(2, ft.Colors.BLACK)),
                                    # +-+-+- Container en bas à gauche
                                    ft.Container(
                                        expand=6,
                                        padding=10,
                                        border=ft.Border.all(2, ft.Colors.BLACK),
                                        border_radius=0,
                                        bgcolor=ft.Colors.GREY_900,
                                        content=ft.Column(controls=[
                                            # +-+-+- Boutons d'actions
                                            ft.Row(expand=3, controls=[
                                                ft.Container(
                                                    expand=1,
                                                    alignment=ft.Alignment.CENTER,
                                                    border=ft.Border.all(2, ft.Colors.BLACK),
                                                    content=ft.ElevatedButton("Attaque", on_click=None)),
                                                ft.Container(
                                                    expand=1,
                                                    alignment=ft.Alignment.CENTER,
                                                    border=ft.Border.all(2, ft.Colors.BLACK),
                                                    content=ft.Text("Abilité 1")),
                                                ft.Container(
                                                    expand=1,
                                                    alignment=ft.Alignment.CENTER,
                                                    border=ft.Border.all(2, ft.Colors.BLACK),
                                                    content=ft.Text("Abilité 2")),
                                                ft.Container(
                                                    expand=1,
                                                    alignment=ft.Alignment.CENTER,
                                                    border=ft.Border.all(2, ft.Colors.BLACK),
                                                    content=ft.Text("Abilité 3")),
                                                ft.Container(
                                                    expand=1,
                                                    alignment=ft.Alignment.CENTER,
                                                    border=ft.Border.all(2, ft.Colors.BLACK),
                                                    content=ft.Text("Abilité 4")),
                                                ft.Container(
                                                    expand=1,
                                                    alignment=ft.Alignment.CENTER,
                                                    border=ft.Border.all(2, ft.Colors.BLACK),
                                                    content=ft.ElevatedButton("Passer", on_click=None),
                                                    on_click=None)
                                            ]),
                                            ft.Row(expand=4, controls=[
                                                ft.Container(
                                                    expand=True,
                                                    alignment=ft.Alignment.TOP_LEFT,
                                                    border=ft.Border.all(2, ft.Colors.BLACK),
                                                    border_radius=00,
                                                    bgcolor=ft.Colors.GREY_900,
                                                    content=ft.Text("Description d'abilité"
                                                                    "\nLes attaques: "))
                                            ]),
                                        ])),
                                    # +-+-+- Container en bas à droite.
                                    ft.Container(
                                        expand=2,
                                        alignment=ft.Alignment.TOP_CENTER,
                                        border=ft.Border.all(2, ft.Colors.BLACK),
                                        border_radius=00,
                                        bgcolor=ft.Colors.GREY_900,
                                        content=ft.Row(controls=[
                                            ft.Text("tour_personnage")
                                        ])),
                                    # Container d'espacement.
                                    ft.Container(expand=1, border=ft.Border.all(2, ft.Colors.BLACK)),
                                ])
                                ))
                        ])))
                ],
                        )
            )
        page.update()


    async def view_pop(e):
        if e.view is not None:
            print("View pop:", e.view)
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = menu_principal
    page.on_view_pop = view_pop

    menu_principal()


if __name__ == "__main__":
    ft.run(main)