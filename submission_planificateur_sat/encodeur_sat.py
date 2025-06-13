"""
Encodeur SAT pour le domaine Gripper - Planification automatisée

Ce module implémente l'encodage SAT pour résoudre des problèmes de planification dans le domaine Gripper. Le domaine Gripper 
consiste en un robot qui doit déplacer une balle entre différentes pièces.

"""

from pysat.formula import CNF


def encode_gripper(horizon=4):

    # Initialisation de la formule CNF et du compteur de variables
    cnf = CNF()
    var_counter = 1  
    var_map = {}     # Mapping bidirectionnel entre concepts et variables numériques
    
    
    # DÉFINITION DE L'ESPACE D'ÉTATS
    # Faits atomiques décrivant l'état du monde à chaque instant
    facts = [
        "at_ball_roomA",  # La balle est dans la pièce A
        "at_ball_roomB",   # La balle est dans la pièce B  
        "at_robot_roomA",   # Le robot est dans la pièce A
        "at_robot_roomB",  # Le robot est dans la pièce B
        "free_hand",     # La main du robot est libre
        "holding_ball"   # Le robot tient la balle
    ]
    
    # Création des variables booléennes pour chaque fait à chaque instant
    for t in range(horizon + 1):  
        for fact in facts:
            var_map[("fact", fact, t)] = var_counter
            var_counter += 1
    
    # Actions possibles dans le domaine Gripper
    actions = [
        "pickup_roomA",   
        "drop_roomB",     
        "move_A_to_B",    
        "move_B_to_A"     
    ]
    
    # Création des variables booléennes pour chaque action à chaque instant, ici nous avons definies les actions que jusqu'à horizon-1 (pas à l'état final)
    for t in range(horizon):
        for action in actions:
            var_map[("act", action, t)] = var_counter
            var_counter += 1
    
   
    # ENCODAGE DE L'ÉTAT INITIAL
    # L'état initial correspond au problème spécifique à résoudre
    # Dans notre cas la balle se trouve dans roomA, robot dans roomA, main libre
    cnf.append([var_map[("fact", "at_ball_roomA", 0)]])    
    cnf.append([var_map[("fact", "at_robot_roomA", 0)]])   
    cnf.append([var_map[("fact", "free_hand", 0)]])        
    
   
    cnf.append([-var_map[("fact", "at_ball_roomB", 0)]])    
    cnf.append([-var_map[("fact", "at_robot_roomB", 0)]])   
    cnf.append([-var_map[("fact", "holding_ball", 0)]])  
    

    
    for t in range(horizon + 1):
        
        # Contrainte 1: Le robot ne peut être que dans une seule pièce
        cnf.append([-var_map[("fact", "at_robot_roomA", t)], 
                   -var_map[("fact", "at_robot_roomB", t)]])
        
        # Contrainte 2: Le robot doit être quelque part 
        cnf.append([var_map[("fact", "at_robot_roomA", t)], 
                   var_map[("fact", "at_robot_roomB", t)]])
        
        # Contrainte 3: La main ne peut être libre ET occupée simultanément
        cnf.append([-var_map[("fact", "free_hand", t)], 
                   -var_map[("fact", "holding_ball", t)]])
        
        # Contrainte 4: La main est soit libre, soit occupée
        cnf.append([var_map[("fact", "free_hand", t)], 
                   var_map[("fact", "holding_ball", t)]])
        
        # Contrainte 5-7: La balle ne peut être qu'à un seul endroit
        cnf.append([-var_map[("fact", "at_ball_roomA", t)], 
                   -var_map[("fact", "at_ball_roomB", t)]])
        cnf.append([-var_map[("fact", "at_ball_roomA", t)], 
                   -var_map[("fact", "holding_ball", t)]])
        cnf.append([-var_map[("fact", "at_ball_roomB", t)], 
                   -var_map[("fact", "holding_ball", t)]])
        
        # Contrainte 8: La balle doit être quelque part
        cnf.append([var_map[("fact", "at_ball_roomA", t)], 
                   var_map[("fact", "at_ball_roomB", t)], 
                   var_map[("fact", "holding_ball", t)]])
    
      # Pour chaque instant temporel, on encode la logique de chaque action possible
    # Chaque action a des préconditions
    # et des effets (ce qui devient vrai/faux après son exécution)
    
    for t in range(horizon):
        
        # l'action de depart est le ramassage  de la balle dans roomA)
        pickup = var_map[("act", "pickup_roomA", t)]
        
        cnf.append([-pickup, var_map[("fact", "at_robot_roomA", t)]])
        cnf.append([-pickup, var_map[("fact", "at_ball_roomA", t)]])
        cnf.append([-pickup, var_map[("fact", "free_hand", t)]])
        
        # après avoir ramassé, le robot tient la balle, 
        cnf.append([-pickup, var_map[("fact", "holding_ball", t + 1)]])
        cnf.append([-pickup, -var_map[("fact", "at_ball_roomA", t + 1)]])
        cnf.append([-pickup, -var_map[("fact", "free_hand", t + 1)]])
        
        # en deuxieme position, le depot de la balle dans roomB par le robot
        drop = var_map[("act", "drop_roomB", t)]
        
        cnf.append([-drop, var_map[("fact", "at_robot_roomB", t)]])
        cnf.append([-drop, var_map[("fact", "holding_ball", t)]])
        

        cnf.append([-drop, var_map[("fact", "at_ball_roomB", t + 1)]])
        cnf.append([-drop, var_map[("fact", "free_hand", t + 1)]])
        cnf.append([-drop, -var_map[("fact", "holding_ball", t + 1)]])
        
        # Se déplacer de roomA vers roomB
        move_ab = var_map[("act", "move_A_to_B", t)]
        
        # Le robot doit être dans roomA
        cnf.append([-move_ab, var_map[("fact", "at_robot_roomA", t)]])
        
        # Le robot est maintenant dans roomB et n'est plus dans roomA
        cnf.append([-move_ab, var_map[("fact", "at_robot_roomB", t + 1)]])
        cnf.append([-move_ab, -var_map[("fact", "at_robot_roomA", t + 1)]])
        
        # Se déplacer de roomB vers roomA
        move_ba = var_map[("act", "move_B_to_A", t)]
        
        #Le robot doit être dans roomB
        cnf.append([-move_ba, var_map[("fact", "at_robot_roomB", t)]])
        
        #Le robot est maintenant dans roomA et n'est plus dans roomB
        cnf.append([-move_ba, var_map[("fact", "at_robot_roomA", t + 1)]])
        cnf.append([-move_ba, -var_map[("fact", "at_robot_roomB", t + 1)]])
        

        cnf.append([-var_map[("fact", "at_ball_roomA", t)], pickup, 
                   var_map[("fact", "at_ball_roomA", t + 1)]])

        cnf.append([var_map[("fact", "at_ball_roomA", t)], -pickup, 
                   -var_map[("fact", "at_ball_roomA", t + 1)]])
        

        cnf.append([-var_map[("fact", "at_ball_roomB", t)], 
                   var_map[("fact", "at_ball_roomB", t + 1)]])
        cnf.append([var_map[("fact", "at_ball_roomB", t)], drop, 
                   -var_map[("fact", "at_ball_roomB", t + 1)]])
        
  
        cnf.append([-var_map[("fact", "holding_ball", t)], drop, 
                   var_map[("fact", "holding_ball", t + 1)]])
        cnf.append([var_map[("fact", "holding_ball", t)], pickup, 
                   -var_map[("fact", "holding_ball", t + 1)]])
        
        cnf.append([-var_map[("fact", "free_hand", t)], pickup, 
                   var_map[("fact", "free_hand", t + 1)]])
        cnf.append([var_map[("fact", "free_hand", t)], drop, 
                   -var_map[("fact", "free_hand", t + 1)]])
        
        cnf.append([-var_map[("fact", "at_robot_roomA", t)], move_ab, 
                   var_map[("fact", "at_robot_roomA", t + 1)]])
        cnf.append([var_map[("fact", "at_robot_roomA", t)], move_ba, 
                   -var_map[("fact", "at_robot_roomA", t + 1)]])
        
        cnf.append([-var_map[("fact", "at_robot_roomB", t)], move_ba, 
                   var_map[("fact", "at_robot_roomB", t + 1)]])
        cnf.append([var_map[("fact", "at_robot_roomB", t)], move_ab, 
                   -var_map[("fact", "at_robot_roomB", t + 1)]])
        
        
        # Dans le domaine Gripper, le robot ne peut exécuter qu'une seule actionà la fois. Cette contrainte évite les plans incohérents où plusieurs
        # actions seraient exécutées simultanément.

        all_actions = [pickup, drop, move_ab, move_ba]
        for i in range(len(all_actions)):
            for j in range(i + 1, len(all_actions)):

                cnf.append([-all_actions[i], -all_actions[j]])
   
    # L'objectif du problème Gripper est d'avoir la balle dans roomB à la fin, Cette contrainte force le solveur à trouver un plan qui atteint cet objectif
    cnf.append([var_map[("fact", "at_ball_roomB", horizon)]])
    
    return cnf, var_map