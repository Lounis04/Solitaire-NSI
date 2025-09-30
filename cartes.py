import os

class Cartes():
    "La couleur de la carte correspond à si c'est un trèfle,un coeur,etc.. et sa valeur correspond à si c'est 1,4,roi,etc..."
    def __init__(self,nom,couleur,valeur , image = None):
        self.retour = True
        self.nom = nom
        self.couleur = couleur
        self.valeur = valeur
        self.image = image

#Liste qui contient toutes les cartes 

jeu = []

#Liste des valeurs,couleurs,noms possibles#

valeurs = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
couleurs = ["coeur","carreau","trefle","pique"]
noms = ["As","2","3","4","5","6","7","8","9","10","Valet","Dame","Roi"]

#Initialisation des 52 cartes#
dossier_cartes = "cartes"

for couleur in couleurs:
    for valeur, nom in zip(valeurs, noms): #On parallélise les 2 listes qui sont de meme longueur vu que la valeur à le même indice que le nom dans les deux listes#
        chemin_image = os.path.join(dossier_cartes, f"{valeur}_{couleur}.gif")
        carte = Cartes(nom=nom, couleur=couleur, valeur=int(valeur), image=chemin_image)
        jeu.append(carte)

#Test des cartes#

#for c in jeu:
    #print(c.nom, c.couleur, c.valeur, c.image)