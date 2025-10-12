import tkinter as tk
import random
import os
from cartes import Cartes
from piles import Pile
import random
from zones_as import Zones_as

# ==================== CRÉATION DU JEU ====================

def creer_jeu():
    jeu = []
    valeurs = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
    familles = ["coeur","carreau","trefle","pique"]
    noms = ["As","2","3","4","5","6","7","8","9","10","Valet","Dame","Roi"]
    dossier_cartes = "cartes"

    for famille in familles:
        for valeur, nom in zip(valeurs, noms):
            couleur = "Rouge" if famille in ("coeur","carreau") else "Noir"
            chemin_image = os.path.join(dossier_cartes, f"{valeur}_{famille}.gif")
            carte = Cartes(nom=nom, famille=famille, valeur=int(valeur), 
                          couleur=couleur, image=chemin_image)
            jeu.append(carte)
    
    return jeu


# ==================== GESTION DES CLICS ====================

carte_en_main = None
pile_origine = None

def clic_carte(carte, canvas):
    """Gère le clic sur une carte"""
    global carte_en_main, pile_origine
    
    # Si on clique sur la carte déjà sélectionnée, on la désélectionne
    if carte_en_main is not None and carte_en_main == carte:
        if hasattr(carte_en_main, "selection_rect") and carte_en_main.selection_rect:
            canvas.delete(carte_en_main.selection_rect)
            carte_en_main.selection_rect = None
        carte_en_main = None
        pile_origine = None
        return
    
    # Si on a déjà une carte en main, essayer de la déposer sur cette carte
    if carte_en_main is not None and carte_en_main != carte:
        # Trouve la pile contenant la carte de destination
        for pile in canvas.piles:
            if carte in pile.cartes and pile.carte_du_haut() == carte:
                # Essaie de déposer sur cette pile
                clic_pile(pile, canvas)
                return
        
        # Vérifie si la carte est dans une zone As
        for zone in canvas.zones_as:
            if carte in zone.cartes and zone.cartes[-1] == carte:
                # Essaie de déposer sur cette zone As
                clic_zone_as(zone, canvas)
                return
        
        # Si pas déposé, on continue pour sélectionner la nouvelle carte
    
    # Si carte retournée, on ne peut pas la prendre
    if carte.retour:
        return
    
    # Trouve la pile contenant cette carte
    pile_source = None
    index_carte = -1
    
    for pile in canvas.piles:
        idx = pile.trouver_index_carte(carte)
        if idx != -1:
            pile_source = pile
            index_carte = idx
            break
    
    # Si pas dans les piles, vérifier les zones as
    if pile_source is None:
        for zone in canvas.zones_as:
            if carte in zone.cartes:
                # On ne peut prendre que la carte du dessus d'une zone as
                if zone.cartes[-1] != carte:
                    return
                pile_source = zone
                break
    
    if pile_source is None:
        return
    
    # Supprime l'ancienne sélection
    if carte_en_main is not None:
        if hasattr(carte_en_main, "selection_rect") and carte_en_main.selection_rect:
            canvas.delete(carte_en_main.selection_rect)
            carte_en_main.selection_rect = None
    
    # Sélectionne la carte (et toutes celles au-dessus si dans une pile)
    carte_en_main = carte
    pile_origine = pile_source
    
    # Crée un rectangle de sélection
    x, y = canvas.coords(carte.canvas_id)[:2]
    w, h = carte.photo.width(), carte.photo.height()
    rect = canvas.create_rectangle(x, y, x + w, y + h, outline="yellow", width=3)
    carte.selection_rect = rect


