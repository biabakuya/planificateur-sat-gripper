# Planificateur SAT - Domaine Gripper

Implémentation d'un planificateur basé sur la satisfiabilité booléenne (SAT) pour résoudre des problèmes de planification dans le domaine Gripper.

## Fonctionnalités

- Encodage SAT de problèmes PDDL
- Résolution avec solveur MiniSat
- Validation des plans avec VAL
- Analyse de performance et benchmarks
- Comparaison avec d'autres planificateurs

## Prérequis

- Python 3.7+
- pip

## Installation

1. Cloner le repository :
```bash
git clone https://github.com/biabakuya/planificateur-sat-gripper.git
cd planificateur-sat-gripper
```

2. Installer les dépendances :
```bash
pip install python-sat matplotlib pandas
```

3. (Optionnel) Installer VAL pour la validation :
```bash
# Ubuntu/Debian
sudo apt-get install val

# Ou télécharger depuis: https://github.com/KCL-Planning/VAL
```

## Utilisation

### Exécution automatique
```bash
python run_full_exercise.py
```

### Exécution manuelle
```bash
# Générer le fichier CNF
python write_cnf.py

# Résoudre avec SAT
python run_solver.py

# Lancer les benchmarks
python benchmark.py

# Comparer les planificateurs
python compare_planners.py
```

## Structure du projet

```
.
domain.pddl              # Définition du domaine PDDL
problem.pddl             # Instance du problème
encodeur_sat.py          # Logique d'encodage SAT
write_cnf.py             # Génération fichier CNF
run_solver.py            # Interface solveur SAT
benchmark.py             # Analyse de performance
ompare_planners.py      # Comparaison planificateurs
val_validator.py         # Validation des plans
run_full_exercise.py     # Script principal
```

## Résultats

Le planificateur SAT trouve des solutions optimales en 3 étapes :
1. `pickup_roomA` - Ramasser la balle
2. `move_A_to_B` - Se déplacer vers roomB
3. `drop_roomB` - Déposer la balle

**Performance :** < 1ms de résolution

## Fichiers générés

- `plan_output.txt` - Plan de solution
- `benchmark_results.png` - Graphiques de performance
- `benchmark_report.txt` - Analyse détaillée
- `planners_comparison.txt` - Résultats de comparaison

## Licence

Projet académique - Usage libre pour l'apprentissage et la recherche.
