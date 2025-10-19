import tkinter as tk

def redimensionner_image(chemin: str, largeur: int, hauteur: int) -> tk.PhotoImage:
    """Redimensionne une image aux dimensions spécifiées avec tkinter.Les entrées sont le chemin vers l'image, la largeur cible et la hauteur cible.La sortie est un objet PhotoImage redimensionné."""
    try:
        img: tk.PhotoImage = tk.PhotoImage(file=chemin)
        largeur_originale: int = img.width()
        hauteur_originale: int = img.height()
        
        # Calculer les ratios
        ratio_x: float = largeur / largeur_originale
        ratio_y: float = hauteur / hauteur_originale
        
        # Pour les GIF, on privilégie subsample qui fonctionne mieux
        if ratio_x <= 1.0 or ratio_y <= 1.0:
            # Réduction avec subsample
            subsample_x: int = max(1, int(largeur_originale / largeur))
            subsample_y: int = max(1, int(hauteur_originale / hauteur))
            img = img.subsample(subsample_x, subsample_y)
        else:
            # Agrandissement avec zoom (rarement nécessaire)
            zoom_x: int = max(1, int(ratio_x))
            zoom_y: int = max(1, int(ratio_y))
            img = img.zoom(zoom_x, zoom_y)
            
            # Si l'image est trop grande après zoom, réduire
            if img.width() > largeur or img.height() > hauteur:
                subsample_x: int = max(1, int(img.width() / largeur))
                subsample_y: int = max(1, int(img.height() / hauteur))
                img = img.subsample(subsample_x, subsample_y)
        
        return img
    except Exception as e:
        print(f"Erreur lors du chargement de {chemin}: {e}")
        # Créer une image de secours
        img_secours = tk.PhotoImage(width=largeur, height=hauteur)
        return img_secours


def mise_en_place(canvas: tk.Canvas, jeu: list) -> None:
    """Place les 7 colonnes du Solitaire avec leurs cartes initiales.Les entrées sont le canvas du jeu et la liste des cartes à distribuer.Il n'y a pas de sortie (None)."""
    from gestionnaire_clics import clic_carte
    
    index: int = 0
    
    for col in range(7):
        pile = canvas.piles[col]
        for ligne in range(col + 1):              
            carte = jeu[index]
            index += 1
            
            if ligne < col:
                carte.retournement_cartes()
                carte.affichage_retournement_cartes()
            
            # Redimensionner l'image selon les dimensions du canvas
            img: tk.PhotoImage = redimensionner_image(carte.image, canvas.carte_largeur, canvas.carte_hauteur)
            carte.photo = img
            canvas.images.append(img)
            
            x: int
            y: int
            x, y = pile.coord_carte(ligne)
            image_id: int = canvas.create_image(x, y, image=img, anchor="nw")
            carte.canvas_id = image_id
            
            pile.ajouter_carte(carte)
            canvas.tag_bind(image_id, "<Button-1>",lambda e, c=carte: clic_carte(c, canvas))


def afficher_pioche(canvas: tk.Canvas, cartes_non_distribuees: list) -> None:
    """Affiche le paquet de cartes non distribuées (face cachée) dans la zone pioche.Les entrées sont le canvas du jeu et la liste des cartes restantes.Il n'y a pas de sortie (None)."""
    for carte in cartes_non_distribuees:
        carte.retournement_cartes()
        carte.affichage_retournement_cartes()
        
        # Redimensionner l'image selon les dimensions du canvas
        img: tk.PhotoImage = redimensionner_image(carte.image, canvas.carte_largeur, canvas.carte_hauteur)
        carte.photo = img
        canvas.images.append(img)
        
        image_id: int = canvas.create_image(canvas.pioche.x, canvas.pioche.y, image=img, anchor="nw")
        carte.canvas_id = image_id
        
        canvas.pioche.ajouter_carte(carte)