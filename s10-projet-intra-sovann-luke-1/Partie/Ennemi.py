
# Fichier de Vann Sovannthanant.
# -------------------- Importation --------------------
from .Personnage import Personnage

# -------------------- Class Ennemi --------------------
class Ennemi(Personnage):
    def __init__(self, nom:str|None, type:str):
        """Propriétés(4/3) de la classe Ennemi. (Propriétés)
        Ennemi est une classe Enfant de la classe Personnage."""
        super().__init__(nom, type)
        self.stats = {
            "degat_melee": 0,
            "degat_distance": 0,
            "point_vie_max": 0,
            "point_vie": 0,
            "point_agilite": 0,
            "point_chance": 0
        }
        # cette propriété pour les type: "BANDIT", "BRIGAND".
        self.stats_ajouter = None

    # -------------------- Méthode de class --------------------
    # Touts est déjà fait dans la class parent 'Personnage'. yessir

    def __str__(self):
        return (
            f"{self.stats_ajouter}| PV:{self.stats['point_vie']}/{self.stats['point_vie_max']}| "
            f"Degat Melee:{self.stats['degat_melee']}| Degat Distance:{self.stats['degat_distance']}| "
            f"Agilité:{self.stats['point_agilite']}| Chance:{self.stats['point_chance']}")