def clic_pile(pile, canvas):
    """Gère le clic sur une pile pour y déposer une carte"""
    global carte_en_main, pile_origine
    
    if carte_en_main is None:
        return
    
    # Vérifie si on peut ajouter la carte
    if not pile.peut_ajouter(carte_en_main):
        return
    
    # Si la carte vient d'une pile, on déplace aussi toutes les cartes au-dessus
    cartes_a_deplacer = [carte_en_main]
    
    if isinstance(pile_origine, Pile):
        idx = pile_origine.trouver_index_carte(carte_en_main)
        if idx != -1:
            # Prend toutes les cartes à partir de celle-ci
            cartes_a_deplacer = pile_origine.cartes[idx:]
            # Les enlève de la pile origine
            pile_origine.cartes = pile_origine.cartes[:idx]
            
            # Retourne la nouvelle carte du dessus si elle existe
            top = pile_origine.carte_du_haut()
            if top and top.retour:
                top.retour = False
                top.affichage_retournement_cartes()
                img = tk.PhotoImage(file=top.image)
                top.photo = img
                canvas.images.append(img)
                canvas.itemconfig(top.canvas_id, image=img)
    else:
        # Vient d'une zone as
        pile_origine.cartes.remove(carte_en_main)
    
    # Ajoute les cartes à la nouvelle pile
    for carte in cartes_a_deplacer:
        pile.ajouter_carte(carte)
        x, y = pile.coord_carte(pile.cartes.index(carte))
        canvas.coords(carte.canvas_id, x, y)
        canvas.tag_raise(carte.canvas_id)
    
    # Supprime la sélection
    if carte_en_main.selection_rect:
        canvas.delete(carte_en_main.selection_rect)
        carte_en_main.selection_rect = None
    
    carte_en_main = None
    pile_origine = None


def clic_zone_as(zone, canvas):
    """Gère le clic sur une zone As pour y déposer une carte"""
    global carte_en_main, pile_origine
    
    if carte_en_main is None:
        return
    
    # On ne peut déposer qu'une seule carte sur les zones as
    if isinstance(pile_origine, Pile):
        idx = pile_origine.trouver_index_carte(carte_en_main)
        # La carte doit être la dernière de la pile
        if idx != len(pile_origine.cartes) - 1:
            return
    
    # Vérifie si on peut ajouter la carte
    if not zone.peut_ajouter(carte_en_main):
        return
    
    # Enlève de la pile/zone origine
    if isinstance(pile_origine, Pile):
        pile_origine.enlever_carte(carte_en_main)
        # Retourne la nouvelle carte du dessus
        top = pile_origine.carte_du_haut()
        if top and top.retour:
            top.retour = False
            top.affichage_retournement_cartes()
            img = tk.PhotoImage(file=top.image)
            top.photo = img
            canvas.images.append(img)
            canvas.itemconfig(top.canvas_id, image=img)
    else:
        pile_origine.cartes.remove(carte_en_main)
    
    # Ajoute à la zone
    zone.ajouter_carte(carte_en_main)
    canvas.coords(carte_en_main.canvas_id, zone.x, zone.y)
    canvas.tag_raise(carte_en_main.canvas_id)
    
    # Met à jour le texte de la zone
    if zone.text_id:
        canvas.itemconfig(zone.text_id, text=f"{zone.famille} ({len(zone.cartes)})")
    
    # Supprime la sélection
    if carte_en_main.selection_rect:
        canvas.delete(carte_en_main.selection_rect)
        carte_en_main.selection_rect = None
    
    carte_en_main = None
    pile_origine = None


# ==================== MISE EN PLACE ====================

def mise_en_place(canvas, jeu):
    """Place les 7 colonnes du Solitaire"""
    index = 0
    
    for col in range(7):
        pile = canvas.piles[col]
        for ligne in range(col + 1):
            if index >= len(jeu):
                break
                
            carte = jeu[index]
            index += 1
            
            # Retourne les cartes sauf la dernière de chaque colonne
            if ligne < col:
                carte.retournement_cartes()
                carte.affichage_retournement_cartes()
            
            # Charge l'image
            img = tk.PhotoImage(file=carte.image)
            carte.photo = img
            canvas.images.append(img)
            
            # Place la carte
            x, y = pile.coord_carte(ligne)
            image_id = canvas.create_image(x, y, image=img, anchor="nw")
            carte.canvas_id = image_id
            
            # Ajoute la carte à la pile
            pile.ajouter_carte(carte)
            
            # Bind le clic
            canvas.tag_bind(image_id, "<Button-1>",lambda e, c=carte: clic_carte(c, canvas))


# ==================== LANCEMENT ====================

