import os 

class Cartes:
    """La couleur de la carte correspond à la famille et la valeur à As..Roi"""
    def __init__(self, nom, famille, valeur, couleur, image=None):
        self.retour = False
        self.nom = nom
        self.famille = famille
        self.valeur = valeur
        self.couleur = couleur
        self.image = image
        self.canvas_id = None
        self.selection_rect = None
        self.photo = None

    def __repr__(self):
        return f"{self.nom} de {self.famille} ({self.valeur})"

    def retournement_cartes(self):
        """Méthode qui permet de retourner une carte"""
        self.retour = True

    def affichage_retournement_cartes(self, dossier_cartes="cartes"):
        """Change l'image si la carte est retournée"""
        if not self.retour:
            chemin = os.path.join(dossier_cartes, f"{self.valeur}_{self.famille}.gif")
            self.image = chemin
        else:
            self.image = os.path.join(dossier_cartes, "carte_retour.png")