(define (problem multiple_moves)
  (:domain gripper)
  
  (:objects
    roomA roomB roomC roomD
  )
  
  (:init
    (at_ball roomA)
    (at_robot roomD)
    (free_hand)  )
  
  (:goal
    (and
      (at_ball roomC)
      (at_robot roomB)    )
  )
)