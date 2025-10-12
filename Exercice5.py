"""
TP2 - Exercice 5 : Analyse de la satisfaction client
"""

def analyser_commentaire(commentaire, mots_cles):
    """
    Analyse un commentaire client et calcule un score de satisfaction.
    
    Args:
        commentaire (str): Le commentaire du client
        mots_cles (dict): Dictionnaire {mot: score}
                         Positif si score > 0, négatif si score < 0
    
    Returns:
        tuple: (score_total, mots_trouves)
    """
    score_total = 5  # Score de base
    mots_trouves = []
    
    # On convertit le commentaire en minuscules
    commentaire_lower = commentaire.lower()
    
    # On crée une version du commentaire avec espaces autour pour faciliter la recherche, donc on remplace la ponctuation par des espaces
    commentaire_modifie = commentaire_lower
    for char in '.,!?;:()[]{}"\'-':
        commentaire_modifie = commentaire_modifie.replace(char, ' ')
    
    # On divise en mots pour une recherche plus précise
    mots_commentaire = commentaire_modifie.split()
    
    #TODO : Rechercher chaque mot-clé dans le commentaire
    for mot_cle in mots_cles:
        # D'abord, vérifier la correspondance exacte dans la liste des mots
        if mot_cle in mots_commentaire:
            mots_trouves.append( mot_cle )
            score_total += mots_cles[ mot_cle ]
        # Sinon, vérifier si le mot-clé est le début d'un mot du commentaire (cela permet de trouver "froid" dans "froide" ou "froids"), pour cela utiliser la méthode startswith().
        else:
            for mot_commentaire in mots_commentaire:
                if mot_commentaire.startswith( mot_cle ):
                    mots_trouves.append( mot_cle )
                    score_total += mots_cles[ mot_cle ]
    # Borner le score final entre 0 et 10
    score_total = max( 0, min( score_total, 10))
    
    return score_total, mots_trouves


def categoriser_commentaires(liste_commentaires, mots_cles):
    """
    Catégorise les commentaires selon leur score de satisfaction.
    
    Args:
        liste_commentaires (list): Liste de commentaires
        mots_cles (dict): Dictionnaire des mots-clés avec scores
    
    Returns:
        dict: Commentaires groupés par catégorie
              'positifs' (score >= 7), 'neutres' (4-6), 'negatifs' (<4)
    """
    categories = {'positifs': [], 'neutres': [], 'negatifs': []}
    
    # TODO: Analyser chaque commentaire
    for commentaire in liste_commentaires:
        # Catégoriser selon le score obtenu
        # analyse -> tuple: (score_total, mots_trouves)
        score = analyser_commentaire( commentaire, mots_cles )[0]
        # Stocker le commentaire et son score dans la bonne catégorie
        if score >= 7:
            categories['positifs'].append(( commentaire, score ))
        elif 4 <= score <= 6:
            categories['neutres'].append(( commentaire, score ))
        elif score < 4:
            categories['negatifs'].append(( commentaire, score ))
    return categories


def identifier_problemes(commentaires_negatifs, mots_cles_negatifs):
    """
    Identifie les problèmes récurrents dans les commentaires négatifs.
    
    Args:
        commentaires_negatifs (list): Liste de commentaires avec score < 4
        mots_cles_negatifs (dict): Mots-clés négatifs uniquement
    
    Returns:
        dict: Fréquence de chaque problème identifié (nombre d'apparitions)
    """
    frequence_problemes = {}
    
    # TODO: Pour chaque commentaire négatif
    for commentaire in commentaires_negatifs:
        # Compter le nombre d'apparition de chaque mot-clé négatif
        for mot_cle in mots_cles_negatifs:
            if mot_cle in commentaire:
                frequence_problemes[ mot_cle ] = frequence_problemes.get( mot_cle, 0) + 1
    # Retourner un dictionnaire trié par fréquence décroissante
    frequence_problemes = dict(sorted( frequence_problemes.items(), key=lambda item: item[1], reverse=True))
    return frequence_problemes


def generer_rapport_satisfaction(categories, frequence_problemes):
    """
    Génère un rapport complet de satisfaction client.
    
    Args:
        categories (dict): Commentaires catégorisés
        frequence_problemes (dict): Problèmes identifiés et leur fréquence (nombre d'apparitions)
    
    Returns:
        dict: Rapport avec statistiques et recommandations
    """
    rapport = {
        'satisfaction_moyenne': 0.0,
        'distribution': {},
        'points_forts': [],
        'points_amelioration': [],
    }
    
    # TODO: Calculer la satisfaction moyenne
    commentaires_total = 0
    somme_satisfaction = 0
    for categorie in categories:
        for commentaire in categories[ categorie ]:
            # commentaire -> (description, score)
            commentaires_total += 1
            somme_satisfaction += commentaire[ 1 ]
    rapport["satisfaction_moyenne"] = somme_satisfaction / commentaires_total
    # Calculer la distribution (% positifs, neutres, négatifs)
    for categorie in categories:
        commentaires_categorie = len(categories[categorie])
        rapport['distribution'][categorie] = commentaires_categorie / commentaires_total * 100
    # Ajout des points forts s'il y a plus de commentaires positifs que négatifs
    if rapport['distribution']['positifs'] > rapport['distribution']['negatifs']:
        rapport['points_forts'] = ['Service apprécié', 'Qualité reconnue']
    # Identifier les 3 principaux points d'amélioration (les 3 problèmes les plus fréquents)
    # Trier les problème par fréquence
    frequence_problemes = dict(sorted( frequence_problemes.items(), key=lambda item: item[1], reverse=True))
    compteur_pistes_amelioration = 0
    for probleme in frequence_problemes:
        rapport['points_amelioration'].append( probleme )
        compteur_pistes_amelioration += 1
        if compteur_pistes_amelioration == 3:
            break

    return rapport


