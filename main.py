import tkinter as tk
import random
from cartes import jeu
from zones_as import Zones_as

carte_en_main = None

def lancement():
    root = tk.Tk()
    root.title("Solitaire")
    root.configure(bg="green")

    largeur, hauteur = root.winfo_screenwidth(), root.winfo_screenheight()
    canvas = tk.Canvas(root, width=largeur, height=hauteur, bg="green", highlightthickness=0)
    canvas.pack()

    # stocke images et zones pour éviter GC
    canvas.images = []
    canvas.zones_as = []
    canvas.selected_rect = None

    # --- Zones As (horizontal en haut) ---
    w_zone, h_zone = 130, 180
    x_zone = largeur * 0.15
    y_zone = hauteur * 0.03
    espacement = 20

    #zone pioche
    w_zonepioche, h_zonepioche = 130, 180
    x_zonepioche = largeur * 0.75
    y_zonepioche = hauteur * 0.03

    for i in range(4):
        x = x_zone + i * (w_zone + espacement)
        rect_id = canvas.create_rectangle(x, y_zone, x + w_zone, y_zone + h_zone,
                                          outline="white", dash=(5,3), width=2, fill="green")
        zone_obj = Zones_as(0, None, x, y_zone)
        zone_obj.rect_id = rect_id
        text_id = canvas.create_text(x + 5, y_zone - 15, anchor="nw", text="vide", fill="white")
        zone_obj.text_id = text_id
        canvas.zones_as.append(zone_obj)
        canvas.tag_bind(rect_id, "<Button-1>", lambda e, idx=i: clic_zone_as(idx, canvas))

    rect_pioche = canvas.create_rectangle(x_zonepioche, y_zonepioche, x_zonepioche + w_zonepioche, y_zonepioche + h_zonepioche, outline="white", dash=(5,3), width=2, fill="green")

    # --- Boutons ---
    x_btn = largeur * 0.945
    for i, (text, color) in enumerate([
        ("S'avouer perdu", "red"),
        ("Piocher 3 cartes", "yellow"),
        ("Relancer la pioche", "yellow")
    ]):
        btn = tk.Button(root, text=text, bg=color, fg="white" if color=="red" else "black")
        btn.place(x=x_btn, y=hauteur*0.5 + i*50, anchor="n")
        if text == "S'avouer perdu":
            btn.config(command=root.destroy)

    # Mélange et mise en place
    random.shuffle(jeu)
    mise_en_place(canvas, jeu, largeur, hauteur, y_offset=y_zone+h_zone+20)

    root.mainloop()

def mise_en_place(canvas, jeu, largeur, hauteur, y_offset=0):
    """Place les 7 colonnes du Solitaire sous les zones As."""
    x_depart = largeur * 0.15
    y_depart = y_offset
    decalage_x = largeur * 0.1
    decalage_y = 40  # fixe pour décalage vertical entre cartes
    index = 0

    for col in range(7):
        for ligne in range(col + 1):
            carte = jeu[index]
            index += 1
            if ligne < col:
                carte.retournement_cartes()
                carte.affichage_retournement_cartes()

            try:
                img = tk.PhotoImage(file=carte.image)
            except Exception as e:
                print(f"Erreur chargement image pour {carte}: {e}")
                img = None

            carte.photo = img
            if img:
                canvas.images.append(img)

            x = x_depart + col * decalage_x
            y = y_depart + ligne * decalage_y
            image_id = canvas.create_image(x, y, image=img, anchor="nw")
            carte.canvas_id = image_id
            canvas.tag_bind(image_id, "<Button-1>", lambda e, idx=index-1: clic_carte(idx, canvas))

def clic_carte(index, canvas):
    global carte_en_main
    carte = jeu[index]
    if getattr(carte, "image", "").endswith("carte_retour.png"):
        return

    if carte_en_main is not None:
        old = jeu[carte_en_main]
        if hasattr(old, "selection_rect") and old.selection_rect:
            try: canvas.delete(old.selection_rect)
            except: pass
            old.selection_rect = None

    carte_en_main = index
    try:
        x, y = canvas.coords(carte.canvas_id)
        w, h = carte.photo.width() if carte.photo else 130, carte.photo.height() if carte.photo else 180
        rect = canvas.create_rectangle(x, y, x+w, y+h, outline="yellow", width=3)
        carte.selection_rect = rect
        canvas.selected_rect = rect
    except Exception:
        pass

def clic_zone_as(i, canvas):
    global carte_en_main
    if carte_en_main is None:
        return

    carte_obj = jeu[carte_en_main]
    zone = canvas.zones_as[i]

    if zone.changement(carte_en_main):
        if hasattr(carte_obj, "canvas_id") and carte_obj.canvas_id:
            try: canvas.delete(carte_obj.canvas_id)
            except: pass
            carte_obj.canvas_id = None
        if hasattr(carte_obj, "selection_rect") and carte_obj.selection_rect:
            try: canvas.delete(carte_obj.selection_rect)
            except: pass
            carte_obj.selection_rect = None

        img = tk.PhotoImage(file=carte_obj.image)
        canvas.images.append(img)
        zone.photo = img
        carte_id = canvas.create_image(zone.x, zone.y, image=img, anchor="nw")
        canvas.tag_bind(carte_id, "<Button-1>", lambda e, idx=i: clic_zone_as(idx, canvas))
        canvas.itemconfig(zone.text_id, text=f"{zone.famille} ({zone.valeur})" if zone.famille else "vide")
        canvas.tag_raise(carte_id)  
        canvas.tag_raise(zone.text_id) 

    carte_en_main = None

if __name__ == "__main__":
    lancement()
