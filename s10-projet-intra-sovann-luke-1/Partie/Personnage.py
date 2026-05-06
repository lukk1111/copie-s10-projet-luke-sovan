
# Fichier de Vann Sovannthanant.
# -------------------- Importation --------------------
from random import randint, randrange
from .Exceptions import NomError,TypePersoError
import json

# -------------------- Class Personnage --------------------
class Personnage:
    def __init__(self, nom: str|None, type: str):
        """Propriétés(4/3) de la classe Personnage.(Propriétés)
        J'ai décidé de garder les stats vide pour éviter des
        complications."""
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
        # cette propriété pour les types : "GUERRIER", "CHASSEUR".
        self.stats_ajouter = None

    # --------------- Accesseurs et Mutateurs ---------------
    @property   # Lecture et Écriture pour 'nom'.
    def nom(self): return self._nom
    @nom.setter # Le nom ne doit pas être changé. (privé=_.)
    def nom(self, nouveau_nom: str|None):
        if isinstance(nouveau_nom, str|None):
            self._nom = nouveau_nom
        else: raise NomError("Le nom doit être une chaine "
                               "de caractère ou est vide.")

    @property  # Lecture et Écriture pour 'type'.
    def type(self): return self._type
    @type.setter# Le type ne doit pas être changé. (privé=_.)
    def type(self, nouveau_type: str):
        if isinstance(nouveau_type, str):
            nouveau_type = nouveau_type.upper()
            if nouveau_type in ["HERO", "ENNEMI"]:
                self._type = nouveau_type
            else: raise TypePersoError("Le type doit être: HERO, ENNEMI.")
        else: raise TypePersoError("Le type doit être un string.")


    # -------------------- Méthodes class --------------------
    def attribuer_stat(self, nom_type: str, dict_stats_ajouter: dict):
        """ Fonction qui attribuer les stats de 'dict_stats_ajouter'
        dans les stats de 'self.stats'. Compatible avec HERO et ENNEMI."""
        for nom_stat, stat_valeur in dict_stats_ajouter.items():
            if nom_type == nom_stat:
                stats_ajouter = dict_stats_ajouter[nom_type]
                self.stats["degat_melee"] += stats_ajouter["degat_melee"]
                self.stats["degat_distance"] += stats_ajouter["degat_distance"]
                self.stats["point_vie_max"] += stats_ajouter["point_vie_max"]
                self.stats["point_vie"] += stats_ajouter["point_vie_max"]
                self.stats["point_agilite"] += stats_ajouter["point_agilite"]
                self.stats["point_chance"] += stats_ajouter["point_chance"]
                self.stats_ajouter = nom_type

    def afficher_informations(self):
        """ Fonction qui affiche les stats du personnage dans la console.
        Compatible avec HERO et ENNEMI."""
        if self.nom: print(f"nom: {self.nom}")
        print(f"Personnage de type: {self.type}")
        print(f"type: {self.stats_ajouter}")
        for stat,point in self.stats.items():
           print(f"{stat}\t: {point}")
        print(25*"-")

    def __str__(self):
        """ Un message spécifique est affiché dans la console lors de 'print'."""
        if self.stats_ajouter:
            return f"{self.nom}|{self.type}|{self.stats_ajouter}|{self.stats}"
        else: return f"{self.nom}|{self.type}|{self.stats}"

    # -------------------- Fermeture de la class --------------------

def lire_stats_json(chemin_fichier: str):
    """Fonction servant à lire des fichiers de type.json. C'est une
    fonction statique, donc peut-être utiliser partout."""
    with open(chemin_fichier, mode="r", encoding="utf-8") as fichier:
        return json.load(fichier)