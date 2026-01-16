import tkinter as tk
from tkinter import messagebox, Toplevel, Scrollbar, Text

# On importe les autres fichiers
from Calculatrice import Calculatrice
from Evaluateur import Evaluateur

class InterfaceCalculatrice:
    """Crée la fenêtre graphique de la calculatrice"""
    
    def __init__(self, root):
        self.root = root
        self.calculatrice = Calculatrice()
        
        # Configuration de la fenêtre
        self.root.title("Calculatrice Python")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        self.root.config(bg="#2C3E50")
        
        self.creer_interface()
        self.lier_clavier()
    
    def creer_interface(self):
        """Crée tous les boutons et zones de texte"""
        
        # Cadre principal
        frame_principal = tk.Frame(self.root, bg="#2C3E50")
        frame_principal.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)
        
        # Titre
        label_titre = tk.Label(
            frame_principal,
            text="CALCULATRICE PYTHON",
            font=("Arial", 16, "bold"),
            bg="#2C3E50",
            fg="white"
        )
        label_titre.pack(pady=10)
        
        # Zone où on tape l'expression
        self.zone_expression = tk.Entry(
            frame_principal,
            font=("Arial", 18),
            justify="right",
            bd=5,
            relief=tk.SUNKEN
        )
        self.zone_expression.pack(fill=tk.X, pady=5)
        
        # Zone qui affiche le résultat
        self.zone_resultat = tk.Label(
            frame_principal,
            text="",
            font=("Arial", 20, "bold"),
            bg="white",
            fg="#27AE60",
            anchor="e",
            padx=10,
            relief=tk.SUNKEN,
            bd=5,
            height=2
        )
        self.zone_resultat.pack(fill=tk.X, pady=5)
        
        # Cadre pour les boutons
        frame_boutons = tk.Frame(frame_principal, bg="#2C3E50")
        frame_boutons.pack(pady=10)
        
        # Disposition des boutons (chaque ligne)
        boutons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['0', '.', '(', '+'],
            [')', '^', '=', '']
        ]
        
        # Créer tous les boutons
        for i, ligne in enumerate(boutons):
            for j, texte in enumerate(ligne):
                if texte != '':
                    # Couleur selon le type de bouton
                    if texte == '=':
                        couleur = "#27AE60"  # Vert pour =
                    elif texte in "+-*/^":
                        couleur = "#3498DB"  # Bleu pour opérateurs
                    else:
                        couleur = "#34495E"  # Gris foncé pour chiffres
                    
                    bouton = tk.Button(
                        frame_boutons,
                        text=texte,
                        font=("Arial", 16, "bold"),
                        width=5,
                        height=2,
                        bg=couleur,
                        fg="white",
                        activebackground="#2980B9",
                        command=lambda t=texte: self.clic_bouton(t)
                    )
                    bouton.grid(row=i, column=j, padx=5, pady=5)
        
        # Cadre pour les boutons spéciaux
        frame_boutons_speciaux = tk.Frame(frame_principal, bg="#2C3E50")
        frame_boutons_speciaux.pack(pady=10)
        
        # Bouton CALCULER
        bouton_calculer = tk.Button(
            frame_boutons_speciaux,
            text="CALCULER",
            font=("Arial", 14, "bold"),
            width=12,
            height=2,
            bg="#27AE60",
            fg="white",
            command=self.calculer
        )
        bouton_calculer.grid(row=0, column=0, padx=5)
        
        # Bouton EFFACER
        bouton_effacer = tk.Button(
            frame_boutons_speciaux,
            text="EFFACER (C)",
            font=("Arial", 14, "bold"),
            width=12,
            height=2,
            bg="#E74C3C",
            fg="white",
            command=self.effacer
        )
        bouton_effacer.grid(row=0, column=1, padx=5)
        
        # Bouton HISTORIQUE
        bouton_historique = tk.Button(
            frame_principal,
            text="AFFICHER HISTORIQUE",
            font=("Arial", 12, "bold"),
            width=30,
            height=2,
            bg="#9B59B6",
            fg="white",
            command=self.afficher_historique
        )
        bouton_historique.pack(pady=10)
    
    def lier_clavier(self):
        """Connecte les touches du clavier aux actions"""
        # Touche Entrée = calculer
        self.root.bind('<Return>', lambda e: self.calculer())
        self.root.bind('<KP_Enter>', lambda e: self.calculer())
        # Touche Echap = effacer
        self.root.bind('<Escape>', lambda e: self.effacer())
        # Touche = = calculer
        self.root.bind('=', lambda e: self.calculer())
        
        # Touches pour taper l'expression
        for touche in '0123456789+-*/^.()':
            self.root.bind(touche, lambda e, t=touche: self.clic_bouton(t))
    
    def clic_bouton(self, caractere):
        """Quand on clique sur un bouton"""
        if caractere == '=':
            self.calculer()
        else:
            self.calculatrice.ajouter_caractere(caractere)
            self.mettre_a_jour_affichage()
    
    def mettre_a_jour_affichage(self):
        """Rafraîchit ce qui est affiché"""
        self.zone_expression.delete(0, tk.END)
        self.zone_expression.insert(0, self.calculatrice.expression_courante)
    
    def calculer(self):
  
        """Calcule et affiche le résultat"""
        expression = self.calculatrice.expression_courante
    
    if not expression:
        messagebox.showwarning("Attention", "Tapez d'abord une expression")
        #return
    
    try:
        # Calculer le résultat
        resultat = Evaluateur.evaluer(expression)
        
        # Formater joliment le résultat
        if resultat == int(resultat):
            resultat_str = str(int(resultat))
        else:
            resultat_str = f"{resultat:.6f}".rstrip('0').rstrip('.')
        
        # Afficher le résultat en vert
        self.zone_resultat.config(text=f"= {resultat_str}", fg="#27AE60")
        # Sauvegarder dans l'historique
        self.calculatrice.ajouter_a_historique(expression, resultat_str)
        
        # 🆕 AJOUTEZ CES 2 LIGNES : Préparer pour un nouveau calcul
        self.calculatrice.effacer_expression()
        self.zone_expression.delete(0, tk.END)
        
    except ValueError as e:
        # Afficher l'erreur en rouge
        self.zone_resultat.config(text=f"ERREUR: {str(e)}", fg="#E74C3C")
    except Exception as e:
        self.zone_resultat.config(text="ERREUR: Expression invalide", fg="#E74C3C")
    
    def effacer(self):
        """Efface tout"""
        self.calculatrice.effacer_expression()
        self.zone_expression.delete(0, tk.END)
        self.zone_resultat.config(text="", fg="#27AE60")
    
    def afficher_historique(self):
        """Ouvre une fenêtre pour voir l'historique"""
        fenetre_hist = Toplevel(self.root)
        fenetre_hist.title("Historique des calculs")
        fenetre_hist.geometry("500x400")
        fenetre_hist.config(bg="#34495E")
        
        # Titre
        label_titre = tk.Label(
            fenetre_hist,
            text="HISTORIQUE DES CALCULS",
            font=("Arial", 14, "bold"),
            bg="#34495E",
            fg="white"
        )
        label_titre.pack(pady=10)
        
        # Cadre pour le texte avec ascenseur
        frame_texte = tk.Frame(fenetre_hist, bg="#34495E")
        frame_texte.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # Barre de défilement
        scrollbar = Scrollbar(frame_texte)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Zone de texte pour l'historique
        texte_historique = Text(
            frame_texte,
            font=("Courier", 12),
            bg="white",
            fg="black",
            yscrollcommand=scrollbar.set,
            relief=tk.SUNKEN,
            bd=5
        )
        texte_historique.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=texte_historique.yview)
        
        # Afficher tous les calculs
        historique = self.calculatrice.obtenir_historique()
        if historique:
            for i, entree in enumerate(historique, 1):
                texte_historique.insert(tk.END, f"{i}. {entree}\n")
        else:
            texte_historique.insert(tk.END, "Aucun calcul dans l'historique")
        
        texte_historique.config(state=tk.DISABLED)
        
        # Cadre pour les boutons
        frame_boutons = tk.Frame(fenetre_hist, bg="#34495E")
        frame_boutons.pack(pady=10)
        
        # Bouton pour effacer l'historique
        bouton_effacer = tk.Button(
            frame_boutons,
            text="EFFACER HISTORIQUE",
            font=("Arial", 11, "bold"),
            bg="#E74C3C",
            fg="white",
            width=20,
            command=lambda: self.effacer_historique(fenetre_hist)
        )
        bouton_effacer.pack(side=tk.LEFT, padx=10)
        
        # Bouton pour fermer
        bouton_fermer = tk.Button(
            frame_boutons,
            text="FERMER",
            font=("Arial", 11, "bold"),
            bg="#95A5A6",
            fg="white",
            width=15,
            command=fenetre_hist.destroy
        )
        bouton_fermer.pack(side=tk.LEFT, padx=10)
    
    def effacer_historique(self, fenetre):
        """Demande confirmation puis efface l'historique"""
        reponse = messagebox.askyesno(
            "Confirmation",
            "Voulez-vous vraiment tout effacer ?"
        )
        if reponse:
            self.calculatrice.effacer_historique()
            messagebox.showinfo("Succès", "Historique effacé")
            fenetre.destroy()