class Pile:
    def __init__(self, x, y):
        self.cartes = []
        self.x = x
        self.y = y
        self.rect_id = None

    def peut_ajouter(self, carte):
        if not self.cartes:
            return carte.valeur == 13  # Roi sur pile vide
        top = self.cartes[-1]
        return carte.couleur != top.couleur and carte.valeur == top.valeur - 1

    def ajouter_carte(self, carte):
        self.cartes.append(carte)

    def enlever_carte(self, carte):
        if carte in self.cartes:
            self.cartes.remove(carte)

    def carte_du_haut(self):
        if self.cartes:
            return self.cartes[-1]
        return None

    def coord_carte(self, index):
        """Retourne les coordonnées pour la carte à l'index donné"""
        decalage_y = 40
        return self.x, self.y + decalage_y * index

    def trouver_index_carte(self, carte):
        """Trouve l'index d'une carte dans la pile"""
        if carte in self.cartes:
            return self.cartes.index(carte)
        return -1