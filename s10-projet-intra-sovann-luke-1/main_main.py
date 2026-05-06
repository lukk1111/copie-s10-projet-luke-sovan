from os import access
# Fichier principal, utiliser par Vann Sovannthanant et Luke Immanuel Legaspina.
# -------------------- Importation --------------------
from pathlib import Path
from Partie import *
from textwrap import dedent
import random

if __name__ == "__main__":
    # Code du prof pour réparer le problème d'importation.
    dossier_parent = Path(__file__).parent

    # -------------------- main principal du jeu --------------------
    dict_ennemi = lire_stats_json("Partie/Fichiers/Type_ennemi.json")
    dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
    dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
    chem_heros = "Partie/Fichiers/Type_Hero.json"
    # -------------------- dict pour Combat
    dict_scene = lire_stats_json("Partie/Fichiers/Dictionnaire_scenario.json")
    # -------------------- dict pour Action
    dict_abilite = lire_stats_json("Partie/Fichiers/Abilite_Hero.json")

    # Menu du jeu
    print("--Darkest Dungeon--\n"
          "1. Jouer / Continuer\n"
          "2. Créer personnages\n"
          "3. Quitter")

    choix_input = input("Choisir une option: ")
    match choix_input:
        case "1": choix_menu = "Jouer"
        case "2": choix_menu = "Créer des personnages"
        case "3": choix_menu = "Quitter"
        case _: raise ValueError("Entrez les options disponibles.")

    # TODO Jouer le jeu -----------------------------------------
    if choix_menu == "Jouer":
        if 0 < len(dict_heros) <= 4:   # 1 hero minimum, 4 heros maximum.
            print(f"{"\n"*50}--- PRÉPARATION DU COMBAT ---")
            combat = Combat([], [], "FORET")

            # -------------------- INITIALISATION --------------------
            combat.inserer_heros(dict_heros, dict_type_hero)
            combat.generer_ennemis(dict_scene, dict_ennemi)
            print("\n--- PLACEMENTS INITIAUX ---")
            print("Héros 🏰👨‍👦‍👦 :")
            for hero in combat.placement_hero: print("-", hero)
            print("\nEnnemis 😡 :")
            for ennemi in combat.placement_ennemi: print("-", ennemi)

            # -------------------- BOUCLE DE COMBAT --------------------
            tour = 1
            resultat = "Continue"
            while resultat == "Continue":
                print(f"\n================ TOUR {tour} ================")
                ordre_personnage = combat.evaluation_agilite_personnage()
                for personnage in ordre_personnage: # [8 personnes]
                    etat = combat.verifier_equipe_vivante(dict_heros)
                    if etat == "0 heros vivants":
                        resultat = "Defeat"
                        break
                    elif etat == "0 ennemis vivants":
                        resultat = "Victoire"
                        break

                    if personnage.type == "HERO":
                        print(f"\nTour de : {personnage.nom}")

                        # ---------- AFFICHAGE ACTIONS DISPONIBLES ----------
                        print("--- ACTIONS DISPONIBLES ---")
                        type_perso = personnage.stats_ajouter
                        if type_perso in dict_abilite:
                            actions_type = dict_abilite[type_perso]
                            for type_action, actions in actions_type.items():
                                print(f"\n⚔ {type_action}")
                                for nom_action, effet in actions.items():
                                    print(f"  ➜ {nom_action} ({effet})")
                        else: print("Aucune action disponible")

                        # ---------- INPUT ACTION ----------
                        while True:
                            action_input = input("Action : ").upper()
                            action_input = action_input.replace(" ","_")
                            action_valide = False
                            actions_type = dict_abilite[type_perso]
                            for type_action, actions in actions_type.items():
                                if not action_valide:
                                    for nom_action, effet in actions.items():
                                        if action_input == nom_action:
                                            action_valide = True
                                            break
                                        else: action_valide = False
                                else: break
                            if action_valide: break
                            else: print("Action Invalide")

                        # ---------- AFFICHER CIBLES ----------
                        cibles_possibles = []
                        # ACTION GUÉRISON (support → héros)
                        if (action_input in actions_type["ACTION_GUERIR"] or
                            action_input in actions_type["ACTION_DEPLACER"]):
                            print("\n--- CIBLES (HÉROS) ---")
                            cibles_possibles = combat.placement_hero
                        if action_input in actions_type["ACTION_ATTAQUE"]:
                            print("\n--- CIBLES (ENNEMIS) ---")
                            for type_action, actions in actions_type.items():
                                for nom_action, effet in actions.items():
                                    if action_input == nom_action:
                                        for index in effet["cible_possible"]:
                                            cibles_possibles.append(combat.placement_ennemi[index])
                        if action_input in actions_type["ACTION_BLOQUER"]:
                            cibles_possibles = combat.placement_ennemi

                        # Afficher index proprement
                        for i, c in enumerate(cibles_possibles): print(f"{i} - {c}")

                        # ---------- CHOIX CIBLE INDEX ----------
                        if action_input in actions_type["ACTION_PASSER"]: pass
                        else:
                            while True:
                                cible_index = int(input("Choisir index cible : "))
                                if 0 <= cible_index < len(cibles_possibles):
                                    cible = cibles_possibles[cible_index]
                                    break
                                else: print("Cible invalide")

                        # ---------- EXECUTION ACTION POUR LES HÉROS ----------
                        try:
                            action = Action(personnage, action_input, cible)
                            action.verification_type_actions(dict_abilite, combat)
                        except Exception as e:
                            print(f"Erreur action: {e}")
                            continue

                    elif personnage.type == "ENNEMI":
                        print(f"\nTour de : {personnage.stats_ajouter}")
                        # ---------- ACTION POUR LES ENNEMIS ----------
                        ennemis_vivants = [e for e in combat.placement_ennemi if e.stats["point_vie"] > 0]

                        if ennemis_vivants:
                            ennemi = random.choice(ennemis_vivants)
                            cibles_hero = [h for h in combat.placement_hero if h.stats["point_vie"] > 0]

                            if cibles_hero:
                                cible_hero = random.choice(cibles_hero)

                                print(f"👹 {ennemi.stats_ajouter} attaque {cible_hero.nom}")

                                # attaque simple
                                cible_hero.stats["point_vie"] -= ennemi.stats["degat_melee"]

                                if cible_hero.stats["point_vie"] < 0:
                                    cible_hero.stats["point_vie"] = 0

                                print(f"{cible_hero.nom} PV: {cible_hero.stats['point_vie']}")

                tour += 1 # Fin du tour

            # -------------------- RESULTAT FINAL --------------------
            print("\n================ FIN DU COMBAT ================")
            print(f"Résultat : {resultat}")
        else: raise ValueError("Vous devez avoir au moins 1 héro pour jouer !")






    # Créer des personnages (Heros) ------------------------
    elif choix_menu == "Créer des personnages":
        print("")
        choix_creation_hero = input("1.\tEntrer pour créer des héros.\n2.\tSupprimer des héros existants.\t\n3.\tVoir les héros.\n"
                           "Choisir une option: ")
        match choix_creation_hero:
            case "1":
                choix_creation_hero = "Entrer pour créer des héros"
            case "2":
                choix_creation_hero = "Supprimer des héros existants"
            case "3":
                choix_creation_hero = "Voir les héros"
            case _:
                raise ValueError("Entrez les options disponibles.")


        if choix_creation_hero == "Entrer pour créer des héros":
            print("")
            if len(dict_heros) >= 4:
                print("La limite est atteinte.")
            else:
                choix_type = input("1.\tHERO\n2.\tENNEMI\n3.\tOBSTACLE\n"
                                   "Choisissez le type de personnage: ")
                match choix_type:
                    case "1":
                        choix_type = "HERO"
                    case "2":
                        choix_type = "ENNEMI"
                    case "3":
                        choix_type = "OBSTACLE"
                    case _:
                        raise ValueError("Entrez les options disponibles.")

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
                        print(f"{index + 1}. {type_hero}")
                    # Si le 'type_choisie' est équivalent à 'index', attribuer le 'type_hero'.
                    type_choisie = int(input(f"Quelle classe est l'héro {nom_hero}:\n{25 * "-"}"))
                    for index, type_hero in enumerate(les_types_hero):
                        if type_choisie == index + 1: hero.attribuer_stat(type_hero, dict_type_hero)
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
                        print(f"{index + 1}. {type_ennemi}")
                    # Si le 'type_choisie' est équivalent à 'index', attribuer le 'type_ennemi'.
                    type_choisie = int(input(f"Quelle classe est l'ennemi:\n{25 * "-"}"))
                    for index, type_ennemi in enumerate(les_types_ennemi):
                        if type_choisie == index + 1: ennemi.attribuer_stat(type_ennemi, dict_ennemi)
                    # Fonction d'affichage.
                    ennemi.afficher_informations()

                elif choix_type == "OBSTACLE":
                    print("On a pas encore faire des stats pour\n"
                          f"les personnages obstacle.\n{25 * "-"}")


        elif choix_creation_hero == "Supprimer des héros existants":
            print("")
            for cle, valeur in dict_heros.items():
                print(cle, valeur)
                print("")
            choix_hero_retirer = input("Choisissez un héro à retirer: ").upper()
            if choix_hero_retirer in dict_heros:
                dict_heros.pop(choix_hero_retirer, None)
                print(f"{choix_hero_retirer} a été supprimé")
            else:
                print("L'héro n'existe pas.")


        elif choix_creation_hero == "Voir les héros":
            print("Voici les héros existants :")
            for cle, valeur in dict_heros.items():
                print(cle, valeur)






    # Quitter --------------------
    elif choix_menu == "Quitter":
        print("Au revoir !")


    # ---------- Combat. ----------
    for i in range (1,5): pass

    # ---------- Action. ----------
