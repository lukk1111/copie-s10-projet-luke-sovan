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

        self.combat = None
        self.tour = 1
        self.ordre = []
        self.index = 0

        self.action = None
        self.cible = None

    def init_combat(self):
        if not (0 < len(self.dict_heros) <= 4):
            raise ValueError("Pas assez de héros")

        self.combat = Combat([], [], "FORET")
        self.combat.inserer_heros(self.dict_heros, self.dict_type_hero)
        self.combat.generer_ennemis(self.dict_scene, self.dict_ennemi)

        self.next_turn()

    def next_turn(self):
        self.ordre = self.combat.evaluation_agilite_personnage()
        self.index = 0

    def current(self):
        return self.ordre[self.index]

    def next_personnage(self):
        self.index += 1

        if self.index >= len(self.ordre):
            self.enemy_phase()
            self.tour += 1
            self.next_turn()

    def enemy_phase(self):
        import random

        ennemis = [e for e in self.combat.placement_ennemi if e.stats["point_vie"] > 0]
        heros = [h for h in self.combat.placement_hero if h.stats["point_vie"] > 0]

        for ennemi in ennemis:
            if heros:
                cible = random.choice(heros)
                cible.stats["point_vie"] -= ennemi.stats["degat_melee"]

                if cible.stats["point_vie"] < 0:
                    cible.stats["point_vie"] = 0

    def do_action(self, cible):
        perso = self.current()

        action = Action(perso, self.action, cible)
        action.verification_type_actions(self.dict_abilite, self.combat)

        self.action = None
        self.next_personnage()

    