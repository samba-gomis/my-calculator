class Validateur:
    """Vérifie que l'expression mathématique est correcte"""
    
    def valider_expression(expression):
        """
        Vérifie si l'expression peut être calculée
        Retourne (True, "") si OK, (False, "message d'erreur") sinon
        """
        # Vérifier que ce n'est pas vide
        if not expression or expression.strip() == "":
            return False, "Expression vide"
        
        # Liste des caractères autorisés
        caracteres_autorises = set("0123456789+-*/^.()=")
        for char in expression.replace(" ", ""):
            if char not in caracteres_autorises:
                return False, f"Caractère non autorisé : '{char}'"
        
        # Vérifier que les parenthèses sont bien fermées
        compteur = 0
        for char in expression:
            if char == '(':
                compteur += 1
            elif char == ')':
                compteur -= 1
                if compteur < 0:
                    return False, "Parenthèses mal placées"
        
        if compteur != 0:
            return False, "Parenthèses non fermées"
        
        # Vérifier qu'il n'y a pas deux opérateurs collés (++ ou ** etc.)
        expression_clean = expression.replace(" ", "")
        if any(op in expression_clean for op in ["++", "**", "//", "^^"]):
            return False, "Deux opérateurs collés"
        
        # Vérifier que ça ne commence pas par * / ou ^
        if expression_clean and expression_clean[0] in "*/^":
            return False, "Ne peut pas commencer par cet opérateur"
        
        # Vérifier que ça ne finit pas par un opérateur
        if expression_clean and expression_clean[-1] in "+-*/^":
            return False, "Ne peut pas finir par un opérateur"
        
        return True, ""
