(define (problem round_trip)
  (:domain gripper)
  
  (:objects
    roomA roomB
  )
  
  (:init
    (at_ball roomA)
    (at_robot roomA)
    (free_hand)  )
  
  (:goal
    (and
      (at_ball roomA)
      (at_robot roomA)
      (free_hand)    )
  )
)