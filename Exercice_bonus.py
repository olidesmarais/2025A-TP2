"""
TP2 - BONUS : Mini-jeu de service au restaurant
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
    
    print("\nCommandes: z↑ s↓ q← d→ | p:prendre l:livrer")
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
    position_tables = [(1,1), (1,3), (3,1), (3,3)]
    # Les tables avec des clients en attente (« ! ») doivent être ajoutées aux positions (1,1) et (3,3).
    position_attente = [(1,1), (3,3)]
    for idx_rangee in range(5):
        rangee = []
        for idx_colonne in range(5):
            position = (idx_rangee, idx_colonne)
            # 'K' = cuisine (position 0,2)
            if position == position_cuisine:
                rangee.append('K')
            # '!' = table avec client en attente
            elif position in position_attente:
                rangee.append('!')
            # 'T' = table vide
            elif position in position_tables:
                rangee.append('L')
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
        direction (str): 'w', 's', 'a', ou 'd'
        plutôt que direction (str): 'z', 's', 'q', ou 'd'
    
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


def prendre_commande(grille, serveur_pos, commandes_en_attente):
    """
    Prend une commande si le serveur est à côté d'une table avec client.
    
    Args:
        grille (list): Grille du restaurant
        serveur_pos (tuple): Position du serveur
        commandes_en_attente (list): Liste des commandes
    
    Returns:
        tuple: (succès, nouvelle_grille, nouvelles_commandes, points_gagnes)
    """
    succes = False
    points = 0
    nouvelle_grille = [rangee[:] for rangee in grille]
    nouvelles_commandes = commandes_en_attente[:]
    
    # TODO: Vérifier si une table avec client '!' est adjacente
    # Si oui: changer '!' en 'T', ajouter position à commandes_en_attente
    # Gagner 10 points
    
    return succes, nouvelle_grille, nouvelles_commandes, points


def livrer_commande(grille, serveur_pos, serveur_porte_commande, commandes_pretes):
    """
    Livre une commande à une table.
    
    Args:
        grille (list): Grille du restaurant
        serveur_pos (tuple): Position du serveur
        serveur_porte_commande (bool): Si le serveur porte une commande
        commandes_pretes (list): Tables où livrer
    
    Returns:
        tuple: (succès, points_gagnes)
    """
    succes = False
    points = 0
    
    # TODO: Si serveur_porte_commande et serveur à côté d'une table dans commandes_pretes
    # Livrer la commande et gagner 20 points
    
    return succes, points


def generer_nouveaux_clients(grille, tables_positions, probabilite=0.3):
    """
    Génère aléatoirement de nouveaux clients aux tables vides.
    
    Args:
        grille (list): Grille du restaurant
        tables_positions (list): Positions de toutes les tables
        probabilite (float): Probabilité qu'un client arrive
    
    Returns:
        list: Nouvelle grille avec clients
    """
    nouvelle_grille = [rangee[:] for rangee in grille]
    
    # TODO: Pour chaque table vide 'T'
    # Avec une certaine probabilité, placer un client '!'
    
    return nouvelle_grille


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
        # 1. Afficher l'état
        print("État du restaurant :")
        for rangee in grille:
            print(' '.join(rangee))
        print('Position du serveur :', serveur_pos)
        print('Serveur porte commande :', serveur_porte_commande)
        print('Commandes en attentes :', commandes_en_attente)
        print('Commande prete :', commandes_pretes)
        # 2. Lire l'entrée utilisateur
        action = input('Quelle action prenez-vous ? (déplacement : w, s, a ou d; prendre une commande : p; livrer une commande : l)')
        # 3. Traiter l'action (déplacement, prendre, livrer)
        match action:
            case 'p':
                resultat = prendre_commande(grille, serveur_pos, commandes_en_attente)
                # resultat -> tuple: (succès, nouvelle_grille, nouvelles_commandes, points_gagnes)
                if resultat[0]:
                    grille = resultat[1]
                    commandes_en_attente = resultat[2]
                    points_gagnes += resultat[3]
            case 'w' | 's' | 'a' | 'd':
                serveur_pos = deplacer_serveur(grille, serveur_pos, action)

        # 4. Générer nouveaux clients (tous les 3 tours)
        # 5. Mettre à jour le score
        score += points_gagnes
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
