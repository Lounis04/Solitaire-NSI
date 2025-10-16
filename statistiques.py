import time

# Variables globales pour les statistiques
temps_debut = None
compteur_coups = 0


def initialiser_stats():
    """Initialise les statistiques au début d'une partie"""
    global temps_debut, compteur_coups
    temps_debut = time.time()
    compteur_coups = 0


def incrementer_coups():
    """Incrémente le compteur de coups"""
    global compteur_coups
    compteur_coups += 1


def mettre_a_jour_timer(canvas, label_timer):
    """Met à jour le timer chaque seconde"""
    global temps_debut
    
    if temps_debut is not None and not hasattr(canvas, 'partie_gagnee'):
        temps_ecoule = int(time.time() - temps_debut)
        minutes = temps_ecoule // 60
        secondes = temps_ecoule % 60
        label_timer.config(text=f"Temps: {minutes:02d}:{secondes:02d}")
        
        # Rappeler cette fonction après 1 seconde
        canvas.after(1000, lambda: mettre_a_jour_timer(canvas, label_timer))


def mettre_a_jour_interface(canvas):
    """Met à jour l'affichage du compteur de coups"""
    if hasattr(canvas, 'label_coups'):
        canvas.label_coups.config(text=f"Coups: {compteur_coups}")


def reset_stats():
    """Réinitialise toutes les statistiques"""
    global temps_debut, compteur_coups
    temps_debut = None
    compteur_coups = 0