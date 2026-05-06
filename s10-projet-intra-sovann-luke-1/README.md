[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/XtBEFomB)
# Projet de session

## Présentation
### Description du projet
Décrire le projet en environ 1 paragraphe. Quel est votre sujet ? Quelles sont les fonctionnalités principales ?
```
    Jeu Roguelike tour par tour
Nous allons créer un jeu tour par tour de type "rogue-like" (exploration dans un donjon pour gagner des récompenses).
Avant l'adventure, le joueur doit choisir 3 aventuriers parmi une liste d'aventuriers.Ils ont chacun des spécialisations
qui leurs attribue des avantages et des désavantages. Pour le moment on à penser à trois types: guerrier, chasseur et 
support. Ces héros ont aussi avec eux des équipements et des armes qui peuvent être changer lors de l'aventure.
Lors de l'exploration, le groupe tombe sur des combats et des événements, le dernier combat est un ennemi majeur(boss).

V Notes pour Sovannthanant et Luke. V
    Notes de méchanismes du jeu:
- 4-6 combats par partie, dernier est l'ennemi majeur(chef/boss).
- 0-2 évenements apres combat (marchand, malues, bonus, etc...)
- Biomes différents (Après chaque partie ou quelques combats?)
- Emplacement des personnages (devant, millieu, arrière)

    Notes sur les stats (dans la Class Personnages)
Stats essentiel:
- degat_melee
- degat_distance
- point_vie
- agilite (esquive et tour)
- chance (critique et contre-esquive)
```

### Membres de l'équipe et division des tâches
```
Inscrire le nom des membres de l'équipe et les tâches qui leurs sont assignées.

    Vann Sovannthanant
Classes : Personnage, Ennemi, Actions, Combat
Interface graphique : Creation_Personnage,
Tests : test_Personnage, test_Hero, test_Combat, test_action

    Luke Immanuel Legaspina
Classes : Hero, Combat, Actions
Interface graphique : Combat,
Tests : test_Ennemi, test_combat, test_action
```

## Conception
### Diagramme de classes
```mermaid
classDiagram
    class Personnage {
        <<Class Parent de Hero et Ennemi>>
        + nom:str
        + type: Hero | Ennemi
        - stats: dict
        - stats_ajouter: None
        + attribuer_stat(self, nom_type, dict_stats_ajouter)
        - afficher_informations(self)
        - __str__(self)
    }
    class Hero {
        <<Class Enfant de Personnage>>
        - nom:str
        + type: Hero
        - stats: dict
        - stats_ajouter: None
        + attribuer_stat(self, nom_type, dict_stats_ajouter)
        + ecrire_stats_hero(self, chemin_fichier, dict_heros)
    }
    class Ennemi {
        <<Class Enfant de Personnage>>
        - nom:str
        + type: Ennemi
        - stats: dict
        - stats_ajouter: None
    }
    class Action {
        - personnage: Hero | Ennemi
        + nom_action: str
        + cible: Hero | Ennemi
        - verifier_action(self)
        + action_attaque(self)
        + action_guerir(self)
        + action_bloquer(self)
        + deplacer_devant(self)
        + deplacer_arriere(self)
    }
    class Combat {
        - placement_hero:list[Personnage]
        - placement_ennemi:list[Personnage]
        - biome: str
        + inserer_heros(self, dict_heros, dict_type_hero)
        - generer_ennemis(self, dict_scenario, dict_ennemi)
        - verifier_equipe_vivante(self, dict_heros)
        - evaluation_agilite_personnage(self)
        - systeme_tours(self, dict_heros)
    }
    class Partie {
        <<?>>
        - nom: str
        - date: datetime
        - sauvegarde: fichier.json
        + Charger(self) fichier.json
        + Sauvegarder(self) fichier.json
    }

    Personnage <|-- Hero: Class enfant de
    Personnage <|-- Ennemi:class enfant de
    Combat <-- Personnage
    Action <-- Personnage: Contient des
    Combat --> Action: Peut accéder aux
    Partie <-- Combat: Se trouve dans
```

