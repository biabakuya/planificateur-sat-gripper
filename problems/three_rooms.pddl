(define (problem three_rooms)
  (:domain gripper)
  
  (:objects
    roomA roomB roomC
  )
  
  (:init
    (at_ball roomA)
    (at_robot roomC)
    (free_hand)  )
  
  (:goal
    (and
      (at_ball roomB)    )
  )
)