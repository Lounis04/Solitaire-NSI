from cartes import Cartes

class Pile:
    """Représente une pile de cartes dans le jeu de Solitaire"""
    
    def __init__(self, x: int, y: int, decalage_y: int = 40) -> None:
        """Initialise une pile de cartes.Les entrées sont la position x, la position y et le décalage vertical entre les cartes.La sortie est une instance de Pile initialisée."""
        self.cartes: list[Cartes] = []
        self.x: int = x
        self.y: int = y
        self.rect_id: int | None = None
        self.decalage_y: int = decalage_y

    def peut_ajouter(self, carte: Cartes) -> bool:
        """Vérifie si une carte peut être ajoutée à cette pile selon les règles du Solitaire.Les entrées sont la carte à vérifier.La sortie est un booléen : True si la carte peut être ajoutée, False sinon."""
        if not self.cartes:
            return carte.valeur == 13  # Roi sur pile vide
        top: Cartes = self.cartes[-1]
        return carte.couleur != top.couleur and carte.valeur == top.valeur - 1

    def ajouter_carte(self, carte: Cartes) -> None:
        """Ajoute une carte à la pile.Les entrées sont la carte à ajouter.Il n'y a pas de sortie (None)."""
        self.cartes.append(carte)

    def enlever_carte(self, carte: Cartes) -> None:
        """Enlève une carte de la pile.Les entrées sont la carte à enlever.Il n'y a pas de sortie (None)."""
        if carte in self.cartes:
            self.cartes.remove(carte)

    def carte_du_haut(self) -> Cartes | None:
        """Retourne la carte au sommet de la pile.Il n'y a pas d'entrée.La sortie est la carte du haut de la pile, ou None si la pile est vide."""
        if self.cartes:
            return self.cartes[-1]
        return None

    def coord_carte(self, index: int) -> tuple[int, int]:
        """Calcule les coordonnées d'une carte à un index donné dans la pile.Les entrées sont l'index de la carte dans la pile.La sortie est un tuple contenant les coordonnées x et y de la carte."""
        return self.x, self.y + self.decalage_y * index

    def trouver_index_carte(self, carte: Cartes) -> int:
        """Trouve l'index d'une carte dans la pile.Les entrées sont la carte à chercher.La sortie est l'index de la carte dans la pile, ou -1 si elle n'y est pas."""
        if carte in self.cartes:
            return self.cartes.index(carte)
        return -1