### Diagramme de cas d'utilisation
### Le plan Initiale
```mermaid
flowchart TB
    %% Déclaration des acteurs.
    UJoueur["👤Joueur"]
    %% Déclaration des cas d'utilisation.
    CasMenu(["Menu"])
    CasCommencer(["Commencer"])
    CasContinuer(["Continuer"])
    CasQuitter(["Quitter"])
    %% Lien des acteurs aux cas d'utilisation.
    UJoueur --> CasMenu
    CasMenu --> CasCommencer
    CasMenu --> CasContinuer
    CasMenu --> CasQuitter
    CasCommencer --> CasIntroduction
    CasCommencer --Optionel--> CasTutoriel
    CasContinuer --> CasFichiers
    
    CasPause --> CasQuitter
    CasSauvegarde --> CasQuitter
    CasConclusion --> CasQuitter
    %% Création d'un sous système du Jeu
    subgraph Système du jeu
        %% Déclaration des cas d'utilisation.
        CasTutoriel(["Tutoriel"])
        CasIntroduction(["Introduction"])
        CasRecrutement(["Recrutement"])
        CasPreparation(["Preparation"])
        CasConclusion(["Conclusion"])
        %% Lien des acteurs aux cas d'utilisation.
        CasTutoriel --> CasIntroduction
        CasIntroduction --> CasRecrutement
        CasRecrutement --> CasPreparation
        CasPreparation --> CasCarte
        %% J'ai mis ces flèches sinon ça devenait chaotique.
        CasCombat --Combat Final--> CasConclusion
        CasRecrutement --Recommencer--o CasPause
        CasRecrutement --Recommencer--o CasConclusion 
        %% Création d'un sous système de partie.
        subgraph Système de partie
            %% Déclaration des cas d'utilisation.
            CasCarte(["Carte"])
            CasCombat(["Combat"])
            CasEvenement(["Evenement/magasin"])
            CasInventaire(["Inventaire"])
            CasPause(["Pause"])
            %% Lien des acteurs aux cas d'utilisation.
            CasCarte --> CasCombat
            CasCarte --> CasEvenement
            CasCarte --Accède--> CasPause
            CasCarte --Accède--> CasInventaire
            CasCombat --> CasCarte
            CasEvenement --> CasCarte
            CasPause --Retourne--> CasCarte
            CasInventaire --Retourne--> CasCarte
            
            
        end
    end
    %% Création d'un sous système de Sauvegarde
    subgraph Système de sauvegarde
        %% Déclaration des cas d'utilisation.
        CasFichiers(["Fichiers"])
        CasCharger(["Charger"])
        CasSauvegarde(["Sauvegarde"])
        %% Lien des acteurs aux cas d'utilisation.
        CasPause --> CasSauvegarde
        CasFichiers --> CasCharger
        CasCharger --> CasCarte
        CasSauvegarde --> CasFichiers
        
    end
```
### Le plan Final
```mermaid
flowchart LR
    %% Déclaration des acteurs.
    UJoueur["👤Joueur"]

    %% Déclaration des cas d'utilisation.
    CasJouer(["Jouer"])
    CasQuitter(["Quitter"])
    
    %% Lien des acteurs aux cas d'utilisation.
    UJoueur --> CasGererHeros
    UJoueur --> CasJouer
    UJoueur --> CasQuitter
    CasJouer --> CasCombat
    
    %% Création d'un sous système de combat.
    subgraph Gerer Héros
        direction LR
        %% Déclaration des cas d'utilisation.
        CasGererHeros(["Gerer Héros"])
        CasVoirEquipe(["Voir Équipe"])
        CasVoirClasses(["Voir Classes"])
        CasCreerHero(["Créer héro"])
        CasEnleverHero(["Enlevez héro"])
        
        %% Lien des acteurs aux cas d'utilisation.
        CasGererHeros --> CasVoirEquipe
        CasGererHeros --> CasVoirClasses
        CasGererHeros --> CasCreerHero
        CasGererHeros --> CasEnleverHero
    end
    subgraph Systeme Combat
        direction LR
        %% Déclaration des acteurs.
        UHero["Hero"]
        UEnnemi["Ennemi"]

        %% Déclaration des cas d'utilisation.
        CasCombat(["Combat"])
        CasSystemeTour(["Système_Tour"])
        CasAction(["Action"])
        CasConclusion(["Conclusion"])
        CasVictoire(["Victoire"])
        CasDefaite(["Défaite"])
        
        %% Lien des acteurs aux cas d'utilisation.
        CasCombat --> CasSystemeTour
        CasSystemeTour --> UHero
        CasSystemeTour --> UEnnemi
        UHero <--> CasAction
        UEnnemi <--> CasAction
        CasSystemeTour --Si une équipe reste--> CasConclusion
        CasConclusion --> CasVictoire
        CasConclusion --> CasDefaite
        end
```

## Avancement et vérification des exigences
Vous pouvez ajouter des numéros de billets et ajouter des éléments. L'objectif est de vous aider à faire la gestion de votre projet.

### Documentation et organisation du code
- [x] Documentation de la personne responsable de chaque fichier
- [x] Documentation du code
- [x] Remise des diagrammes dans le projet
- [x] Organisation du code à l'aide d'au moins 2 _packages_

### Orienté-objet
- [x] Diagramme de classes
- [x] Au moins 4 classes qui entrent en relation (3 si vous êtes seul)
- [x] Au moins 3 propriétés par classe
- [x] Utilisation de l’héritage
- [x] Utilisation des accesseurs et des mutateurs
- [x] Utilisation d’au moins une exception personnalisée par personne

### Logique applicative
- [x] Diagramme de cas d'utilisation
- [x] Créer, modifier et supprimer différents objets
- [x] Afficher des objets selon leur relation avec d’autres objets 
- [x] Manipuler des dates
- [x] Valider adéquatement les données
- [x] Enregistrer les données
- [x] Charger les données au lancement de l’application

### Interface graphique
- [ ] Planification/ébauche
- [x] La taille relative des éléments est logique
- [x] Alignement adéquat des éléments graphiques
- [x] Messages d’erreurs situés près des erreurs
- [x] Confirmation des actions destructrices

### Contrôle de qualité
- [x] Tests unitaires
- [x] Appliquer les recommandations suite à la remise formative du 24 avril
- [x] Appliquer les recommandations suite à la rétroaction par les pairs
