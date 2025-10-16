import tkinter as tk


def mise_en_place(canvas, jeu):
    """Place les 7 colonnes du Solitaire"""
    from gestionnaire_clics import clic_carte
    
    index = 0
    
    for col in range(7):
        pile = canvas.piles[col]
        for ligne in range(col + 1):              
            carte = jeu[index]
            index += 1
            
            if ligne < col:
                carte.retournement_cartes()
                carte.affichage_retournement_cartes()
            
            img = tk.PhotoImage(file=carte.image)
            carte.photo = img
            canvas.images.append(img)
            
            x, y = pile.coord_carte(ligne)
            image_id = canvas.create_image(x, y, image=img, anchor="nw")
            carte.canvas_id = image_id
            
            pile.ajouter_carte(carte)
            canvas.tag_bind(image_id, "<Button-1>",lambda e, c=carte: clic_carte(c, canvas))


def afficher_pioche(canvas, cartes_non_distribuees):
    """Affiche le paquet de cartes non distribuées (face cachée)"""
    for carte in cartes_non_distribuees:
        carte.retournement_cartes()
        carte.affichage_retournement_cartes()
        
        img = tk.PhotoImage(file=carte.image)
        carte.photo = img
        canvas.images.append(img)
        
        image_id = canvas.create_image(canvas.pioche.x, canvas.pioche.y, image=img, anchor="nw")
        carte.canvas_id = image_id
        
        canvas.pioche.ajouter_carte(carte)
