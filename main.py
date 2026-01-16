import tkinter as tk
from Interface import InterfaceCalculatrice

def main():
     
    # Créer la fenêtre principale
    root = tk.Tk()
    
    # Créer l'interface de la calculatrice
    app = InterfaceCalculatrice(root)
    
    # Lancer la boucle d'affichage
    root.mainloop()


# Point d'entrée du programme
if __name__ == "__main__":
    main()