def calculer_tendance(historique_scores):
    """
    Calcule la tendance de satisfaction sur plusieurs périodes.
    
    Args:
        historique_scores (list): Liste de listes [periode, score_moyen]
    
    Returns:
        str: 'amélioration', 'stable', ou 'dégradation'
    """
    tendance = 'stable'
    augmentation_constante = True
    diminution_constante = True
    score_precedent = None

    print( historique_scores )
    
    # TODO: Analyser l'évolution des scores
    for historique in historique_scores:
        score = historique[ 1 ]
        if score_precedent:
            if not score > score_precedent:
                augmentation_constante = False
            elif not score < score_precedent:
                diminution_constante = False
        score_precedent = score
    # Si augmentation constante: 'amélioration'
    if augmentation_constante:
        tendance = 'amélioration'
    # Si diminution constante: 'dégradation'
    elif diminution_constante:
        tendance = 'dégradation'
    # Sinon: 'stable'
    else:
        tendance = 'stable'
    
    return tendance


if __name__ == '__main__':
    # Dictionnaire des mots-clés et leurs scores
    mots_cles = {
        # Positifs
        'excellent': 3, 'délicieux': 2, 'parfait': 3,
        'rapide': 1, 'frais': 2, 'savoureux': 2,
        'accueillant': 1, 'propre': 1, 'recommande': 2,
        
        # Négatifs  
        'froid': -2, 'lent': -3, 'décevant': -2,
        'cher': -1, 'sale': -3, 'impoli': -2,
        'insipide': -2, 'attente': -1, 'déçu': -2
    }
    
    # Exemples de commentaires
    commentaires_test = [
        "Service excellent et plats délicieux! Je recommande vivement.",
        "Attente trop longue, et les plats étaient froids.",
        "Restaurant propre mais un peu cher pour la qualité.",
        "Très déçu, service lent et nourriture insipide.",
        "Accueil chaleureux, plats frais et savoureux!",
        "Correct, sans plus. Prix raisonnables.",
        "Parfait! Rapide, délicieux et accueillant.",
        "Sale et impoli, vraiment décevant.",
        "Bonne ambiance mais l'attente était longue.",
        "Les plats sont excellents mais le service est lent."
    ]
    
    # Test analyse de commentaire
    print("=== Analyse de commentaires individuels ===")
    for i, comm in enumerate(commentaires_test[:3], 1):
        score, mots = analyser_commentaire(comm, mots_cles)
        print(f"Commentaire {i}:")
        print(f"  Texte: '{comm[:50]}...'")
        print(f"  Score: {score}/10")
        print(f"  Mots-clés: {mots}")
    
    # Test catégorisation
    print("\n=== Catégorisation des commentaires ===")
    categories = categoriser_commentaires(commentaires_test, mots_cles)
    for cat, comms in categories.items():
        print(f"{cat.capitalize()}: {len(comms)} commentaires")
        if comms and len(comms) > 0:
            print(f"  Exemple: '{comms[0][0][:40]}...' (score: {comms[0][1]})")
    
    # Test identification problèmes
    print("\n=== Problèmes identifiés ===")
    mots_negatifs = {k: v for k, v in mots_cles.items() if v < 0}
    commentaires_negatifs = [c[0] for c in categories.get('negatifs', [])]
    problemes = identifier_problemes(commentaires_negatifs, mots_negatifs)
    
    if problemes:
        print("Problèmes récurrents (fréquence en %):")
        for probleme, freq in list(problemes.items())[:5]:
            print(f"  - {probleme}: {freq:.1f}% des commentaires négatifs")
    
    # Test rapport
    print("\n=== Rapport de satisfaction ===")
    rapport = generer_rapport_satisfaction(categories, problemes)
    print(f"Satisfaction moyenne: {rapport['satisfaction_moyenne']:.1f}/10")
    print(f"Distribution: {rapport['distribution']}")
    if rapport['points_forts']:
        print(f"Points forts: {rapport['points_forts']}")
    if rapport['points_amelioration']:
        print(f"Points d'amélioration prioritaires: {rapport['points_amelioration']}")
    
    # Test tendance
    print("\n=== Analyse de tendance ===")
    historique = [
        ['Janvier', 6.5],
        ['Février', 6.8],
        ['Mars', 7.1],
        ['Avril', 7.3]
    ]
    tendance = calculer_tendance(historique)
    print(f"Tendance sur 4 mois: {tendance}")
