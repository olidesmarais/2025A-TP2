"""
TP2 - BONUS : Mini-jeu de service au restaurant

CHOIX ÉDITORIAUX
En l'absence de réponses à nos interrogations sur les logiques derrières le fonctionnements de cette question bonus, nous avons pris la liberté
d'apporter certains changements aux codes. Ces choix éditoriaux sont présentés ci-dessous, accompagnés d'une justification. 
* L'étape de générer nouveaux clients (tous les 3 tours) est déplacée à la première étape d'un tour (plutôt que la 4e étape).
  À noter que selon le hasard, par contre, il n'y a parfois pas de client au début de l'exécution.
    Justification : Permet de générer des clients dès le début du premier tour.
* La fonction generer_nouveaux_clients(...) prend en entrée les commandes en attente et retourne une nouvelle version de cette liste.
    Justification : Nous assumons que les commandes_en_attente correspondent aux commandes qui n'ont pas encore été prises par le serveur.
    Par conséquent, l'adresse des tables avec de nouveaux clients (!) est ajoutée aux commandes en attente. 
* La fonction prendre_commande(...) prend en entrée pos_cuisine, commandes_pretes
    Justification : Nous assumons que la fonction 'p', lorsqu'exécutée dans la cuisine (pos_cuisine), correspond au moment où 
    le serveur prend une commande pour la livrée. 
    De plus, nous considérons que le moment où la commande est prise par le serveur correspond au moment où cette commande devient prête. 
    Finalement, lorsque la commande est prise, nous modifions la table à 'O', pour occupée, pour signifier que des clients y sont toujours.
    Ces clients attendent que leur commande leur soit livrée. 
* La fonction livrer_commande(...) retourne la variable commande_prete.
    Justification : Nous considérons qu'une fois la commande livrée, la commande est retirée des commandes prête. 
    À noter que de nouveaux clients peuvent arriver au moment où la commande est livrée, auquel cas la table passe de 'O' à '!' sans retourner à 'T'.
"""

import random

# Fonction fournie - ne pas modifier
def effacer_ecran():
    """Efface l'écran pour une meilleure lisibilité."""
    print('\n' * 5)


def afficher_restaurant(grille, serveur_pos, score, commandes_en_attente):
    """
    Affiche l'état du restaurant.
    
    Args:
        grille (list): Grille du restaurant
        serveur_pos (tuple): Position (ligne, colonne) du serveur
        score (int): Score actuel
        commandes_en_attente (list): Liste des tables avec commandes
    """
    effacer_ecran()
    print("=" * 30)
    print(f"SCORE: {score} | Commandes en attente: {len(commandes_en_attente)}")
    print("=" * 30)
    
    for i, rangee in enumerate(grille):
        for j, case in enumerate(rangee):
            if (i, j) == serveur_pos:
                print('S', end=' ')  # Serveur
            else:
                print(case, end=' ')
        print()
    
    print("\nCommandes: w↑ s↓ a← d→ | p:prendre l:livrer")
    print("=" * 30)


def initialiser_restaurant():
    """
    Initialise le restaurant avec des tables et la cuisine.
    
    Returns:
        tuple: (grille, position_cuisine, tables_positions)
    """
    grille = []
    tables_positions = []
    
    # TODO: Créer une grille 5x5
    position_cuisine = (0, 2)
    # Placer 4 tables aux positions: (1,1), (1,3), (3,1), (3,3)
    tables_positions = [(1,1), (1,3), (3,1), (3,3)]
    for idx_rangee in range(5):
        rangee = []
        for idx_colonne in range(5):
            position = (idx_rangee, idx_colonne)
            # 'K' = cuisine (position 0,2)
            if position == position_cuisine:
                rangee.append('K')
            # 'T' = table vide
            elif position in tables_positions:
                rangee.append('T')
            # '_' = espace vide
            else:
                rangee.append("_")
        grille.append(rangee)
    
    return grille, position_cuisine, tables_positions


def deplacer_serveur(grille, serveur_pos, direction):
    """
    Déplace le serveur dans la direction donnée.
    
    Args:
        grille (list): Grille du restaurant
        serveur_pos (tuple): Position actuelle
        direction (str): 'w', 's', 'a', ou 'd' - plutôt que direction (str): 'z', 's', 'q', ou 'd'
    
    Returns:
        tuple: Nouvelle position ou position actuelle si mouvement invalide
    """
    nouvelle_pos = serveur_pos
    
    # TODO: Calculer la nouvelle position selon la direction
    match direction:
        case 'w':
            nouvelle_pos = (serveur_pos[0] - 1, serveur_pos[1])
        case 's':
            nouvelle_pos = (serveur_pos[0] + 1, serveur_pos[1])
        case 'a':
            nouvelle_pos = (serveur_pos[0], serveur_pos[1] - 1)
        case 'd':
            nouvelle_pos = (serveur_pos[0], serveur_pos[1] + 1)
    
    # Vérifier que la position est valide (dans la grille)
    nouvelle_pos = ( max(0, min( nouvelle_pos[0], len(grille[0]) - 1 )), max( 0, min(nouvelle_pos[1], len(grille) - 1 )))

    # Retourner la nouvelle position
    return nouvelle_pos


