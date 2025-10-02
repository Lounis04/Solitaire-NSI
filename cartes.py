import os

class Cartes():
    "La couleur de la carte correspond à si c'est un trèfle,un coeur,etc.. et sa valeur correspond à si c'est 1,4,roi,etc..."
    def __init__(self,nom,famille,valeur,couleur,image = None):
        self.retour = False
        self.nom = nom
        self.famille = famille
        self.valeur = valeur
        self.couleur = couleur
        self.image = image

    def retournement_cartes(self):
        "Méthode qui permet de retourner une carte"
        self.retour = True

    def affichage_retournement_cartes(self):
        "Méthode qui permet de changer l'image d'une carte à une carte retournée si elle doit etre retournée"
        if self.retour == True:
            self.image = os.path.join(dossier_cartes,"carte_retour.png")


#Liste qui contient toutes les cartes 

jeu = []

#Liste des valeurs,couleurs,noms possibles#

valeurs = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
familles = ["coeur","carreau","trefle","pique"]
noms = ["As","2","3","4","5","6","7","8","9","10","Valet","Dame","Roi"]
couleurs = ["Rouge","Noir"]

#Initialisation des 52 cartes#
dossier_cartes = "cartes"

for famille in familles:
    for valeur, nom in zip(valeurs, noms): #On parallélise les 2 listes qui sont de meme longueur vu que la valeur à le même indice que le nom dans les deux listes#
        if famille == familles[0] or famille == familles[1]:
            couleur = couleurs[0]
        else:
            couleur = couleurs[1]
        chemin_image = os.path.join(dossier_cartes, f"{valeur}_{famille}.gif")
        carte = Cartes(nom=nom, famille = famille, valeur=int(valeur),couleur = couleur, image=chemin_image)
        jeu.append(carte)

#Test des cartes#


#for c in jeu:
    #print(c.nom, c.famille, c.valeur,c.couleur, c.image)

#c = jeu[0]  # la première carte du jeu
#print("Avant retournement :", c.nom, c.famille, c.valeur, c.couleur, c.image)

#c.retournement_cartes()
#c.affichage_retournement_cartes()

#print("Après retournement :", c.nom, c.famille, c.valeur, c.couleur, c.image)
