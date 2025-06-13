import pickle
from encodeur_sat import encode_gripper  # Correction de l'import
from pysat.formula import CNF

#Ce module génère un fichier CNF au format DIMACS à partir de l'encodage SAT 
#du problème Gripper. Le format DIMACS est le standard universel pour les 
#solveurs SAT, permettant l'interopérabilité entre différents outils.


def save_cnf_file(cnf, filename):
    with open(filename, "w") as f:
        f.write(f"p cnf {cnf.nv} {len(cnf.clauses)}\n")
        for clause in cnf.clauses:
            f.write(" ".join(map(str, clause)) + " 0\n")

if __name__ == "__main__":
    horizon = 4  
    print(f"Encodage du problème avec horizon = {horizon}")
    
    cnf, var_map = encode_gripper(horizon=horizon)
    
    print(f"Nombre de variables: {cnf.nv}")
    print(f"Nombre de clauses: {len(cnf.clauses)}")

    # Sauvegarde du fichier CNF
    save_cnf_file(cnf, "problem.cnf")

    # Sauvegarde du dictionnaire var_map
    with open("var_map.pkl", "wb") as f:
        pickle.dump(var_map, f)

    print("CNF et dictionnaire sauvegardés.")
    print("Fichiers générés:")
    print("  - problem.cnf")
    print("  - var_map.pkl")