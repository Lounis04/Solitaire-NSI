from cartes import jeu

class Zones_as:
    def __init__(self, valeur, famille, x, y):
        self.valeur = valeur   # valeur de la dernière carte posée (0 si vide)
        self.famille = famille # famille des cartes posées
        self.x = x
        self.y = y
        self.photo = None
        self.text_id = None

    def changement(self, idx_carte):
        carte = jeu[idx_carte]

        if self.valeur == 0:
            # zone vide -> accepter uniquement un As
            if carte.valeur == 1:
                self.valeur = 1
                self.famille = carte.famille
                return True
            return False

        # sinon -> vérifier famille et valeur suivante
        if carte.famille == self.famille and carte.valeur == self.valeur + 1:
            self.valeur += 1
            return True

        return False
