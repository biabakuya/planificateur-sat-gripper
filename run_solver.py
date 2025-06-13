from pysat.solvers import Minisat22
import pickle
import time

def load_cnf_file(filename): #Chargement d'un fichier CNF au format DIMACS et retourne les clauses
    clauses = []
    with open(filename, "r") as f:
        for line in f:
            if line.startswith("p") or line.startswith("c"):
                continue
            literals = list(map(int, line.strip().split()))   # Conversion de la ligne en liste d'entiers
            if literals and literals[-1] == 0:
                literals.pop()
            if literals:         # Ajout de la clause si elle n'est pas vide
                clauses.append(literals)
    return clauses

def print_state(var_map, model, t):
    #Affichage de l'état du monde à l'instant t
    print(f"\n=== État à t={t} ===")
    
    # Récupère tous les faits vrais à l'instant t
    facts_at_t = {}
    for (typ, fact, time), var_id in var_map.items():
        if typ == "fact" and time == t:
            facts_at_t[fact] = var_id in model and model[model.index(var_id)] > 0
    
    # Position du robot
    if facts_at_t.get("at_robot_roomA", False):
        print(" Robot dans roomA")
    elif facts_at_t.get("at_robot_roomB", False):
        print(" Robot dans roomB")
    
    # Position de la balle
    if facts_at_t.get("at_ball_roomA", False):
        print(" Balle dans roomA")
    elif facts_at_t.get("at_ball_roomB", False):
        print(" Balle dans roomB")
    elif facts_at_t.get("holding_ball", False):
        print(" Robot tient la balle")
    
    # État de la main
    if facts_at_t.get("free_hand", False):
        print(" Main libre")
    elif facts_at_t.get("holding_ball", False):
        print(" Main occupée")

if __name__ == "__main__":
    try:
        # chargement du fichier CNF qui venait d'être généré
        print("Chargement du problème CNF...")
        clauses = load_cnf_file("problem.cnf")

        #Chargement du dictionnaire de mapping des variables
        with open("var_map.pkl", "rb") as f:
            var_map = pickle.load(f)

        print(f"Clauses chargées: {len(clauses)}")
        print(f"Variables mappées: {len(var_map)}")
        
        # Créer le mapping inverse pour décoder la solution
        rev_map = {v: k for k, v in var_map.items()}

        # lancement du solveur SAT MiniSat
        print("\nRésolution avec MiniSat...")
        with Minisat22(bootstrap_with=clauses) as solver:
            start = time.time()
            if solver.solve():
                end = time.time()
                model = solver.get_model()
                print(" Plan trouvé !")
                print(f"  Temps de résolution: {round(end - start, 4)} secondes")

                # Extractions dees actions du modèle
                actions = []
                facts_true = []
                
                for v in model:
                    if v > 0 and v in rev_map:
                        typ, content, t = rev_map[v]
                        if typ == "act":
                            actions.append((t, content))
                        elif typ == "fact":
                            facts_true.append((content, t))

                # organisation et affichage du plan
                actions.sort()
                
                print(f"\n Plan de {len(actions)} actions:")
                if actions:
                    # Affichage de l'état initial
                    print_state(var_map, model, 0)
                    
                    # Afficher chaque action et l'état résultant
                    for i, (t, action) in enumerate(actions):
                         # Gère l'affichage selon le format de l'action
                        if isinstance(action, tuple):
                            if len(action) == 2:
                                act_name, param = action
                                print(f"\n Action {i+1}: {act_name}({param}) à t={t}")
                            elif len(action) == 3:
                                act_name, param1, param2 = action
                                print(f"\n Action {i+1}: {act_name}({param1}, {param2}) à t={t}")
                        else:
                            print(f"\n Action {i+1}: {action} à t={t}")
                        
                        # Affichage de l'état après l'action
                        print_state(var_map, model, t + 1)

                    # Sauvegarde du plan
                    with open("plan_output.txt", "w", encoding="utf-8") as f:
                        f.write("Plan de résolution du problème Gripper\n")
                        f.write("=" * 40 + "\n\n")
                        
                        for i, (t, action) in enumerate(actions):
                            if isinstance(action, tuple):
                                if len(action) == 2:
                                    act_name, param = action
                                    f.write(f"Étape {i+1}: {act_name}({param}) à t={t}\n")
                                elif len(action) == 3:
                                    act_name, param1, param2 = action
                                    f.write(f"Étape {i+1}: {act_name}({param1}, {param2}) à t={t}\n")
                            else:
                                f.write(f"Étape {i+1}: {action} à t={t}\n")
                    
                    print(f"\n Plan détaillé sauvegardé dans 'plan_output.txt'")
                    
                    # Vérification de l'objectif
                    horizon = max(t for typ, _, t in var_map.keys() if typ == "fact")
                    goal_var = var_map.get(("fact", "at_ball_roomB", horizon))
                    if goal_var and goal_var in [abs(v) for v in model if v > 0]:
                        print(" Objectif atteint: la balle est dans roomB!")
                    else:
                        print("Attention: l'objectif pourrait ne pas être atteint")
                        
                else:
                    print(" Aucune action trouvée dans le modèle")
                    
            else:
                end = time.time()
                print("Aucun plan trouvé (problème non satisfiable)")
                print(f"Temps de recherche: {round(end - start, 4)} secondes")
               
    except FileNotFoundError as e:
        print(f"Erreur: fichier manquant - {e}")
        print("Assurez-vous d'avoir exécuté write_cnf.py d'abord")
    except Exception as e:
        print(f"Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()