import time
import tkinter as tk
from typing import Optional

# Variables globales pour les statistiques
temps_debut: Optional[float] = None
compteur_coups: int = 0


def initialiser_stats() -> None:
    """
    Initialise les statistiques au début d'une partie.
    Il n'y a pas d'entrée.
    Il n'y a pas de sortie (None).
    """
    global temps_debut, compteur_coups
    temps_debut = time.time()
    compteur_coups = 0


def incrementer_coups() -> None:
    """
    Incrémente le compteur de coups de 1.
    Il n'y a pas d'entrée.
    Il n'y a pas de sortie (None).
    """
    global compteur_coups
    compteur_coups += 1


def mettre_a_jour_timer(canvas: tk.Canvas, label_timer: tk.Label) -> None:
    """
    Met à jour le timer affiché chaque seconde.
    Les entrées sont le canvas du jeu et le label affichant le timer.
    Il n'y a pas de sortie (None).
    """
    global temps_debut
    
    if temps_debut is not None and not hasattr(canvas, 'partie_gagnee'):
        temps_ecoule: int = int(time.time() - temps_debut)
        minutes: int = temps_ecoule // 60
        secondes: int = temps_ecoule % 60
        label_timer.config(text=f"Temps: {minutes:02d}:{secondes:02d}")
        
        # Rappeler cette fonction après 1 seconde
        canvas.after(1000, lambda: mettre_a_jour_timer(canvas, label_timer))


def mettre_a_jour_interface(canvas: tk.Canvas) -> None:
    """
    Met à jour l'affichage du compteur de coups dans l'interface.
    Les entrées sont le canvas contenant le label des coups.
    Il n'y a pas de sortie (None).
    """
    if hasattr(canvas, 'label_coups'):
        canvas.label_coups.config(text=f"Coups: {compteur_coups}")


def reset_stats() -> None:
    """
    Réinitialise toutes les statistiques pour une nouvelle partie.
    Il n'y a pas d'entrée.
    Il n'y a pas de sortie (None).
    """
    global temps_debut, compteur_coups
    temps_debut = None
    compteur_coups = 0