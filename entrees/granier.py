from .entree import current_host, Entree


class Granier(Entree):
    def __init__(self, nom='granier', host=current_host, period=10, n_values=3):
        super(Granier, self).__init__(nom=nom, host=host, period=period, n_values=n_values)
