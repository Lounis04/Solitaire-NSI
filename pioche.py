import tkinter as tk
from utils import redimensionner_image

def piocher_cartes(canvas: tk.Canvas) -> None:
    """Pioche 3 cartes du paquet et les affiche dans la zone défausse.Les entrées sont le canvas contenant la pioche et la défausse.Il n'y a pas de sortie (None)."""
    if len(canvas.pioche.cartes) == 0:
        if len(canvas.zone_pioche.cartes) == 0:
            return
        recycler_defausse(canvas)
    
    cartes_disponibles: int = len(canvas.pioche.cartes)
    nombre_a_piocher: int = min(3, cartes_disponibles)
    
    for _ in range(nombre_a_piocher):
        carte = canvas.pioche.cartes.pop()
        carte.retour = False
        carte.affichage_retournement_cartes()
        
        img: tk.PhotoImage = redimensionner_image(carte.image, canvas.carte_largeur, canvas.carte_hauteur)
        carte.photo = img
        canvas.images.append(img)
        canvas.itemconfig(carte.canvas_id, image=img)
        
        canvas.zone_pioche.ajouter_carte(carte)
    
    if nombre_a_piocher < 3 and len(canvas.pioche.cartes) == 0 and len(canvas.zone_pioche.cartes) < 3:
        cartes_a_garder = canvas.zone_pioche.cartes[-nombre_a_piocher:]
        cartes_a_recycler = canvas.zone_pioche.cartes[:-nombre_a_piocher]
        
        if len(cartes_a_recycler) > 0:
            canvas.zone_pioche.cartes = cartes_a_garder
            
            for carte in reversed(cartes_a_recycler):
                carte.retour = True
                carte.affichage_retournement_cartes()
                img: tk.PhotoImage = redimensionner_image(carte.image, canvas.carte_largeur, canvas.carte_hauteur)
                carte.photo = img
                canvas.images.append(img)
                canvas.itemconfig(carte.canvas_id, image=img)
                
                canvas.coords(carte.canvas_id, canvas.pioche.x, canvas.pioche.y)
                canvas.pioche.ajouter_carte(carte)
            
            cartes_manquantes: int = 3 - nombre_a_piocher
            for _ in range(min(cartes_manquantes, len(canvas.pioche.cartes))):
                carte = canvas.pioche.cartes.pop()
                carte.retour = False
                carte.affichage_retournement_cartes()
                
                img: tk.PhotoImage = redimensionner_image(carte.image, canvas.carte_largeur, canvas.carte_hauteur)
                carte.photo = img
                canvas.images.append(img)
                canvas.itemconfig(carte.canvas_id, image=img)
                
                canvas.zone_pioche.ajouter_carte(carte)
    
    afficher_defausse(canvas)


def recycler_defausse(canvas: tk.Canvas) -> None:
    """Remet toutes les cartes de la défausse dans la pioche, face cachée.Les entrées sont le canvas contenant la pioche et la défausse.Il n'y a pas de sortie (None)."""
    if len(canvas.zone_pioche.cartes) == 0:
        return
    
    while len(canvas.zone_pioche.cartes) > 0:
        carte = canvas.zone_pioche.cartes.pop()
        carte.retour = True
        carte.affichage_retournement_cartes()
        
        img: tk.PhotoImage = redimensionner_image(carte.image, canvas.carte_largeur, canvas.carte_hauteur)
        carte.photo = img
        canvas.images.append(img)
        canvas.itemconfig(carte.canvas_id, image=img)
        
        canvas.coords(carte.canvas_id, canvas.pioche.x, canvas.pioche.y)
        canvas.pioche.ajouter_carte(carte)


def afficher_defausse(canvas: tk.Canvas) -> None:
    """Affiche les cartes de la défausse avec les 3 dernières visibles en cascade.Les entrées sont le canvas contenant la zone défausse.Il n'y a pas de sortie (None)."""
    from gestionnaire_clics import clic_carte
    
    nb_cartes: int = len(canvas.zone_pioche.cartes)
    
    if nb_cartes == 0:
        return
    
    for i, carte in enumerate(canvas.zone_pioche.cartes):
        if i >= nb_cartes - 3:
            position_cascade: int = i - (nb_cartes - 3)
            decalage: int = position_cascade * 25
            x: int = canvas.zone_pioche.x + decalage
            y: int = canvas.zone_pioche.y
        else:
            x: int = canvas.zone_pioche.x
            y: int = canvas.zone_pioche.y
        
        canvas.coords(carte.canvas_id, x, y)
        canvas.tag_raise(carte.canvas_id)
        canvas.tag_unbind(carte.canvas_id, "<Button-1>")
        
        if i == nb_cartes - 1:
            canvas.tag_bind(carte.canvas_id, "<Button-1>",
                          lambda e, c=carte: clic_carte(c, canvas))