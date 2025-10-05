import os

class Cartes:
    "La couleur de la carte correspond à la famille et la valeur à As..Roi"
    def __init__(self, nom, famille, valeur, couleur, image=None):
        self.retour = False
        self.nom = nom
        self.famille = famille
        self.valeur = valeur
        self.couleur = couleur
        self.image = image
        self.canvas_id = None

    def __repr__(self):
        return f"{self.nom} de {self.famille} ({self.valeur})"

    def retournement_cartes(self):
        "Méthode qui permet de retourner une carte"
        self.retour = True

    def affichage_retournement_cartes(self, dossier_cartes="cartes"):
        "Change l'image si la carte est retournée"
        if self.retour:
            self.image = os.path.join(dossier_cartes, "carte_retour.png")

jeu = []

valeurs = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]
familles = ["coeur","carreau","trefle","pique"]
noms = ["As","2","3","4","5","6","7","8","9","10","Valet","Dame","Roi"]
couleurs = ["Rouge","Noir"]

dossier_cartes = "cartes"

for famille in familles:
    for valeur, nom in zip(valeurs, noms):
        couleur = couleurs[0] if famille in ("coeur","carreau") else couleurs[1]
        chemin_image = os.path.join(dossier_cartes, f"{valeur}_{famille}.gif")
        carte = Cartes(nom=nom, famille=famille, valeur=int(valeur), couleur=couleur, image=chemin_image)
        jeu.append(carte)
