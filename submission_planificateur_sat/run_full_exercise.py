import os
import sys
import time
import subprocess

def check_dependencies():

    print("Vérification des dépendances...")
    
    required_packages = ['pysat', 'matplotlib']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f" {package}")
        except ImportError:
            print(f" {package}")
            missing.append(package)
    
    if missing:
        print(f"\nInstallez les packages manquants:")
        print(f"pip install {' '.join(missing)}")
        return False
    
    return True

def check_files():

    print("\nVérification des fichiers...")
    
    required_files = [
        'domain.pddl',
        'problem.pddl', 
        'encodeur_sat.py',
        'write_cnf.py',
        'run_solver.py',
        'benchmark.py'
    ]
    
    missing = []
    for file in required_files:
        if os.path.exists(file):
            print(f" {file}")
        else:
            print(f" {file}")
            missing.append(file)
    
    if missing:
        print(f"\nFichiers manquants: {missing}")
        return False
    
    return True

def run_step(step_name, command, description):
    """Exécute une étape de l'exercice"""
    print(f"\n{'='*50}")
    print(f"ÉTAPE: {step_name}")
    print(f"{'='*50}")
    print(f"Description: {description}")
    print(f"Commande: {command}")
    print()
    
    try:
        if isinstance(command, list):
            result = subprocess.run(command, check=True, capture_output=True, text=True)
        else:
            result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        
        if result.stdout:
            print("SORTIE:")
            print(result.stdout)
        
        print(f" {step_name} terminé avec succès")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f" Erreur dans {step_name}:")
        print(f"Code de retour: {e.returncode}")
        if e.stdout:
            print(f"Sortie: {e.stdout}")
        if e.stderr:
            print(f"Erreur: {e.stderr}")
        return False
    except Exception as e:
        print(f" Erreur inattendue dans {step_name}: {e}")
        return False

def run_complete_exercise():

    print(" EXERCICE 1 : PLANIFICATEUR SAT")
    print(" EXÉCUTION COMPLÈTE")
    print("=" * 50)
    
    # Étapes
    steps = [
        {
            'name': '1. Génération du fichier CNF',
            'command': 'python write_cnf.py',
            'description': 'Encode le problème en format SAT CNF'
        },
        {
            'name': '2. Résolution SAT', 
            'command': 'python run_solver.py',
            'description': 'Résout le problème avec MiniSat et génère le plan'
        },
        {
            'name': '3. Benchmark performance',
            'command': 'python benchmark.py', 
            'description': 'Analyse les performances sur différents horizons'
        },
        {
            'name': '4. Validation VAL',
            'command': 'python val_validator.py',
            'description': 'Valide le plan avec l\'outil VAL'
        },
        {
            'name': '5. Comparaison planificateurs',
            'command': 'python compare_planners.py',
            'description': 'Compare avec HSP et autres planificateurs'
        },
        {
            'name': '6. Génération résultats finaux',
            'command': 'python generate_results.py',
            'description': 'Compile tous les résultats et génère le rapport'
        }
    ]
    
    # Compteurs de succès
    success_count = 0
    total_steps = len(steps)
    
    # Exécution de chaque étape
    for step in steps:
        success = run_step(step['name'], step['command'], step['description'])
        if success:
            success_count += 1
        
        # Petite pause entre les étapes
        time.sleep(1)
    
    # Résumé final
    print("RÉSUMÉ DE L'EXÉCUTION")
    print(f"Étapes réussies: {success_count}/{total_steps}")
    
    if success_count == total_steps:
        print("EXERCICE COMPLÈTEMENT RÉUSSI!")
        print("\n Tous les objectifs atteints:")
        print("Planificateur SAT implémenté")
        print("Plans générés et validés")
        print("Comparaison avec autres planificateurs")
        print("Analyses de performance complètes")
        print("Rapports et documentation générés")
        
    elif success_count >= total_steps * 0.7:  # 70% de réussite
        print("EXERCICE LARGEMENT RÉUSSI")
        print(f"  {success_count} étapes sur {total_steps} réussies")
        print("  Points principaux atteints")
        
    else:
        print(" EXERCICE PARTIELLEMENT RÉUSSI")
        print(f"  Seulement {success_count} étapes sur {total_steps} réussies")
        print("  Vérifiez les erreurs ci-dessus")
    
    # Liste des fichiers générés
    print(f"\n FICHIERS GÉNÉRÉS:")
    generated_files = [
        'problem.cnf',
        'var_map.pkl', 
        'plan_output.txt',
        'benchmark_results.png',
        'benchmark_report.txt',
        'validation_report.txt',
        'planners_comparison.txt',
        'exercise_summary.txt',
        'results.json'
    ]
    
    for file in generated_files:
        if os.path.exists(file):
            print(f" {file}")
        else:
            print(f" {file} (manquant)")
    
    return success_count == total_steps

