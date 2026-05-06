
# Fichier de Luke Immanuel Legaspina.
# -------------------- Importation --------------------
from random import randrange
from .Personnage import Personnage, lire_stats_json
import json

# -------------------- Class Hero --------------------
class Hero(Personnage):
    """ Hero est une classe enfant de Personnage.
    Attributes:
        nom (str) : Le nom de l'hero
        type (str) : Le type de l'hero
        stats (dict) : Les stats de l'hero """

    def __init__(self, nom: str, type: str):
        super().__init__(nom, type)
        self.nom = nom
        self.type = type
        self.stats = {
            "degat_melee": 0,
            "degat_distance": 0,
            "point_vie_max": 0,
            "point_vie": 0,
            "point_agilite": 0,
            "point_chance": 0
        }
        self.stats_ajouter = None

    # -------------------- Méthodes class --------------------
    # La class hero contient ses propres fonctions uniques à elle.

    def attribuer_hero(self):
        """Sous fonction dans attribuer_stat_hero(). Le joueur
        n'y a pas accès. Stats pour hero sans spécialisation."""
        if self.type == "HERO":
            point_vie_max = randrange(20, 30, 2)
            self.stats = {
                # 'randrange' est identique que 'randint' avec
                # la possibilité de mettre des sauts.
                "degat_melee": randrange(2,6,2),
                "degat_distance": randrange(2,6,2),
                "point_vie_max": point_vie_max,
                "point_vie": point_vie_max,
                "point_agilite": randrange(2,4,2),
                "point_chance": randrange(0,10,2),
            }

    def ecrire_stats_hero(self, chemin_fichier: str, dict_heros: dict):
        """Fonction qui enregistre les stats du personnage dans un
         fichier .json. Utiliser uniquement par la classe Hero."""
        contenu_json = lire_stats_json(chemin_fichier)
        stats_hero = {self.nom: {self.stats_ajouter: self.stats}}
        heros_dans_dict = 0
        for hero_present, ___ in dict_heros.items():
            if hero_present: heros_dans_dict += 1
        if heros_dans_dict < 4:
            # Ajoute 'stats_hero' dans le 'chemin_fichier'.
            contenu_json.update(stats_hero)
            with open(chemin_fichier, mode="w", encoding="utf-8") as fichier:
                json.dump(contenu_json, fichier, indent=4, ensure_ascii=False)
        else: raise ValueError("La limite de héros à été atteint. (4/4)")

    def supprimer_stats_hero(self, chemin_fichier: str, dict_heros: dict, nom):
        """Fonction qui enlève les stats du personnage dans un
         fichier .json. Utiliser uniquement par la classe Hero."""
        contenu_json = lire_stats_json(chemin_fichier)
        del dict_heros[nom]
        contenu_json.update()
        with open(chemin_fichier, mode="w", encoding="utf-8") as fichier:
            json.dump(contenu_json, fichier, indent=4, ensure_ascii=False)

    # Désactiver temporairement.
    def __str__(self):
        return (
            f"{self.nom}| {self.stats_ajouter}| PV:{self.stats['point_vie']}/{self.stats['point_vie_max']}| "
            f"Degat Melee:{self.stats['degat_melee']}| Degat Distance:{self.stats['degat_distance']}| "
            f"Agilité:{self.stats['point_agilite']}| Chance:{self.stats['point_chance']}")