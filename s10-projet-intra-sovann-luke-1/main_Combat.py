
# Fichier main, utiliser par Sovannthanant et Luke Immanuel Legaspina.
# -------------------- Importation --------------------
from pathlib import Path
from Partie import lire_stats_json, Combat

if __name__ == "__main__":
    # Code du prof pour réparer le problème d'importation.
    dossier_parent = Path(__file__).parent

    # ---------- main de Combat ----------
    dict_ennemi = lire_stats_json("Partie/Fichiers/Type_ennemi.json")
    dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
    dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
    dict_scene = lire_stats_json("Partie/Fichiers/Dictionnaire_scenario.json")


    combat = Combat([], [], "FORET")

    combat.inserer_heros(dict_heros, dict_type_hero)
    combat.generer_ennemis(dict_scene, dict_ennemi)
    combat.verifier_equipe_vivante(dict_heros)

    print("Placements")
    print(combat.placement_hero)
    print(combat.placement_ennemi)
    ordre = combat.evaluation_agilite_personnage()

    print("Ordre")
    print(ordre)