def prendre_commande(grille, serveur_pos, commandes_en_attente, pos_cuisine, commandes_pretes):
    """
    Prend une commande si le serveur est à côté d'une table avec client.
    
    Args:
        grille (list): Grille du restaurant
        serveur_pos (tuple): Position du serveur
        commandes_en_attente (list): Liste des commandes
        + pos_cuisine (tuple): Position de la cuisine dans la grille (voir choix éditoriaux dans le haut de ce document)
        + commandes_pretes (list): Liste des tables où les commandes sont prête (voir choix éditoriaux dans le haut de ce document)
    
    Returns:
        tuple: (succès, nouvelle_grille, nouvelles_commandes_en_attente, points_gagnes, nouvelles_commandes_pretes)
    """
    succes = False
    points = 0
    nouvelle_grille = [rangee[:] for rangee in grille]
    nouvelles_commandes_en_attente = commandes_en_attente[:]
    nouvelles_commandes_pretes = commandes_pretes[:]
    
    if serveur_pos == pos_cuisine:
        if len(nouvelles_commandes_pretes) > 0:
            succes = True
    else:
        # TODO: Vérifier si une table avec client '!' est adjacente
        # Correspond aux commandes en attente (voir choix éditoriaux au début du document)
        for table in nouvelles_commandes_en_attente:
            # Au-dessus
            au_dessus = serveur_pos[0] == table[0] - 1 and serveur_pos[1] == table[1]
            # En-dessous
            en_dessous = serveur_pos[0] == table[0] + 1 and serveur_pos[1] == table[1]
            # À gauche
            a_gauche = serveur_pos[0] == table[0] and serveur_pos[1] == table[1] - 1
            # À droite
            a_droite = serveur_pos[0] == table[0] and serveur_pos[1] == table[1] + 1
            # Si oui: 
            if au_dessus or en_dessous or a_gauche or a_droite:
                succes = True
                # La commande n'est plus en attente.
                nouvelles_commandes_en_attente.remove(table)
                # La commande devient prête à être ramassée en cuisine.
                nouvelles_commandes_pretes.append(table)
                # changer '!' en 'O', ajouter position à commandes_en_attente - Changé pour un 'O', plutôt qu'un T. (Voir choix éditoriaux au début de ce document.)
                nouvelle_grille[table[0]][table[1]] = 'O'
                # Gagner 10 points
                points = 10
                break
    
    return succes, nouvelle_grille, nouvelles_commandes_en_attente, points, nouvelles_commandes_pretes


def livrer_commande(grille, serveur_pos, serveur_porte_commande, commandes_pretes):
    """
    Livre une commande à une table.
    
    Args:
        grille (list): Grille du restaurant
        serveur_pos (tuple): Position du serveur
        serveur_porte_commande (bool): Si le serveur porte une commande
        commandes_pretes (list): Tables où livrer
    
    Returns:
        tuple: (succès, points_gagnes, nouvelle_grille, nouvelles_commandes_pretes)
    """
    succes = False
    points = 0
    nouvelle_grille = grille[:]
    nouvelles_commandes_pretes = commandes_pretes[:]
    
    # TODO: Si serveur_porte_commande et serveur à côté d'une table dans commandes_pretes
    if serveur_porte_commande:
        for table in nouvelles_commandes_pretes:
            # Au-dessus
            au_dessus = serveur_pos[0] == table[0] - 1 and serveur_pos[1] == table[1]
            # En-dessous
            en_dessous = serveur_pos[0] == table[0] + 1 and serveur_pos[1] == table[1]
            # À gauche
            a_gauche = serveur_pos[0] == table[0] and serveur_pos[1] == table[1] - 1
            # À droite
            a_droite = serveur_pos[0] == table[0] and serveur_pos[1] == table[1] + 1
            if au_dessus or en_dessous or a_gauche or a_droite:
                # Livrer la commande
                succes = True
                # Commande retirée des commandes prêtes
                nouvelles_commandes_pretes.remove(table)
                # La table redevient disponible
                grille[table[0]][table[1]] = 'T'
                # Gagner 20 points
                points = 20
                break
        
    return succes, points, nouvelle_grille, nouvelles_commandes_pretes


