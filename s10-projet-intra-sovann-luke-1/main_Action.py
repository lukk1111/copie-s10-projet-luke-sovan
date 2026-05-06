
# Fichier main, utiliser par Sovannthanant et Luke Immanuel Legaspina.
# -------------------- Importation --------------------
from pathlib import Path
from Partie import Hero, Ennemi, Combat, Action, lire_stats_json

if __name__ == "__main__":
    # Code du prof pour réparer le problème d'importation.
    dossier_parent = Path(__file__).parent

    # ---------- main de Action ----------
    dict_abilite = lire_stats_json("Partie/Fichiers/Abilite_Hero.json")
    dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
    dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
    dict_ennemi = lire_stats_json("Partie/Fichiers/Type_ennemi.json")

    combat = Combat([], [], "FORET")
    combat.inserer_heros(dict_heros, dict_type_hero)
    ennemi = Ennemi(None, "ENNEMI")
    ennemi.attribuer_stat("VOLEUR",dict_ennemi)
    ennemi2 = Ennemi(None, "ENNEMI")
    ennemi2.attribuer_stat("BANDIT", dict_ennemi)

    # Voir 'Dictionnaire_hero.json', HENRY est à la position 0.
    action = Action(combat.placement_hero[0],"LAME_TRANCHER",ennemi)
    action.raccourci_dict_abilite(dict_abilite)
    action.verification_type_actions(dict_abilite,combat)