def lancement():
    root = tk.Tk()
    root.title("Solitaire")
    root.configure(bg="green")

    largeur, hauteur = root.winfo_screenwidth(), root.winfo_screenheight()
    canvas = tk.Canvas(root, width=largeur, height=hauteur, bg="green",highlightthickness=0)
    canvas.pack()

    # Stocke les images pour éviter le garbage collection
    canvas.images = []
    canvas.zones_as = []
    canvas.piles = []

    # --- Zones As (horizontal en haut) ---
    w_zone, h_zone = 130, 180
    x_zone = largeur * 0.15
    y_zone = hauteur * 0.03
    espacement = 20

    for i in range(4):
        x = x_zone + i * (w_zone + espacement)
        rect_id = canvas.create_rectangle(x, y_zone, x + w_zone, y_zone + h_zone,outline="white", dash=(5,3), width=2, fill="green")
        zone_obj = Zones_as(valeur=0, famille=None, x=x, y=y_zone)
        zone_obj.rect_id = rect_id
        text_id = canvas.create_text(x + w_zone//2, y_zone + h_zone//2, text="As", fill="white", font=("Arial", 16))
        zone_obj.text_id = text_id
        canvas.zones_as.append(zone_obj)
        canvas.tag_bind(rect_id, "<Button-1>", 
                       lambda e, z=zone_obj: clic_zone_as(z, canvas))

    # --- Zone Pioche (au-dessus de la 7e colonne) ---
    x_pioche = x_depart = largeur * 0.15
    x_pioche += 6 * (largeur * 0.1)  # Position de la 7e colonne
    rect_pioche = canvas.create_rectangle(x_pioche, y_zone, x_pioche + w_zone, y_zone + h_zone, outline="white",dash=(5,3), width=2, fill="green")
    canvas.create_text(x_pioche + w_zone//2, y_zone + h_zone//2, text="Pioche", fill="white", font=("Arial", 16))

    # --- Piles (7 colonnes principales) ---
    x_depart = largeur * 0.15
    y_depart = y_zone + h_zone + 40
    decalage_x = largeur * 0.1

    for i in range(7):
        pile = Pile(x_depart + i * decalage_x, y_depart)
        canvas.piles.append(pile)
        rect_id = canvas.create_rectangle(pile.x, pile.y, pile.x + w_zone, pile.y + h_zone, outline="white",dash=(3,3), width=2, fill="green")
        pile.rect_id = rect_id
        canvas.tag_bind(rect_id, "<Button-1>", 
                       lambda e, p=pile: clic_pile(p, canvas))

    # --- Boutons ---
    x_btn = largeur * 0.90
    y_btn_start = hauteur * 0.4
    
    btn_piocher = tk.Button(root, text="Piocher 3 cartes", bg="orange", fg="white",font=("Arial", 12), width=15, height=2)
    btn_piocher.place(x=x_btn, y=y_btn_start, anchor="center")
    
    btn_perdant = tk.Button(root, text="S'avouer perdant", bg="red", fg="white",font=("Arial", 12), width=15, height=2,command=root.destroy)
    btn_perdant.place(x=x_btn, y=y_btn_start + 80, anchor="center")
    
    btn_nouvelle = tk.Button(root, text="Nouvelle partie", bg="green", fg="white",font=("Arial", 12), width=15, height=2,command=lambda: nouvelle_partie(canvas, root))
    btn_nouvelle.place(x=x_btn, y=y_btn_start + 160, anchor="center")

    # Création et mélange du jeu
    jeu = creer_jeu()
    random.shuffle(jeu)
    
    # Mise en place initiale
    mise_en_place(canvas, jeu)

    root.mainloop()


def nouvelle_partie(canvas, root):
    """Relance une nouvelle partie"""
    # Efface tout
    canvas.delete("all")
    
    # Réinitialise
    canvas.images = []
    canvas.zones_as = []
    canvas.piles = []
    
    global carte_en_main, pile_origine
    carte_en_main = None
    pile_origine = None
    
    # Recrée l'interface
    root.destroy()
    lancement()


if __name__ == "__main__":
    lancement()