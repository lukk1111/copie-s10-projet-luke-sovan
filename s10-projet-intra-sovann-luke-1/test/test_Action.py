
# Fichier de Luke Immanuel Legaspina
# -------------------- Importation --------------------
import pytest
from pathlib import Path
from Partie import Action, Combat, Hero, Ennemi, lire_stats_json

dict_ennemi = lire_stats_json("Partie/Fichiers/Type_ennemi.json")
dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
dict_scene = lire_stats_json("Partie/Fichiers/Dictionnaire_scenario.json")
dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
chem_heros = "Partie/Fichiers/Type_Hero.json"

# ------- Mes tests ---------

def test_action_attaque_melee():
    """ Test ou un hero (HENRY) attaque un ennemi (LOUP). """
    # Arrange
    hero = Hero("HENRY", "HERO")
    hero.attribuer_stat("GUERRIER", dict_type_hero)
    ennemi = Ennemi(None, "ENNEMI")
    ennemi.attribuer_stat("LOUP", dict_ennemi)
    action = Action(hero, "LAME_TRANCHER", ennemi)

    pv_initial = ennemi.stats["point_vie"]
    test_dict_abilite = {"GUERRIER": {
            "ACTION_ATTAQUE": {
                "LAME_TRANCHER": {"type_degat": "degat_melee"}}
        }}
    # Act
    action.action_attaque(test_dict_abilite["GUERRIER"]["ACTION_ATTAQUE"])

    # Assert
    assert ennemi.stats["point_vie"] == pv_initial - hero.stats["degat_melee"]


def test_deplacement_avant():
    """ Test ou un hero (HENRY) change de position avec un autre hero (CHERNOV). """
    # Arrange
    hero = Hero("HENRY", "HERO")
    hero.attribuer_stat("GUERRIER", dict_type_hero)
    hero1 = Hero("CHERNOV", "HERO")
    hero1.attribuer_stat("CHASSEUR", dict_type_hero)
    combat = Combat([],[],"FORET")
    combat.placement_hero = [hero,hero1]

    test_dict_abilite = {"GUERRIER": {
            "ACTION_DEPLACER": {
                "DEPLACER_AVANT": {"changer_index": 1}}
        }}

    # Act
    action = Action(hero, "DEPLACER_AVANT", hero1)
    action.verification_type_actions(test_dict_abilite, combat)

    # Assert

    assert combat.placement_hero[0] == hero1


def test_action_guerir_augmente_pv():
    # Arrange
    hero = Hero("ELOISE", "HERO")
    hero.attribuer_stat("SUPPORT", dict_type_hero)
    cible = Hero("HENRY", "HERO")
    hero.attribuer_stat("GUERRIER", dict_type_hero)

    cible.stats["point_vie_max"] = 20
    cible.stats["point_vie"] = 10
    action = Action(hero, "EAU_DIVINE", cible)

    test_dict_abilite = {"SUPPORT": {
            "ACTION_GUERIR": {
                "EAU_DIVINE": {"point_guerison": 3}}
        }}

    # Act
    action.action_guerir(test_dict_abilite["SUPPORT"]["ACTION_GUERIR"])

    # Assert
    assert cible.stats["point_vie"] == 13