def create_submission_package():
    """Crée un package de soumission pour l'exercice"""
    print(f"\nCRÉATION DU PACKAGE DE SOUMISSION")
    
    # liste des fichiers à inclure dans la soumission
    submission_files = [
       
        'domain.pddl',
        'problem.pddl',
        'encodeur_sat.py', 
        'write_cnf.py',
        'run_solver.py',
        'benchmark.py',
        'val_validator.py',
        'compare_planners.py',
        'generate_results.py',
        'run_full_exercise.py',
        
        # Résultats
        'plan_output.txt',
        'benchmark_results.png',
        'benchmark_report.txt',
        'validation_report.txt',
        'planners_comparison.txt',
        'exercise_summary.txt',
        'results.json'
    ]
    
    # Création d'un dossier de soumission
    submission_dir = "submission_planificateur_sat"
    os.makedirs(submission_dir, exist_ok=True)
    
    # Copie des fichiers
    import shutil
    copied_count = 0
    
    for file in submission_files:
        if os.path.exists(file):
            try:
                shutil.copy2(file, submission_dir)
                print(f" {file}")
                copied_count += 1
            except Exception as e:
                print(f" {file}: {e}")
        else:
            print(f" {file} (pas trouvé)")
    
    # Création d'un README
    readme_path = os.path.join(submission_dir, "README.txt")
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write("EXERCICE 1 : PLANIFICATEUR SAT\n")
        f.write("=" * 35 + "\n\n")
        f.write("CONTENU DU PACKAGE:\n")
        f.write("- Fichiers source Python\n")
        f.write("- Fichiers PDDL (domaine et problème)\n")
        f.write("- Plans générés\n")
        f.write("- Rapports d'analyse\n")
        f.write("- Graphiques de performance\n\n")
        f.write("EXÉCUTION:\n")
        f.write("1. python run_full_exercise.py\n")
        f.write("   (lance l'exercice complet)\n\n")
        f.write("2. Ou étape par étape:\n")
        f.write("   - python write_cnf.py\n")
        f.write("   - python run_solver.py\n")
        f.write("   - python benchmark.py\n")
        f.write("   - etc.\n\n")
        f.write(f"Fichiers copiés: {copied_count}/{len(submission_files)}\n")
        f.write(f"Date: {time.strftime('%d/%m/%Y %H:%M')}\n")
    
    print(f"\n Package créé: {submission_dir}/")
    print(f" {copied_count} fichiers copiés")
    print(f" README inclus")
    
    return submission_dir

if __name__ == "__main__":
    print("LANCEMENT DE L'EXERCICE COMPLET")
    print("=" * 40)
    
    if not check_dependencies():
        print("Dépendances manquantes")
        sys.exit(1)
    
    if not check_files():
        print("Fichiers manquants") 
        sys.exit(1)
    
    print("Toutes les vérifications passées")
    
    # Lancement de l'exercice complet
    success = run_complete_exercise()
    
    # Création de package de soumission
    if success:
        package_dir = create_submission_package()
        print(f"\n EXERCICE TERMINÉ AVEC SUCCÈS!")
        print(f"Package de soumission prêt: {package_dir}/")
    else:
        print(f"\n Exercice terminé avec des erreurs")
        print("Consultez les messages ci-dessus pour diagnostiquer")
