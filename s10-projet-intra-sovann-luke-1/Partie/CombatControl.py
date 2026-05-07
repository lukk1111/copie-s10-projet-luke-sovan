# Gestion combat + state
from Partie import (lire_stats_json, Hero, Ennemi)
from Partie import Personnage, Hero, Ennemi, Combat, Action
from dataclasses import field
from datetime import datetime
from typing import Callable
from pathlib import Path
import flet as ft
import asyncio
import json
import sys
import random

class CombatController:
    def __init__(self, dicts):
        self.dict_heros = dicts["heros"]
        self.dict_ennemi = dicts["ennemi"]
        self.dict_abilite = dicts["abilite"]
        self.dict_scene = dicts["scene"]
        self.dict_type_hero = dicts["type_hero"]

        self.combat = None # Contiendra l’objet Combat une fois le combat créé
        self.tour = 1 # Numéro du tour actuel
        self.ordre = [] # Liste de personnages qui vont jouer dans l'ordre du tour
        self.index = 0 # Position du personnage actuel

        self.action = None # Action choisie par le joueur.
        self.cible = None # Cible de l'action
        self.etat_combat = None

    def init_combat(self): # Initialisation du combat
        if not (0 < len(self.dict_heros) <= 4): # Minimum 1 héro. Maximum 4 héros.
            raise ValueError("Pas assez de héros")

        self.combat = Combat([], [], "FORET")
        self.combat.inserer_heros(self.dict_heros, self.dict_type_hero)
        self.combat.generer_ennemis(self.dict_scene, self.dict_ennemi)

        self.next_turn() # Démarrage du premier tour

    def next_turn(self): # Prépare un nouveau tour
        ordre_complet = self.combat.evaluation_agilite_personnage()

        # Garder seulement les héros vivants
        self.ordre = [
            p for p in ordre_complet
            if isinstance(p, Hero) and p.stats["point_vie"] > 0
        ]
        self.index = 0

    def personnage_actuel(self):
        if not self.ordre:
            return None

        perso = self.ordre[self.index]

        #  bloquer les ennemis dans UI
        if isinstance(perso, Ennemi):
            return None

        return perso

    def prochain_personnage(self):
        self.index += 1 # avancer d'un index.

        if self.index >= len(self.ordre): # Vérifier si on arrive à la fin de la liste
            self.enemmi_phase() # Si les tous les héros ont joué, les ennemis attaquent

            resultat = self.check_fin_combat()
            if resultat:
                self.etat_combat = resultat
                return

            self.tour += 1 # Le tour augmente
            self.next_turn() # Un nouveau tour commence

    def enemmi_phase(self):
        import random

        ennemis = [e for e in self.combat.placement_ennemi if e.stats["point_vie"] > 0]
        heros = [h for h in self.combat.placement_hero if h.stats["point_vie"] > 0] # Liste des héros vivants

        for ennemi in ennemis:
            if heros:
                cible = random.choice(heros)
                cible.stats["point_vie"] -= ennemi.stats["degat_melee"]

                if cible.stats["point_vie"] < 0: # empêcher les points de vie négatifs
                    cible.stats["point_vie"] = 0

    def do_action(self, cible):
        perso = self.personnage_actuel()

        action = Action(perso, self.action, cible)
        action.verification_type_actions(self.dict_abilite, self.combat)

        self.action = None
        self.prochain_personnage()

        resultat = self.check_fin_combat()
        if resultat:
            self.etat_combat = resultat

    def check_fin_combat(self):
        heros_vivants = any(h.stats["point_vie"] > 0 for h in self.combat.placement_hero)
        ennemis_vivants = any(e.stats["point_vie"] > 0 for e in self.combat.placement_ennemi)

        if not heros_vivants:
            return "DEFAITE"
        if not ennemis_vivants:
            return "🎆 VICTOIRE 🎆"


        return None

    