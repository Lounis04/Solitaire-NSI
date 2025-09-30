import tkinter as tk

visuel = tk.Tk()
visuel.title("Solitaire")
visuel.configure(bg="green")

#Prise d'info sur la taille de l'écran de l'utulisateur#

largeur_ecran = visuel.winfo_screenwidth()
longueur_ecran = visuel.winfo_screenheight()

#Création de l'instance espace_cartes qui correspond aux rectangles en pointillés blancs#

espace_cartes = tk.Canvas(visuel, width =  largeur_ecran, height = longueur_ecran, bg="green", highlightthickness=0)
espace_cartes.pack()

#Définition des coordonnées des rectangles#

espace_cartes.create_rectangle(largeur_ecran * 0.01 ,longueur_ecran * 0.01, largeur_ecran * 0.1, longueur_ecran * 0.22, outline="white", dash=(5, 3), width=2)
espace_cartes.create_rectangle(largeur_ecran * 0.01 ,longueur_ecran * 0.23, largeur_ecran * 0.1, longueur_ecran * 0.45, outline="white", dash=(5, 3), width=2)
espace_cartes.create_rectangle(largeur_ecran * 0.01 ,longueur_ecran * 0.46, largeur_ecran * 0.1, longueur_ecran * 0.68, outline="white", dash=(5, 3), width=2)
espace_cartes.create_rectangle(largeur_ecran * 0.01 ,longueur_ecran * 0.69, largeur_ecran * 0.1, longueur_ecran * 0.91, outline="white", dash=(5, 3), width=2)

espace_cartes.create_rectangle(largeur_ecran*0.9, longueur_ecran*0.23,largeur_ecran*0.99, longueur_ecran*0.45,outline="white", dash=(5,3), width=2)

#Lancement du programme#

visuel.mainloop()