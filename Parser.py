class Parser:
    """Découpe l'expression en morceaux (nombres et symboles)"""
    
    def tokeniser(expression):
        """
        Transforme "2+3*4" en ['2', '+', '3', '*', '4']
        C'est plus facile à analyser ensuite !
        """
        tokens = []  # Liste des morceaux
        nombre_actuel = ""  # Nombre en cours de lecture
        expression = expression.replace(" ", "")  # Enlever les espaces
        
        i = 0
        while i < len(expression):
            char = expression[i]
            
            # Si c'est un chiffre ou un point
            if char.isdigit() or char == '.':
                nombre_actuel += char
                
            # Si c'est un symbole mathématique
            elif char in "+-*/^()":
                # Sauvegarder le nombre en cours
                if nombre_actuel:
                    tokens.append(nombre_actuel)
                    nombre_actuel = ""
                
                # Gérer les nombres négatifs comme -5
                if char == '-':
                    # Si c'est au début ou après un symbole
                    if i == 0 or expression[i-1] in "+-*/^(":
                        nombre_actuel = "-"
                        i += 1
                        continue
                
                tokens.append(char)
            
            i += 1
        
        # Ajouter le dernier nombre
        if nombre_actuel:
            tokens.append(nombre_actuel)
        
        return tokens
    
    def est_nombre(token):
        """Vérifie si un morceau est un nombre"""
        try:
            float(token)
            return True
        except ValueError:
            return False
    
    def est_operateur(token):
        """Vérifie si un morceau est un opérateur (+, -, *, /, ^)"""
        return token in "+-*/^"