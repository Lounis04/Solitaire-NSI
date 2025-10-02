import tkinter as tk
import random
from cartes import jeu

def lancement():
    visuel = tk.Tk()
    visuel.title("Solitaire")
    visuel.configure(bg="green")

    global largeur_ecran #x
    global longueur_ecran #y
    largeur_ecran = visuel.winfo_screenwidth()
    longueur_ecran = visuel.winfo_screenheight()

    espace_cartes = tk.Canvas(visuel, width =  largeur_ecran, height = longueur_ecran, bg="green", highlightthickness=0)
    espace_cartes.pack()

    espace_cartes.create_rectangle(largeur_ecran * 0.01 ,longueur_ecran * 0.01, largeur_ecran * 0.1, longueur_ecran * 0.22, outline="white", dash=(5, 3), width=2)
    espace_cartes.create_rectangle(largeur_ecran * 0.01 ,longueur_ecran * 0.23, largeur_ecran * 0.1, longueur_ecran * 0.45, outline="white", dash=(5, 3), width=2)
    espace_cartes.create_rectangle(largeur_ecran * 0.01 ,longueur_ecran * 0.46, largeur_ecran * 0.1, longueur_ecran * 0.68, outline="white", dash=(5, 3), width=2)
    espace_cartes.create_rectangle(largeur_ecran * 0.01 ,longueur_ecran * 0.69, largeur_ecran * 0.1, longueur_ecran * 0.91, outline="white", dash=(5, 3), width=2)

    espace_cartes.create_rectangle(largeur_ecran*0.9, longueur_ecran*0.23,largeur_ecran*0.99, longueur_ecran*0.45,outline="white", dash=(5,3), width=2)

    x_btn = largeur_ecran * 0.945   
    y_btn1 = longueur_ecran * 0.5  
    y_btn2 = longueur_ecran * 0.55
    y_btn3 = longueur_ecran * 0.6

    btn_perdu = tk.Button(visuel, text="S'avouer perdu", command=visuel.destroy, bg="red", fg="white")
    btn_perdu.place(x=x_btn, y=y_btn1, anchor="n")

    btn_piocher = tk.Button(visuel, text="Piocher 3 cartes", bg="yellow")
    btn_piocher.place(x=x_btn, y=y_btn2, anchor="n")

    btn_piocher = tk.Button(visuel, text="Relancer la pioche", bg="yellow")
    btn_piocher.place(x=x_btn, y=y_btn3, anchor="n")

    random.shuffle(jeu)

    images = mise_en_place(espace_cartes, jeu, largeur_ecran, longueur_ecran)

    visuel.mainloop()

def mise_en_place(espace_cartes, jeu, largeur_ecran, longueur_ecran):
    """Place les 7 colonnes du Solitaire sur le canvas."""
    images = [] 
    x_depart = largeur_ecran * 0.15
    y_depart = longueur_ecran * 0.01
    decalage_x = largeur_ecran * 0.1
    decalage_y = longueur_ecran * 0.05   
    index = 0  
    for col in range(7):
        for ligne in range(col + 1):
            carte = jeu[index]
            index += 1
            if ligne < col:
                carte.retournement_cartes()
                carte.affichage_retournement_cartes()
            img = tk.PhotoImage(file=carte.image) #Charge l'image en question#
            images.append(img)  
            x = x_depart + col * decalage_x
            y = y_depart + ligne * decalage_y
            espace_cartes.create_image(x, y, image=img, anchor="nw")
    return images

lancement()


