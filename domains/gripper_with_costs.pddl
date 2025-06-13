(define (domain gripper)
  (:requirements :strips :action-costs)
  (:predicates
    (at_ball ?x)        ;; La balle est dans la pièce ?x
    (at_robot ?x)       ;; Le robot est dans la pièce ?x
    (free_hand)         ;; La main est libre
    (holding_ball)      ;; Le robot tient la balle
  )
  (:functions (total-cost) - number)
  (:action pickup
    :parameters (?x)
    :precondition (and
      (at_ball ?x)
      (at_robot ?x)
      (free_hand)
    )
    :effect (and
      (holding_ball)
      (not (at_ball ?x))
      (not (free_hand))
      (increase (total-cost) 1)
    )
  )
  (:action drop
    :parameters (?x)
    :precondition (and
      (holding_ball)
      (at_robot ?x)
    )
    :effect (and
      (at_ball ?x)
      (free_hand)
      (not (holding_ball))
      (increase (total-cost) 1)
    )
  )
  (:action move
    :parameters (?from ?to)
    :precondition (at_robot ?from)
    :effect (and
      (at_robot ?to)
      (not (at_robot ?from))
      (increase (total-cost) 2)
    )
  )
)