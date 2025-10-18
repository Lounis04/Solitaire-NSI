import os
import tkinter as tk
from cartes import Cartes

def creer_jeu() -> list[Cartes]:
    """Crée le jeu 52 cartes.Il n'y a pas d'entrée.La sortie est une liste contenant les 52 cartes du jeu."""
    jeu: list[Cartes] = []
    valeurs: list[str] = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
    familles: list[str] = ["coeur","carreau","trefle","pique"]
    noms: list[str] = ["As","2","3","4","5","6","7","8","9","10","Valet","Dame","Roi"]
    dossier_cartes: str = "cartes"

    for famille in familles:
        for valeur, nom in zip(valeurs, noms):
            couleur: str = "Rouge" if famille in ("coeur","carreau") else "Noir"
            chemin_image: str = os.path.join(dossier_cartes, f"{valeur}_{famille}.gif")
            carte: Cartes = Cartes(nom=nom, famille=famille, valeur=int(valeur), couleur=couleur, image=chemin_image)
            jeu.append(carte)
    return jeu


def verifier_victoire(canvas: tk.Canvas) -> None:
    """Vérifie si toutes les cartes sont dans les zones As (victoire).Les entrées sont le canvas contenant les zones As.Il n'y a pas de sortie (None), mais affiche un message de victoire si gagné."""
    import time
    from statistiques import temps_debut, compteur_coups
    
    total_cartes: int = sum(len(zone.cartes) for zone in canvas.zones_as)
    
    if total_cartes == 52:
        canvas.partie_gagnee = True
        temps_final: int = int(time.time() - temps_debut)
        minutes: int = temps_final // 60
        secondes: int = temps_final % 60
        
        # Afficher un message de victoire
        canvas.create_rectangle(canvas.winfo_width()//2 - 200, canvas.winfo_height()//2 - 100,canvas.winfo_width()//2 + 200, canvas.winfo_height()//2 + 100,fill="gold", outline="black", width=3)
        canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2 - 40,text="VICTOIRE !", font=("Arial", 24, "bold"), fill="green")
        canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2,text=f"Temps: {minutes:02d}:{secondes:02d}", font=("Arial", 16), fill="black")
        canvas.create_text(canvas.winfo_width()//2, canvas.winfo_height()//2 + 30,text=f"Coups: {compteur_coups}", font=("Arial", 16), fill="black")