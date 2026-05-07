
# Fichier de Luke Immanuel Legaspina et de Vann Sovannthanant.
# -------------------- Importation --------------------
from Partie import Personnage, Ennemi, Hero, Action
from random import randint
from .Exceptions import NomError


# -------------------- Class Combat --------------------
class Combat:
    def __init__(self, placement_hero:list[Hero],
                 placement_ennemi:list[Ennemi], biome):
        """Propriétés(4/3) de la classe Combat. (Propriétés)
        Le placement affecte les attaques et leurs effets."""
        self.placement_hero = placement_hero
        self.placement_ennemi = placement_ennemi
        self.biome = biome
        self.combat_final = False

    # --------------- Accesseurs et Mutateurs ---------------
    @property               # Lecture et Écriture pour 'placement_hero'.
    def placement_hero(self): return self._placement_hero
    @placement_hero.setter  # 'placement_hero' ne doit pas changé.
    def placement_hero(self, nouveau_placement_hero: list):
        if isinstance(nouveau_placement_hero, list):
            self._placement_hero = nouveau_placement_hero
        else: raise ValueError("placement_hero doit être une liste vide.")

    @property               # Lecture et Écriture pour 'placement_ennemi'.
    def placement_ennemi(self): return self._placement_ennemi
    @placement_ennemi.setter# 'placement_ennemi' ne doit pas changer.
    def placement_ennemi(self, nouveau_placement_ennemi: list):
        if isinstance(nouveau_placement_ennemi, list):
            self._placement_ennemi = nouveau_placement_ennemi
        else: raise ValueError("placement_hero doit être une liste vide.")

    @property       # Lecture et Écriture pour 'biome'.
    def biome(self): return self._biome
    @biome.setter   # 'biome' ne doit pas changer.
    def biome(self, nouveau_biome: str):
        if isinstance(nouveau_biome, str):
            nouveau_biome = nouveau_biome.upper()
            if nouveau_biome in ["FORET","VILLAGE"]:
                self._biome = nouveau_biome
            else: raise NomError("Les biomes sont: FORET, VILLAGE.")
        else: raise NomError("Le biome doit être un string.")

    # -------------------- Méthode Class --------------------

    def inserer_heros(self, dict_heros: dict, dict_type_hero: dict):
        """ Fonction qui permet d'insérer les heros dans
        'Dictionnaire_hero.json' dans 'self.placement_hero'. Classes complètes dans un fichier.json,
        ils seront créés ici. """
        liste_nom = []
        liste_type = []
        liste_stat = []
        for hero_dans_dict, type_stat_dict in dict_heros.items():
            liste_nom.append(hero_dans_dict)
            for type_dans_dict, stats_dans_dict in type_stat_dict.items():
                liste_type.append(type_dans_dict)
                liste_stat.append(stats_dans_dict)
        liste_hero = []
        # Boucle créant des variables selon le nombre de heros.
        for hero in range(len(liste_nom)):
            globals()['hero$s' .format(hero)] = Hero(liste_nom[hero],"HERO")
            globals()['hero$s' .format(hero)].attribuer_stat(liste_type[hero],dict_type_hero)
            globals()['hero$s' .format(hero)].stats = liste_stat[hero]
            liste_hero.append(globals()['hero$s' .format(hero)])
        self.placement_hero.extend(liste_hero)
        return self.placement_hero


    def generer_ennemis(self, dict_scenario: dict, dict_ennemi: dict):
        """ Fonction qui génère des ennemis selon le 'biome' et les
        ennemis dans le fichier 'Dictionnaire_scenario.json'. """
        ennemi1 = Ennemi(None, "Ennemi")
        ennemi2 = Ennemi(None, "Ennemi")
        ennemi3 = Ennemi(None, "Ennemi")
        ennemi4 = Ennemi(None, "Ennemi")
        # Génère un index de scénario aléatoire, sauf si combat final.
        index_generer = randint(1,6) # 7,8 pas encore fait.
        if self.combat_final: index_generer = randint(9,10)
        # Deux boucles pour trouver l'index dans 'Dictionnaire_scenario'
        # et attribuer ses ennemis dans 'self.placement_ennemi'.
        for biome, index_scenario in dict_scenario.items():
            for index, scenario in index_scenario.items():
                # Le 'biome' est une propriété attribuée dans la classe.
                if self.biome == biome:
                    if index_generer == int(index):
                        ennemi1.attribuer_stat(scenario[0], dict_ennemi)
                        ennemi2.attribuer_stat(scenario[1], dict_ennemi)
                        ennemi3.attribuer_stat(scenario[2], dict_ennemi)
                        ennemi4.attribuer_stat(scenario[3], dict_ennemi)
        # 'extend' est identique à 'append' pour plusieurs variables.
        self.placement_ennemi.extend([ennemi1,ennemi2,ennemi3,ennemi4])
        return self.placement_ennemi


    def verifier_equipe_vivante(self, dict_heros:dict):
        """ Sous fonction utilisée dans 'système_tours' qui
        vérifie s'il reste des heros ou des ennemis vivants. Est
        compatible avec 'placement_hero' et 'placement_ennemi'."""
        heros_mort = 0
        for nom_dans_dict, type_dans_dict in dict_heros.items():
            for type_hero, stats in type_dans_dict.items():
                if stats["point_vie"] <= 0: heros_mort += 1
        if heros_mort == len(dict_heros):
            return "0 heros vivants"
        ennemi_mort = 0
        for ennemi in self.placement_ennemi:
            if ennemi.stats["point_vie"] <= 0: ennemi_mort += 1
        if ennemi_mort == len(self.placement_ennemi):
            return "0 ennemis vivants"


    def evaluation_agilite_personnage(self):
        """ Dans un tour, tous les personnages jouent. Leurs ordres
        dépens de leur 'point_abilite'. Le plus haut, joue en premier:
        Max=10 et min=1, 0 est pour les obstacles immobiles."""
        ordre_personnages = []
        personnage_agilite_plus_haut = 0
        for hero in self.placement_hero: ordre_personnages.append(hero)
        for ennemi in self.placement_ennemi: ordre_personnages.append(ennemi)
        for personnage in ordre_personnages:
            if personnage.stats["point_agilite"] >= personnage_agilite_plus_haut:
                personnage_agilite_plus_haut = personnage.stats["point_agilite"]
                # Enlève 'personnage' à sa position pour le mettre au début.
                ordre_personnages.remove(personnage)
                ordre_personnages.insert(0,personnage)
        return ordre_personnages


    def systeme_tours(self, dict_heros:dict):
        """ Système de tours, Tous les personnages 'Hero','Ennemi'
        jouent leurs actions. Après toutes les actions, le tour est
        terminé. 'nombre_personnage' est 8 = héro + ennemi. """
        nombre_personnage = len(self.placement_hero)
        nombre_personnage += len(self.placement_ennemi)
        # Paramètre pour le début de chacun des combats.
        conclusion = "Continue"
        tours_combat = 0
        while conclusion == "Continue":
            for act in range(nombre_personnage):
                ordres_personnage = self.evaluation_agilite_personnage()
                for personnage in ordres_personnage:
                    action = input("Qu'elle est l'action: ")
                    cible = input("Qui est la cible: ")
                    action = Action(personnage, action, cible)
                verification = self.verifier_equipe_vivante(dict_heros)
                if verification == "0 heros vivants": conclusion = "Defeat"
                if verification == "0 ennemis vivants": conclusion = "Victoire"
                if conclusion == "Defeat" or conclusion == "Victoire": break
            if conclusion == "Defeat" or conclusion == "Victoire": break
            tours_combat += 1
            print(f"tour:{tours_combat}")
        print(f"{conclusion}")
        return conclusion


    # Avant de commencer le combat, vérifier si les heros sont
    # vivants. Minimum 1 hero vivant.
    def fin_combat(self):
        """ Terminer le combat si tous les héros ou les ennemis
        sont morts. """
        # heros_vivants = True   si au moins un élément est vrai
        heros_vivants = any(h.stats["point_vie"] > 0 for h in
                            self.placement_hero)
        ennemis_vivants = any(e.stats["point_vie"] > 0 for e in
                              self.placement_ennemi)
        return not (heros_vivants and ennemis_vivants)

    def placement_avancer_reculer(self):
        """ Permet d'avancer ou de reculer le personnage choisi. """
        # Boucle
        while True:
            # Choisir Héro 1
            choix_hero1 = int(input("Choisissez l'héro selon sa "
                                    "position (1, 2, 3, 4) : "))
            # Héro 2
            choix_hero2 = int(input("Choisissez le deuxième héro "
                                    "selon position sa position "
                                    "(1, 2, 3, 4) : "))
            # Ne peut pas choisir le même héro
            if choix_hero1 == choix_hero2:
                print("Choisissez un autre.!")
            else:
                # échanger de positions
                (self.placement_hero[choix_hero1],
                 self.placement_hero[choix_hero2]) = (
                    self.placement_hero[choix_hero2],
                    self.placement_hero[choix_hero1])
            # Demander si tu veux continuer ou non
            choix = input("Continuer ou quitter ? : ").lower()
            if choix == "quitter": break
            elif choix == "continuer": continue
