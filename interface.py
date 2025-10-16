
import tkinter as tk
import random
from piles import Pile
from zones_as import Zones_as
from jeu import creer_jeu
from statistiques import initialiser_stats, mettre_a_jour_timer, reset_stats
from gestionnaire_clics import clic_pile, clic_zone_as, reset_selection
from pioche import piocher_cartes
from utils import mise_en_place, afficher_pioche


def lancement():
    root = tk.Tk()
    root.title("Solitaire")
    root.configure(bg="green")

    largeur, hauteur = root.winfo_screenwidth(), root.winfo_screenheight()
    canvas = tk.Canvas(root, width=largeur, height=hauteur, bg="green",highlightthickness=0)
    canvas.pack()

    # Initialiser les statistiques
    initialiser_stats()

    # Stocke les images pour éviter le garbage collection
    canvas.images = []
    canvas.zones_as = []
    canvas.piles = []

    # Calcul des dimensions adaptatives
    w_zone = int(largeur * 0.068)
    h_zone = int(w_zone * 1.4)
    espacement = int(largeur * 0.012)
    decalage_y = int(hauteur * 0.03)
    y_zone = int(hauteur * 0.05)
    y_piles = y_zone + h_zone + int(hauteur * 0.05)
    largeur_totale_piles = 7 * w_zone + 6 * espacement
    x_depart = int((largeur - largeur_totale_piles) / 2)

    # Zones As
    x_zone = x_depart
    for i in range(4):
        x = x_zone + i * (w_zone + espacement)
        rect_id = canvas.create_rectangle(x, y_zone, x + w_zone, y_zone + h_zone,outline="white", dash=(5,3), width=2, fill="green")
        zone_obj = Zones_as(valeur=0, famille=None, x=x, y=y_zone)
        zone_obj.rect_id = rect_id
        canvas.zones_as.append(zone_obj)
        canvas.tag_bind(rect_id, "<Button-1>",lambda e, z=zone_obj: clic_zone_as(z, canvas))

    # Zone Pioche
    x_pioche = x_depart + 5 * (w_zone + espacement)
    canvas.pioche = Pile(x_pioche, y_zone, decalage_y)
    rect_pioche = canvas.create_rectangle(x_pioche, y_zone, x_pioche + w_zone, y_zone + h_zone, outline="white", dash=(5,3), width=2, fill="green")
    font_size = max(10, int(hauteur * 0.018))
    canvas.create_text(x_pioche + w_zone//2, y_zone + h_zone//2, text="Pioche", fill="white", font=("Arial", font_size))

    # Zone Défausse
    x_zone_pioche = x_pioche + w_zone + espacement
    canvas.zone_pioche = Pile(x_zone_pioche, y_zone, decalage_y)
    largeur_defausse = w_zone + 50
    rect_zone_pioche = canvas.create_rectangle(x_zone_pioche, y_zone, x_zone_pioche + largeur_defausse, y_zone + h_zone,outline="white", dash=(5,3), width=2, fill="green"
    )
    canvas.create_text(x_zone_pioche + largeur_defausse//2, y_zone + h_zone//2,text="Défausse", fill="white", font=("Arial", font_size))

    # Piles (7 colonnes)
    for i in range(7):
        pile = Pile(x_depart + i * (w_zone + espacement), y_piles, decalage_y)
        canvas.piles.append(pile)
        rect_id = canvas.create_rectangle(pile.x, pile.y, pile.x + w_zone, pile.y + h_zone, outline="white", dash=(3,3), width=2, fill="green")
        pile.rect_id = rect_id
        canvas.tag_bind(rect_id, "<Button-1>",lambda e, p=pile: clic_pile(p, canvas))

    # Labels pour le timer et les coups
    x_btn = int(largeur * 0.90)
    y_btn_start = int(hauteur * 0.4)
    espacement_btn = int(hauteur * 0.08)
    
    label_timer = tk.Label(root, text="Temps: 00:00", bg="green", fg="white",font=("Arial", 16, "bold"))
    label_timer.place(x=30, y=30)
    
    label_coups = tk.Label(root, text="Coups: 0", bg="green", fg="white",font=("Arial", 16, "bold"))
    label_coups.place(x=30, y=70)
    
    canvas.label_coups = label_coups
    mettre_a_jour_timer(canvas, label_timer)
    
    # Boutons
    btn_piocher = tk.Button(root, text="Piocher 3 cartes", bg="orange", fg="white",font=("Arial", 12), width=15, height=2,command=lambda: piocher_cartes(canvas))
    btn_piocher.place(x=x_btn, y=y_btn_start, anchor="center")
    
    btn_perdant = tk.Button(root, text="S'avouer perdant", bg="red", fg="white",font=("Arial", 12), width=15, height=2,command=root.destroy)
    btn_perdant.place(x=x_btn, y=y_btn_start + espacement_btn, anchor="center")
    
    btn_nouvelle = tk.Button(root, text="Nouvelle partie", bg="green", fg="white",font=("Arial", 12), width=15, height=2,command=lambda: nouvelle_partie(canvas, root))
    btn_nouvelle.place(x=x_btn, y=y_btn_start + 2 * espacement_btn, anchor="center")

    # Création et distribution
    jeu = creer_jeu()
    random.shuffle(jeu)
    cartes_non_distribuees = jeu[28:]
    
    mise_en_place(canvas, jeu)
    afficher_pioche(canvas, cartes_non_distribuees)

    root.mainloop()


def nouvelle_partie(canvas, root):
    """Relance une nouvelle partie"""
    canvas.delete("all")
    canvas.images = []
    canvas.zones_as = []
    canvas.piles = []
    
    reset_selection()
    reset_stats()
    
    root.destroy()
    lancement()