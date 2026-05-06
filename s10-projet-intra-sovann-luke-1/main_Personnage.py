
# Fichier main, utiliser par Sovannthanant et Luke Immanuel Legaspina.
# -------------------- Importation --------------------
from pathlib import Path
from Partie import (lire_stats_json, Hero, Ennemi)

if __name__ == "__main__":


    # Code du prof pour réparer le problème d'importation.
    dossier_parent = Path(__file__).parent

    # ---------- main de Personnage,Hero,Ennemi ----------
    dict_ennemi = lire_stats_json("Partie/Fichiers/Type_ennemi.json")
    dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
    dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
    chem_heros = "Partie/Fichiers/Dictionnaire_hero.json"

    # Test de création d'un personnage.
    choix_type = input("1.\tHERO\n2.\tENNEMI\n3.\tOBSTACLE\n"
                       "Choisissez le type de personnage: ")
    match choix_type:
        case "1": choix_type = "HERO"
        case "2": choix_type = "ENNEMI"
        case "3": choix_type = "OBSTACLE"
        case _: raise ValueError("Entrez les options disponibles.")

    if choix_type == "HERO":
        nom_hero = input(f"Quelle est le nom de l'{choix_type}: ")
        hero = Hero(nom_hero.upper(), choix_type)
        hero.attribuer_hero()
        hero.afficher_informations()
        # Fonction 'enumerate' affiche les types héros avec leurs index.
        les_types_hero = []
        for type_hero, ___ in dict_type_hero.items():
            les_types_hero.append(type_hero)
        for index, type_hero in enumerate(les_types_hero):
            print(f"{index+1}. {type_hero}")
        # Si le 'type_choisie' est équivalent à 'index', attribuer le 'type_hero'.
        type_choisie = int(input(f"Quelle classe est l'héro {nom_hero}:\n{25*"-"}"))
        for index, type_hero in enumerate(les_types_hero):
            if type_choisie == index + 1: hero.attribuer_stat(type_hero,dict_type_hero)
        # Fonction d'affichage et de sauvegarde.
        hero.afficher_informations()
        hero.ecrire_stats_hero(chem_heros, dict_heros)

    elif choix_type == "ENNEMI":
        ennemi = Ennemi(None, choix_type)
        ennemi.afficher_informations()
        # Fonction 'enumerate affiche les types ennemis avec leurs index.
        les_types_ennemi = []
        for type_ennemi, ___ in dict_ennemi.items():
            les_types_ennemi.append(type_ennemi)
        for index, type_ennemi in enumerate(les_types_ennemi):
            print(f"{index+1}. {type_ennemi}")
        # Si le 'type_choisie' est équivalent à 'index', attribuer le 'type_ennemi'.
        type_choisie = int(input(f"Quelle classe est l'ennemi:\n{25 * "-"}"))
        for index, type_ennemi in enumerate(les_types_ennemi):
            if type_choisie == index+1: ennemi.attribuer_stat(type_ennemi, dict_ennemi)
        #Fonction d'affichage.
        ennemi.afficher_informations()

    elif choix_type == "OBSTACLE":
        print("On a pas encore faire des stats pour\n"
              f"les personnages obstacle.\n{25*"-"}")
