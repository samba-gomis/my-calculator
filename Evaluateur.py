from Parser import Parser

class Evaluateur:
    """Calcule le résultat de l'expression"""
    
    # Ordre de priorité des opérateurs (plus le chiffre est élevé, plus c'est prioritaire)
    PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    # Associativité (G = gauche à droite, D = droite à gauche)
    ASSOCIATIVITE = {'+': 'G', '-': 'G', '*': 'G', '/': 'G', '^': 'D'}
    
    def puissance(base, exposant):
        """Calcule base^exposant (ex: 2^3 = 8)"""
        if exposant == 0:
            return 1
        
        # Si l'exposant est négatif (ex: 2^-3)
        if exposant < 0:
            if base == 0:
                raise ValueError("Impossible : 0 avec exposant négatif")
            return 1 / Evaluateur.puissance(base, -exposant)
        
        # Si l'exposant a des décimales
        if exposant != int(exposant):
            resultat = 1
            exp_entier = int(exposant)
            for _ in range(exp_entier):
                resultat *= base
            return resultat
        
        # Méthode rapide pour calculer la puissance
        resultat = 1
        exposant = int(exposant)
        
        while exposant > 0:
            if exposant % 2 == 1:
                resultat *= base
            base *= base
            exposant //= 2
        
        return resultat
    
    def convertir_en_postfixe(tokens):
        """
        Réorganise les morceaux pour faciliter le calcul
        Utilise l'algorithme de Dijkstra (Shunting Yard)
        """
        sortie = []
        pile_operateurs = []
        
        for token in tokens:
            # Si c'est un nombre, on l'ajoute directement
            if Parser.est_nombre(token):
                sortie.append(token)
            
            # Si c'est un opérateur (+, -, *, /, ^)
            elif Parser.est_operateur(token):
                # On vérifie la priorité avec les opérateurs déjà en attente
                while (pile_operateurs and 
                       pile_operateurs[-1] != '(' and
                       pile_operateurs[-1] in Evaluateur.PRECEDENCE and
                       (Evaluateur.PRECEDENCE[pile_operateurs[-1]] > Evaluateur.PRECEDENCE[token] or
                        (Evaluateur.PRECEDENCE[pile_operateurs[-1]] == Evaluateur.PRECEDENCE[token] and
                         Evaluateur.ASSOCIATIVITE[token] == 'G'))):
                    sortie.append(pile_operateurs.pop())
                pile_operateurs.append(token)
            
            # Si c'est une parenthèse ouvrante
            elif token == '(':
                pile_operateurs.append(token)
            
            # Si c'est une parenthèse fermante
            elif token == ')':
                while pile_operateurs and pile_operateurs[-1] != '(':
                    sortie.append(pile_operateurs.pop())
                if not pile_operateurs:
                    raise ValueError("Parenthèses mal placées")
                pile_operateurs.pop()  # Enlever la (
        
        # Vider ce qui reste
        while pile_operateurs:
            if pile_operateurs[-1] in '()':
                raise ValueError("Parenthèses mal placées")
            sortie.append(pile_operateurs.pop())
        
        return sortie
    
    def evaluer_postfixe(postfixe):
        """Calcule le résultat à partir de la notation postfixe"""
        pile = []
        
        for token in postfixe:
            # Si c'est un nombre, on l'empile
            if Parser.est_nombre(token):
                pile.append(float(token))
            
            # Si c'est un opérateur, on calcule
            elif Parser.est_operateur(token):
                if len(pile) < 2:
                    raise ValueError("Expression invalide")
                
                # On prend les deux derniers nombres
                operande2 = pile.pop()
                operande1 = pile.pop()
                
                # On fait le calcul
                if token == '+':
                    resultat = operande1 + operande2
                elif token == '-':
                    resultat = operande1 - operande2
                elif token == '*':
                    resultat = operande1 * operande2
                elif token == '/':
                    if operande2 == 0:
                        raise ValueError("Division par zéro impossible")
                    resultat = operande1 / operande2
                elif token == '^':
                    resultat = Evaluateur.puissance(operande1, operande2)
                
                # On remet le résultat dans la pile
                pile.append(resultat)
        
        if len(pile) != 1:
            raise ValueError("Expression invalide")
        
        return pile[0]
    
    def evaluer(expression):
        """
        Fonction principale qui calcule le résultat final
        C'est celle qu'on appelle de l'extérieur !
        """
        # On a besoin du validateur ici
        from Validateur import Validateur
        
        # 1. Vérifier que l'expression est correcte
        valide, message = Validateur.valider_expression(expression)
        if not valide:
            raise ValueError(message)
        
        # 2. Découper en morceaux
        tokens = Parser.tokeniser(expression)
        
        if not tokens:
            raise ValueError("Expression vide")
        
        # 3. Réorganiser pour faciliter le calcul
        postfixe = Evaluateur.convertir_en_postfixe(tokens)
        
        # 4. Calculer le résultat
        resultat = Evaluateur.evaluer_postfixe(postfixe)
        
        return resultat