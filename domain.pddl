(define (domain gripper)

  (:requirements :strips)

  (:predicates
    (at_ball ?x)        ;; La balle est dans la pièce ?x
    (at_robot ?x)       ;; Le robot est dans la pièce ?x
    (free_hand)         ;; La main est libre
    (holding_ball)      ;; Le robot tient la balle
  )

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
    )
  )

  (:action move
    :parameters (?from ?to)
    :precondition (at_robot ?from)
    :effect (and
      (at_robot ?to)
      (not (at_robot ?from))
    )
  )
)
