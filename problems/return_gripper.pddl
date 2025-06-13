(define (problem return_gripper)
  (:domain gripper)
  
  (:objects
    roomA roomB
  )
  
  (:init
    (at_ball roomB)
    (at_robot roomA)
    (free_hand)  )
  
  (:goal
    (and
      (at_ball roomA)
      (at_robot roomA)    )
  )
)