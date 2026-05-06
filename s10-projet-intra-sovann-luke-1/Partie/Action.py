
# Fichier de Vann Sovannthanant et de Luke Immanuel Legaspina.
# -------------------- Importation --------------------
import random
from Partie import Hero, Ennemi, Combat

# -------------------- Class Personnage --------------------
class Action:
    def __init__(self, personnage: Hero|Ennemi, nom_action:str, cible:Hero|Ennemi):
        """ Propriétés(3/3) de la classe Action. (Propriétés) """
        self.personnage = personnage
        self.nom_action = nom_action
        self.cible = cible

    # -------------------- Méthodes class --------------------

    def raccourci_dict_abilite(self, dict_abilite:dict):
        """ NOTES SUR L'EXPLORATION DES DICTIONNAIRES.
        Je te conseille de regarder le fichier 'main_Action' pour mieux comprendre.
        Pour les ("GUERRIER, etc"), ("tout autre que le type du perso") dans 'Abilite_Hero'.
            Si ("GUERRIER, etc") est équivalent au type de "self personnage" :
                Pour "type actions", "actions" dans "tout autre que le type du perso".
                    Retourne "tout autre que le type du perso". """
        for type_personnage_dans_dict, dict_type_actions in dict_abilite.items(): # Pour chaque type hero (ex: Guerrier, Support, etc) et leurs type d'actiosn (ACTION_ATTAQUE, etc) dans le dictionnaire fichier Abilite_Hero
            if self.personnage.stats_ajouter == type_personnage_dans_dict: # Si GUERRIER == GUERRIER
                for type_actions, actions in dict_type_actions.items():
                    return dict_type_actions
        raise Exception ("Le personnage ne possède pas cette action.")


    def verification_type_actions(self, dict_abilite:dict, combat:Combat):
        """ Fonction qui vérifie qu'elle type d'action, "self.nom_action" appartient à
        puis lance une fonction selon ce type d'action. """
        nom_action = self.nom_action
        dict_type_actions = self.raccourci_dict_abilite(dict_abilite)
        for type_actions, actions in dict_type_actions.items():
            for action, effet in actions.items():
                if action == nom_action:
                    dict_actions = actions
                    if type_actions == "ACTION_ATTAQUE": self.action_attaque(dict_actions)
                    if type_actions == "ACTION_GUERISON": self.action_guerir(effet)
                    if type_actions == "ACTION_BLOQUER": self.action_bloquer(dict_abilite)
                    if type_actions == "ACTION_ESQUIVER": self.action_esquiver(dict_abilite)
                    if type_actions == "ACTION_DEPLACER": self.deplacer_position(dict_actions, combat)


    def deplacer_position(self, dict_actions: dict, combat):
        """ Fonction de déplacement, change la position(index) du personnage dépendant
        de sa position initiale. Il peut se déplacer en avant ou en arrière."""
        # Attribution de multiples variables en une seule ligne.
        placement, nouveau_placement, position = [], [], 0
        index, personne_deplacer = 0, None  # Pas nécessaire, pour enlever des avertissements.
        if self.personnage.type == "HERO": placement = combat.placement_hero
        if self.personnage.type == "ENNEMI": placement = combat.placement_ennemi
        for personne in placement:
            if personne.nom == self.personnage.nom:
                index = position
                personne_deplacer = personne
            position += 1
            nouveau_placement.append(personne)
        for nom_action, dict_effet in dict_actions.items():
            nouveau_placement.pop(index)
            nouveau_placement.insert(index + dict_effet["changer_index"], personne_deplacer)
            break
        if self.personnage.type == "HERO":
            combat.placement_hero = nouveau_placement
            return combat.placement_hero
        elif self.personnage.type == "ENNEMI":
            combat.placement_ennemi = nouveau_placement
            return combat.placement_ennemi


    def action_attaque(self, dict_actions:dict):
        """ Fonction d'attaque, sert à enlever des ["point_vie"] de la cible dépendant
        des points de mélee et des points de distance."""
        print(f"Point de vie de {self.cible.stats_ajouter}: "
              f"{self.cible.stats["point_vie"]}")
        for nom_action, dict_effet in dict_actions.items():
            if dict_effet["type_degat"] == "degat_melee":
                self.cible.stats["point_vie"] -= self.personnage.stats["degat_melee"]
            elif dict_effet["type_degat"] == "degat_distance":
                self.cible.stats["point_vie"] -= self.personnage.stats["degat_distance"]
            if self.cible.stats["point_vie"] <= 0: self.cible.stats["point_vie"] = 0
            break
        print(f"Point de vie de {self.cible.stats_ajouter}: "
              f"{self.cible.stats["point_vie"]}")

    
    def action_guerir(self, dict_actions:dict):
        """ Soigner une cible. Soi-même ou un autre héro. """
        print(f"Point de vie de {self.cible.stats_ajouter}: "
              f"{self.cible.stats["point_vie"]}")
        # Si le point de vie de la cible est au max.
        if self.cible.stats["point_vie"] <= self.cible.stats["point_vie_max"]:
            for nom_action_fonc, dict_effet in dict_actions.items():
                if self.nom_action == nom_action_fonc:
                    self.cible.stats["point_vie"] += dict_effet["point_guerison"]
        # Si le soin passe au-dessus de la vie maximum de la cible. Point_vie = Point_vie_max
                    if self.cible.stats["point_vie"] >= self.cible.stats["point_vie_max"]:
                        self.cible.stats["point_vie"] = self.cible.stats["point_vie_max"]
        else: print(f"La vie de {self.cible.nom} est au maximum. Aucun soin appliqué.")
        print(f"Point de vie de {self.cible.nom}: "
              f"{self.cible.stats["point_vie"]}")


    def action_bloquer(self, dict_abilite:dict):
        """ Fonction qui permet de bloquer la prochaine attaque. """
        #for type_ennemis, stats in dict_enemmis.items():
        dict_type_actions = self.raccourci_dict_abilite(dict_abilite)
        for types_actions, nom_actions in dict_type_actions.items():
            if types_actions == "ACTION_BLOQUER":
                bloquer = nom_actions[self.nom_action]
                # Dans le fichier Abilite_hero, un guerrier a une chance de 70% pour bloquer une attaque
                bloquer_reussit = random.random() <= bloquer["chance_bloquer"]
                if bloquer_reussit:
                    reduction = bloquer["reduction_degats"] # 0.5 = 50%
                    print(f"{self.personnage.nom} a bloqué l'attaque!")
                    # continuer
                    # bloquer la prochaine attaque qui vient vers lui ou les autres??
                    # degats_reduits =
                else:
                    print(f"{self.personnage.nom} n'a pas réussi à bloquer l'attaque.")


    def action_esquiver(self, dict_abilite: dict):
        """ Permet d'esquiver une attaque. """
        # Si un héro esquive une attaque, il n'y aurait aucun dégâts infligés. dépend de stat "agilité
        #exempl
        agilite = self.personnage.stats["point_agilite"]
        stat_agilite = agilite * 0.4
        esquiver = random.random() < stat_agilite
        #if "ACTION_ESQUIVER" in :

        # if esquiver:
        #     print(f"{self.personnage} a esquivé l'attaque.")
        #     return True
        # else:
        #     print(f"{self.personnage} n'a pas réussi à esquiver.")
        #     return False

        # fichier avec type action
        #    "ACTION_ESQUIVER": {
        #  "ESQUIVER": {
        #    "base": 0.1,
        #    "scaling_agilite": 0.04,
        #    "max": 0.8
        #  }
        #}
        # Pas encore sûr si esquiver devrait être passif. Dans Darkest Dungeon 1, esquiver est passif
        pass
