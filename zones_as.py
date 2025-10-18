from cartes import Cartes

class Zones_as:
    """Représente une zone de destination pour les cartes (As à Roi d'une même famille)"""

    def __init__(self, valeur: int, famille: str | None, x: int, y: int) -> None:
        """Initialise une zone As.Les entrées sont la valeur initiale, la famille de cartes (None au départ), et les coordonnées x et y.La sortie est une instance de Zones_as initialisée."""
        self.cartes: list[Cartes] = []
        self.valeur: int = valeur
        self.famille: str | None = famille
        self.x: int = x
        self.y: int = y
        self.rect_id: int | None = None

    def peut_ajouter(self, carte: Cartes) -> bool:
        """Vérifie si une carte peut être ajoutée à cette zone selon les règles du Solitaire.Les entrées sont la carte à vérifier.La sortie est un booléen : True si la carte peut être ajoutée, False sinon."""
        if not self.cartes:
            return carte.valeur == 1  # As sur zone vide
        top: Cartes = self.cartes[-1]
        return carte.famille == top.famille and carte.valeur == top.valeur + 1

    def ajouter_carte(self, carte: Cartes) -> None:
        """Ajoute une carte à la zone.Les entrées sont la carte à ajouter.Il n'y a pas de sortie (None)."""
        if not self.cartes:
            self.famille = carte.famille
        self.cartes.append(carte)