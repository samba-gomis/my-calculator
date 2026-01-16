class Calculatrice:
    """Gère l'expression courante et l'historique des calculs"""
    
    def __init__(self):
        # Stocke ce que l'utilisateur tape
        self.expression_courante = ""
        # Liste pour garder tous les calculs effectués
        self.historique = []
        
    def ajouter_caractere(self, caractere):
        """Ajoute un chiffre ou symbole à l'expression"""
        self.expression_courante += str(caractere)
        
    def effacer_expression(self):
        """Efface tout ce qui a été tapé"""
        self.expression_courante = ""
        
    def ajouter_a_historique(self, expression, resultat):
        """Enregistre un calcul dans l'historique"""
        entree = f"{expression} = {resultat}"
        self.historique.append(entree)
        
    def effacer_historique(self):
        """Supprime tout l'historique"""
        self.historique = []
        
    def obtenir_historique(self):
        """Retourne la liste des calculs"""
        return self.historique