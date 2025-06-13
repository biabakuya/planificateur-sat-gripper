# Validation des plans avec l'outil VAL
import subprocess
import os
import sys

def check_val_installation():
    """Vérifie si VAL est installé et accessible"""
    try:
        result = subprocess.run(['validate', '-h'], 
                              capture_output=True, text=True, timeout=5)
        return True
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return False

def validate_plan_with_val(domain_file, problem_file, plan_file):
    """Valide un plan avec VAL et retourne les résultats"""
    if not check_val_installation():
        print("Erreur: VAL n'est pas installé ou pas dans le PATH")
        print("Installez VAL depuis: https://github.com/KCL-Planning/VAL")
        return None
    
    try:
        # Commande VAL pour valider le plan
        cmd = ['validate', domain_file, problem_file, plan_file]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        validation_result = {
            'valid': 'Plan valid' in result.stdout,
            'makespan': extract_makespan(result.stdout),
            'actions_count': count_actions_in_plan(plan_file),
            'output': result.stdout,
            'error': result.stderr
        }
        
        return validation_result
        
    except subprocess.TimeoutExpired:
        print("Timeout lors de la validation VAL")
        return None
    except Exception as e:
        print(f"Erreur lors de la validation: {e}")
        return None

def extract_makespan(val_output):
    """Extrait le makespan depuis la sortie VAL"""
    lines = val_output.split('\n')
    for line in lines:
        if 'Plan length' in line or 'Makespan' in line:
            # Chercher le nombre dans la ligne
            words = line.split()
            for word in words:
                try:
                    return float(word)
                except ValueError:
                    continue
    return None

def count_actions_in_plan(plan_file):
    """Compte le nombre d'actions dans un plan"""
    if not os.path.exists(plan_file):
        return 0
    
    with open(plan_file, 'r') as f:
        lines = f.readlines()
    
    # Compter les lignes non vides qui ne commencent pas par ';' ou '#'
    action_count = 0
    for line in lines:
        line = line.strip()
        if line and not line.startswith(';') and not line.startswith('#'):
            action_count += 1
    
    return action_count

def convert_sat_plan_to_pddl(sat_plan_file, pddl_plan_file):
    """Convertit un plan SAT en format PDDL standard"""
    if not os.path.exists(sat_plan_file):
        print(f"Fichier plan SAT introuvable: {sat_plan_file}")
        return False
    
    try:
        with open(sat_plan_file, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        pddl_actions = []
        
        for line in lines:
            line = line.strip()
            if 'pickup_roomA' in line:
                pddl_actions.append("(pickup ball roomA)")
            elif 'move_A_to_B' in line:
                pddl_actions.append("(move roomA roomB)")
            elif 'drop_roomB' in line:
                pddl_actions.append("(drop ball roomB)")
        
        # Écrire le plan au format PDDL
        with open(pddl_plan_file, 'w') as f:
            for i, action in enumerate(pddl_actions):
                f.write(f"{action}\n")
        
        print(f"Plan PDDL généré: {pddl_plan_file}")
        return True
        
    except Exception as e:
        print(f"Erreur lors de la conversion: {e}")
        return False

def validate_sat_planner_results():
    """Valide les résultats du planificateur SAT"""
    print("Validation des plans avec VAL")
    print("=" * 35)
    
    # Fichiers nécessaires
    domain_file = "domain.pddl"
    problem_file = "problem.pddl"
    sat_plan_file = "plan_output.txt"
    pddl_plan_file = "plan_pddl.txt"
    
    # Vérifier que les fichiers existent
    missing_files = []
    for file in [domain_file, problem_file, sat_plan_file]:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print("Fichiers manquants:")
        for file in missing_files:
            print(f"  - {file}")
        return None
    
    # Convertir le plan SAT en format PDDL
    print("Conversion du plan SAT vers PDDL...")
    if not convert_sat_plan_to_pddl(sat_plan_file, pddl_plan_file):
        return None
    
    # Valider avec VAL
    print("Validation avec VAL...")
    result = validate_plan_with_val(domain_file, problem_file, pddl_plan_file)
    
    if result:
        print("\nRésultats de la validation:")
        print(f"  Plan valide: {'Oui' if result['valid'] else 'Non'}")
        print(f"  Nombre d'actions: {result['actions_count']}")
        if result['makespan']:
            print(f"  Makespan: {result['makespan']}")
        
        if result['valid']:
            print("✅ Plan validé avec succès par VAL")
        else:
            print("❌ Plan invalide selon VAL")
            if result['error']:
                print(f"Erreur: {result['error']}")
    
    return result

def create_validation_report(validation_result):
    """Crée un rapport de validation"""
    if not validation_result:
        return
    
    with open('validation_report.txt', 'w', encoding='utf-8') as f:
        f.write("RAPPORT DE VALIDATION VAL\n")
        f.write("=" * 30 + "\n\n")
        
        f.write("PLANIFICATEUR SAT - DOMAINE GRIPPER\n")
        f.write("-" * 35 + "\n\n")
        
        f.write(f"Plan valide: {'Oui' if validation_result['valid'] else 'Non'}\n")
        f.write(f"Nombre d'actions: {validation_result['actions_count']}\n")
        
        if validation_result['makespan']:
            f.write(f"Makespan: {validation_result['makespan']}\n")
        
        f.write(f"\nSortie VAL:\n")
        f.write("-" * 12 + "\n")
        f.write(validation_result['output'])
        
        if validation_result['error']:
            f.write(f"\nErreurs:\n")
            f.write("-" * 9 + "\n")
            f.write(validation_result['error'])
    
    print("Rapport de validation sauvegardé: validation_report.txt")

if __name__ == "__main__":
    # Vérifier l'installation de VAL
    if not check_val_installation():
        print("ATTENTION: VAL n'est pas installé")
        print("Pour installer VAL:")
        print("1. Téléchargez depuis: https://github.com/KCL-Planning/VAL")
        print("2. Compilez et ajoutez au PATH")
        print("3. Ou utilisez: sudo apt-get install val (sur Ubuntu)")
        print()
    
    # Lancer la validation
    result = validate_sat_planner_results()
    
    if result:
        create_validation_report(result)
        print("\nValidation terminée!")
    else:
        print("Échec de la validation")