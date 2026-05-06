
# Fichier de Luke Immanuel Legaspina et Vann Sovannthanant.
# -------------------- Importation --------------------
from pathlib import Path
import random
import pytest
from Partie import Hero, Ennemi,Combat, lire_stats_json
from Partie.Exceptions import NomError, TypePersoError

dict_ennemi = lire_stats_json("Partie/Fichiers/Type_ennemi.json")
dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
dict_scene = lire_stats_json("Partie/Fichiers/Dictionnaire_scenario.json")
dict_heros = lire_stats_json("Partie/Fichiers/Dictionnaire_hero.json")
dict_abilite = lire_stats_json("Partie/Fichiers/Abilite_Hero.json")
chem_heros = "Partie/Fichiers/Type_Hero.json"

# -------------------- Tests de Combat --------------------
@pytest.mark.parametrize("placement_hero, placement_ennemi, biome,",[
    ([Hero],[],"FORET"),
    ([],[Ennemi],"VILLAGE"),
    ([],[],"PLAINE")])   # Celui-ci devrait échouer avec l'exception'.NomError'.
def test_creation_class(placement_hero, placement_ennemi, biome):
    combat = Combat(placement_hero, placement_ennemi, biome)
    if combat.inserer_heros(dict_heros, dict_type_hero):
        assert combat.inserer_heros(dict_ennemi, dict_type_hero)



def test_generer_ennemis(monkeypatch):
    """ Ca fonctionne de temps en temps. """
    # Arrange
    combat = Combat([],[],"FORET")
    # Act, Je veux obtenir le scenario 0 de 'Dictionnaire_scenario' dans 'placement_ennemi'.
    monkeypatch.setattr("random.randint" , lambda: 0)
    combat.generer_ennemis(dict_scene, dict_ennemi)
    nom_objet_ennemis = []
    for ennemi in combat.placement_ennemi: nom_objet_ennemis.append(ennemi.stats_ajouter)
    # Assert
    assert nom_objet_ennemis == ["VOLEUR","VOLEUR","VOLEUR","VOLEUR"]



@pytest.mark.parametrize("equipe_morte, resultat_attendu",[
    ("HERO","0 heros vivants"),
    ("ENNEMI","0 ennemis vivants")])
def test_verifier_equipe_vivante(equipe_morte, resultat_attendu):
    combat = Combat([],[], "FORET")
    combat.inserer_heros(dict_heros, dict_type_hero)
    combat.generer_ennemis(dict_scene, dict_ennemi)
    if equipe_morte == "HERO":
        for hero in combat.placement_hero: hero.stats["point_vie"] = 0
        for ennemi in combat.placement_ennemi: ennemi.stats["point_vie"] = 10
    if equipe_morte == "ENNEMI":
        for ennemi in combat.placement_ennemi: ennemi.stats["point_vie"] = 0
        for hero in combat.placement_hero: hero.stats["point_vie"] = 10
    assert combat.verifier_equipe_vivante(dict_heros) == resultat_attendu



def test_evaluation_agilite_personnage():
    """ Le plus rapide (point_agilite haute), joue en premier. """
    hero0 = Hero("test1", "HERO")
    hero0.stats["point_agilite"] = 1
    hero1 = Hero("test1", "HERO")
    hero1.stats["point_agilite"] = 2
    hero2 = Hero("test2", "HERO")
    hero2.stats["point_agilite"] = 3
    hero3 = Hero("test3", "HERO")
    hero3.stats["point_agilite"] = 4
    combat = Combat([hero0,hero1,hero2,hero3],[],"FORET")
    resultat_obtenu = combat.evaluation_agilite_personnage()
    resultat_attendu = [hero3, hero2, hero1, hero0]
    assert resultat_obtenu == resultat_attendu
