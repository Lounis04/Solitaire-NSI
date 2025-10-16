import tkinter as tk
from piles import Pile
from statistiques import incrementer_coups, mettre_a_jour_interface
from jeu import verifier_victoire

# Variables globales pour la sélection
carte_en_main = None
pile_origine = None


def reset_selection():
    """Réinitialise la sélection de carte"""
    global carte_en_main, pile_origine
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
                clic_pile(pile, canvas)
                return
        
        # Vérifie si la carte est dans une zone As
        for zone in canvas.zones_as:
            if carte in zone.cartes and zone.cartes[-1] == carte:
                clic_zone_as(zone, canvas)
                return
    
    # Si carte retournée, on ne peut pas la prendre
    if carte.retour:
        return
    
    # Trouve la pile contenant cette carte
    pile_source = None
    
    for pile in canvas.piles:
        idx = pile.trouver_index_carte(carte)
        if idx != -1:
            pile_source = pile
            break
    
    # Si pas dans les piles, vérifier les zones as
    if pile_source is None:
        for zone in canvas.zones_as:
            if carte in zone.cartes:
                if zone.cartes[-1] != carte:
                    return
                pile_source = zone
                break
    
    # Vérifier la zone de pioche (défausse)
    if pile_source is None and canvas.zone_pioche:
        if carte in canvas.zone_pioche.cartes:
            if canvas.zone_pioche.cartes[-1] != carte:
                return
            pile_source = canvas.zone_pioche
    
    if pile_source is None:
        return
    
    # Supprime l'ancienne sélection
    if carte_en_main is not None:
        if hasattr(carte_en_main, "selection_rect") and carte_en_main.selection_rect:
            canvas.delete(carte_en_main.selection_rect)
            carte_en_main.selection_rect = None
    
    # Sélectionne la carte
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
    from pioche import afficher_defausse
    
    if carte_en_main is None:
        return
    
    if not pile.peut_ajouter(carte_en_main):
        return
    
    # Incrémenter le compteur de coups
    incrementer_coups()
    mettre_a_jour_interface(canvas)
    
    cartes_a_deplacer = [carte_en_main]
    
    if isinstance(pile_origine, Pile):
        idx = pile_origine.trouver_index_carte(carte_en_main)
        if idx != -1:
            cartes_a_deplacer = pile_origine.cartes[idx:]
            pile_origine.cartes = pile_origine.cartes[:idx]
            
            top = pile_origine.carte_du_haut()
            if top and top.retour:
                top.retour = False
                top.affichage_retournement_cartes()
                img = tk.PhotoImage(file=top.image)
                top.photo = img
                canvas.images.append(img)
                canvas.itemconfig(top.canvas_id, image=img)
            
            if pile_origine == canvas.zone_pioche:
                afficher_defausse(canvas)
    else:
        pile_origine.cartes.remove(carte_en_main)
    
    for carte in cartes_a_deplacer:
        pile.ajouter_carte(carte)
        x, y = pile.coord_carte(pile.cartes.index(carte))
        canvas.coords(carte.canvas_id, x, y)
        canvas.tag_raise(carte.canvas_id)
    
    if carte_en_main.selection_rect:
        canvas.delete(carte_en_main.selection_rect)
        carte_en_main.selection_rect = None
    
    carte_en_main = None
    pile_origine = None
    
    verifier_victoire(canvas)


def clic_zone_as(zone, canvas):
    """Gère le clic sur une zone As pour y déposer une carte"""
    global carte_en_main, pile_origine
    from pioche import afficher_defausse
    
    if carte_en_main is None:
        return
    
    if isinstance(pile_origine, Pile):
        idx = pile_origine.trouver_index_carte(carte_en_main)
        if idx != len(pile_origine.cartes) - 1:
            return
    
    if not zone.peut_ajouter(carte_en_main):
        return
    
    # Incrémenter le compteur de coups
    incrementer_coups()
    mettre_a_jour_interface(canvas)
    
    if isinstance(pile_origine, Pile):
        pile_origine.enlever_carte(carte_en_main)
        top = pile_origine.carte_du_haut()
        if top and top.retour:
            top.retour = False
            top.affichage_retournement_cartes()
            img = tk.PhotoImage(file=top.image)
            top.photo = img
            canvas.images.append(img)
            canvas.itemconfig(top.canvas_id, image=img)
        
        if pile_origine == canvas.zone_pioche:
            afficher_defausse(canvas)
    else:
        pile_origine.cartes.remove(carte_en_main)
    
    zone.ajouter_carte(carte_en_main)
    canvas.coords(carte_en_main.canvas_id, zone.x, zone.y)
    canvas.tag_raise(carte_en_main.canvas_id)
    
    if carte_en_main.selection_rect:
        canvas.delete(carte_en_main.selection_rect)
        carte_en_main.selection_rect = None
    
    carte_en_main = None
    pile_origine = None
    
    verifier_victoire(canvas)