def generer_nouveaux_clients(grille, tables_positions, commandes_en_attentes, probabilite=0.3):
    """
    Génère aléatoirement de nouveaux clients aux tables vides.
    
    Args:
        grille (list): Grille du restaurant
        tables_positions (list): Positions de toutes les tables
        + commandes_en_attentes (list) : Position des tables en attente (voir choix éditoriaux décris au début du document)
        probabilite (float): Probabilité qu'un client arrive
    
    Returns:
        nouvelle_grille (list): Nouvelle grille avec clients
        nouvelles_commandes_en_attente (list): Position des tables avec client en attente = avec commande en attente (voir choix éditoriaux au début de ce document.)
    """
    nouvelle_grille = [rangee[:] for rangee in grille]
    nouvelles_commandes_en_attente = commandes_en_attentes[:]
    
    # TODO: Pour chaque table vide 'T'
    for table in tables_positions:
        if nouvelle_grille[table[0]][table[1]] == 'T':
            # Avec une certaine probabilité, placer un client '!'
            nouveau_client = random.random() <= probabilite
            if nouveau_client:
                nouvelle_grille[table[0]][table[1]] = '!'
                # Ajout de la commande de cette nouvelle table aux commandes en attente.
                nouvelles_commandes_en_attente.append(table)
    
    return nouvelle_grille, nouvelles_commandes_en_attente


def jouer():
    """
    Boucle principale du jeu.
    """
    # Initialisation
    grille, pos_cuisine, tables_pos = initialiser_restaurant()
    serveur_pos = (2, 2)  # Centre du restaurant
    score = 0
    commandes_en_attente = []
    commandes_pretes = []
    serveur_porte_commande = False
    tours = 0
    max_tours = 50
    
    print("=== BIENVENUE AU PYTHON BISTRO ===")
    print("Objectif: Servir un maximum de clients!")
    print("Prenez les commandes (p) et livrez-les (l)")
    print("Appuyez sur Entrée pour commencer...")
    input()
    
    # TODO: Implémenter la boucle de jeu
    points_gagnes = 0
    while tours < max_tours:
        # 1. Générer nouveaux clients (tous les 3 tours) - Étape devancée (voir choix éditoriaux au début ce document.)
        if tours % 3 == 0:
            grille, commandes_en_attente = generer_nouveaux_clients(grille, tables_pos, commandes_en_attente)
        # 2. Afficher l'état
        afficher_restaurant(grille, serveur_pos, score, commandes_en_attente)
        # 3. Lire l'entrée utilisateur
        action = input('Quelle action prenez-vous ? (déplacement : w, s, a ou d; prendre une commande : p; livrer une commande : l)')
        # 4. Traiter l'action (déplacement, prendre, livrer)
        match action:
            case 'p':
                resultat = prendre_commande(grille, serveur_pos, commandes_en_attente, pos_cuisine, commandes_pretes)
                # resultat -> tuple: (succès, nouvelle_grille, nouvelles_commandes_en_attente, points_gagnes, nouvelles_commandes_pretes, serveur_porte_commande)
                if resultat[0]:
                    grille = resultat[1]
                    commandes_en_attente = resultat[2]
                    points_gagnes += resultat[3]
                    commandes_pretes = resultat[4]
                    serveur_porte_commande = True
            case 'l':
                resultat = livrer_commande(grille, serveur_pos, serveur_porte_commande, commandes_pretes)
                # resultat -> tuple: (succès, points_gagnes, nouvelle_grille, nouvelles_commandes_pretes) (voir choix éditoriaux dans le haut de ce document)
                if resultat[0]:
                    points_gagnes += resultat[1]
                    grille = resultat[2]
                    commandes_pretes = resultat[3]
                    serveur_porte_commande = False
            case 'w' | 's' | 'a' | 'd':
                serveur_pos = deplacer_serveur(grille, serveur_pos, action)
        # 5. Mettre à jour le score
        score += points_gagnes
        points_gagnes = 0
        # 6. Incrémenter tours
        tours += 1
    
    print(f"\n=== PARTIE TERMINÉE ===")
    print(f"Score final: {score}")
    print(f"Performance: ", end="")
    if score >= 200:
        print("⭐⭐⭐ Excellent!")
    elif score >= 100:
        print("⭐⭐ Bon travail!")
    else:
        print("⭐ Continuez vos efforts!")
    
    return score


if __name__ == '__main__':
    # Test des fonctions individuelles
    print("=== Tests du mini-jeu ===")
    
    # Test initialisation
    grille, pos_cuisine, tables = initialiser_restaurant()
    print("Restaurant initialisé:")
    for rangee in grille:
        print(' '.join(rangee))
    
    # Test déplacement
    print("\nTest déplacement:")
    pos_test = (2, 2)
    nouvelle_pos = deplacer_serveur(grille, pos_test, 's')
    print(f"Position (2,2) + droite → {nouvelle_pos}")
    
    # Décommenter pour jouer
    print("\n" + "="*30)
    print("Appuyez sur Entrée pour lancer le jeu...")
    input()
    score_final = jouer()
