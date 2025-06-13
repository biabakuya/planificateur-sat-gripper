import os
import sys
import argparse
import time
from pathlib import Path

def check_dependencies():
   
    required_packages = ['pysat', 'matplotlib', 'pandas']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing.append(package)
    
    if missing:
        print(" Dépendances manquantes:")
        for pkg in missing:
            print(f"   - {pkg}")
        print("\nInstallation:")
        print(f"   pip install {' '.join(missing)}")
        return False
    
    return True

def run_basic_planning():
 
    print(" PLANIFICATION DE BASE")
    print("=" * 30)
    
    try:
      
        print(" Génération du fichier CNF...")
        os.system("python write_cnf.py")
        
        if not os.path.exists("problem.cnf"):
            print(" Échec de la génération du CNF")
            return False
        
 
        print("\n Résolution du problème...")
        os.system("python run_solver.py")
        
        return True
        
    except Exception as e:
        print(f" Erreur lors de la planification: {e}")
        return False

def run_validation():

    print("\n VALIDATION")
    print("=" * 15)
    
    try:
        os.system("python validation.py")
        return True
    except Exception as e:
        print(f" Erreur lors de la validation: {e}")
        return False

def run_benchmarks():

    print("\n BENCHMARKS")
    print("=" * 15)
    
    try:
        os.system("python benchmark.py")
        return True
    except Exception as e:
        print(f" Erreur lors du benchmark: {e}")
        return False

def run_problem_generation():

    print("\n GÉNÉRATION DE PROBLÈMES")
    print("=" * 30)
    
    try:
        os.system("python generate_problems.py")
        return True
    except Exception as e:
        print(f" Erreur lors de la génération: {e}")
        return False

def clean_files():

    files_to_clean = [
        "problem.cnf",
        "var_map.pkl",
        "plan_output.txt",
        "benchmark_results.png",
        "benchmark_report.txt"
    ]
    
    dirs_to_clean = ["problems", "domains"]
    
    print(" Nettoyage des fichiers temporaires...")
    
    for file in files_to_clean:
        if os.path.exists(file):
            os.remove(file)
            print(f" Supprimé: {file}")
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            import shutil
            shutil.rmtree(dir_name)
            print(f" Supprimé: {dir_name}/")

def show_results():

    print("\n RÉSUMÉ DES RÉSULTATS")
    print("=" * 25)
    
    files_to_check = {
        "plan_output.txt": "Plan de solution",
        "benchmark_report.txt": "Rapport de benchmark",
        "benchmark_results.png": "Graphiques de performance"
    }
    
    for file, description in files_to_check.items():
        if os.path.exists(file):
            print(f" {description}: {file}")
        else:
            print(f" {description}: non généré")
    

    if os.path.exists("plan_output.txt"):
        print(f"\n Contenu du plan:")
        with open("plan_output.txt", "r", encoding="utf-8") as f:
            content = f.read()
            print("   " + content.replace("\n", "\n   "))
 
 #Fonction principale"
def main():
   
    parser = argparse.ArgumentParser(description="Planificateur SAT pour le domaine Gripper")
    parser.add_argument("--mode", choices=["basic", "full", "validation", "benchmark", "generate", "clean"], 
                       default="basic", help="Mode d'exécution")
    parser.add_argument("--horizon", type=int, default=4, help="Horizon temporel (défaut: 4)")
    parser.add_argument("--quiet", action="store_true", help="Mode silencieux")
    
    args = parser.parse_args()
    
    if not args.quiet:
        print("PLANIFICATEUR SAT - DOMAINE GRIPPER")
        print("=" * 40)
        print(f"Mode: {args.mode}")
        print(f"Horizon: {args.horizon}")
        print()
    
    # Vérification des dépendances
    if not check_dependencies():
        return 1
    
    success = True
    start_time = time.time()
    
    try:
        if args.mode == "clean":
            clean_files()
            
        elif args.mode == "basic":
            success = run_basic_planning()
            
        elif args.mode == "validation":
            success = run_validation()
            
        elif args.mode == "benchmark":
            success = run_benchmarks()
            
        elif args.mode == "generate":
            success = run_problem_generation()
            
        elif args.mode == "full":
            
            success = (run_basic_planning() and 
                      run_validation() and 
                      run_benchmarks() and 
                      run_problem_generation())
        
        end_time = time.time()
        
        if not args.quiet:
            if success:
                print(f"\n Exécution terminée avec succès!")
                print(f" Temps total: {end_time - start_time:.2f} secondes")
                show_results()
            else:
                print(f"\n Exécution terminée avec des erreurs")
                return 1
                
    except KeyboardInterrupt:
        print(f"\n  Interruption par l'utilisateur")
        return 1
    except Exception as e:
        print(f"\n Erreur inattendue: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())