
# Fichier de Vann Sovannthanant.
# -------------------- Importation --------------------
from pathlib import Path
import pytest
from Partie import Personnage,Hero, lire_stats_json
from Partie.Exceptions import NomError, TypePersoError

dict_type_hero = lire_stats_json("Partie/Fichiers/Type_Hero.json")
# -------------------- Tests de Personnage --------------------
@pytest.mark.parametrize("nom_type, degat_melee, degat_distance, "
                         "point_vie_max,point_agilite, point_chance",[
     ("GUERRIER", 2,-2, 8, 2, 0),
     ("CHASSEUR",-2, 2, 6, 2, 0),
     ("SUPPORT" , 0, 0, 4, 2, 0),
     ("GUARDE"  , 0,-2,12,-2, 0),
     (None, 0, 0, 0, 0, 0)
])
def test_personnage_attribuer_stat(nom_type, degat_melee, degat_distance,
                                   point_vie_max, point_agilite, point_chance):
     test_personnage = Personnage("Nom","HERO")
     test_personnage.attribuer_stat(nom_type, dict_type_hero)
     assert test_personnage.stats["degat_melee"] == degat_melee
     assert test_personnage.stats["degat_distance"] == degat_distance
     assert test_personnage.stats["point_vie_max"] == point_vie_max
     assert test_personnage.stats["point_vie"] == point_vie_max
     assert test_personnage.stats["point_agilite"] == point_agilite
     assert test_personnage.stats["point_chance"] == point_chance


@pytest.mark.parametrize("stats_attribuer",["GUERRIER",None])
def test__str__personnage(stats_attribuer):
     """ S'il y'a un stat_attribuer, afficher dans le __str__(). """
     test_personnage = Personnage("Nom", "HERO")
     test_personnage.attribuer_stat(stats_attribuer, dict_type_hero)
     if stats_attribuer is str:
          assert test_personnage.__str__() == (f"{test_personnage.nom}|{test_personnage.type}|"
          f"{test_personnage.stats_ajouter}|{test_personnage.stats}")
     if stats_attribuer is None:
          assert test_personnage.__str__() == (f"{test_personnage.nom}|{test_personnage.type}|"
          f"{test_personnage.stats}")


# -------------------- Tests de Hero --------------------
# Le prof a dit que pour les fonctions ayant plusieurs random, il est
# impossible de faire des monkey patch.
def test_attribuer_hero():
     test_hero = Hero("Nom","HERO")
     test_hero.attribuer_hero()
     assert 2 <= test_hero.stats["degat_melee"] <= 6
     assert 2 <= test_hero.stats["degat_distance"] <= 6
     assert 20 <= test_hero.stats["point_vie_max"] <= 30
     assert 20 <= test_hero.stats["point_vie"] <= 30
     assert 2 <= test_hero.stats["point_agilite"] <= 4
     assert 0 <= test_hero.stats["point_chance"] <= 10


def test__str__hero():
     test_hero = Hero("Nom", "HERO")
     test_hero.attribuer_hero()
     assert test_hero.__str__() == (f"{test_hero.nom}| {test_hero.stats_ajouter}| "
     f"PV:{test_hero.stats['point_vie']}/{test_hero.stats['point_vie_max']}| "
     f"Degat Melee:{test_hero.stats['degat_melee']}| Degat Distance:{test_hero.stats['degat_distance']}| "
     f"Agilité:{test_hero.stats['point_agilite']}| Chance:{test_hero.stats['point_chance']}")