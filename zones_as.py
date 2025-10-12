class Zones_as:
    def __init__(self, valeur, famille, x, y):
        self.cartes = []
        self.valeur = valeur  # Pour compatibilité
        self.famille = famille  # None au départ, défini par la première carte
        self.x = x
        self.y = y
        self.rect_id = None
        self.text_id = None

    def peut_ajouter(self, carte):
        if not self.cartes:
            return carte.valeur == 1  # As sur zone vide
        top = self.cartes[-1]
        return carte.famille == top.famille and carte.valeur == top.valeur + 1

    def ajouter_carte(self, carte):
        if not self.cartes:
            self.famille = carte.famille
        self.cartes.append(carte)