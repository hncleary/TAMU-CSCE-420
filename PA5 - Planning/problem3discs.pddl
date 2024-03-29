; Problem description
; Describe one scenario within the domain constraints
; This one describes the Star Problem with 3 discs
(define (problem starProblem3Discs)
  (:domain starProblem)

  ; Objects are candidates to replace free variables
  (:objects pegA pegB pegC pegO d1 d2 d3)

  ; The initial state describe what is currently true
  ; Everything else is considered false
  (:init

    (currentCenterPiece pegO)

    ; Discs are smaller than pegs
    (smaller d1 pegA) (smaller d1 pegB) (smaller d1 pegC) (smaller d1 pegO)
    (smaller d2 pegA) (smaller d2 pegB) (smaller d2 pegC) (smaller d2 pegO)
    (smaller d3 pegA) (smaller d3 pegB) (smaller d3 pegC) (smaller d3 pegO)
    ; Discs are also smaller than some other discs
    (smaller d1 d2) ;disc one is smaller than disc two
    (smaller d1 d3) ;disc one is smaller than disc three
    (smaller d2 d3) ;disc two is smaller than disc three

    ; There is nothing on top of some pegs and disc
    (clear pegB) ;peg B is empty
    (clear pegC) ;peg C is empty
    (clear pegO) ;peg O is empty
    (clear d1)   ;there is not a disc on top of disc one

    ; Discs are stacked on peg1
    (on d3 pegA) ;disc three is on peg A
    (on d2 d3)   ;disc two is on disc three
    (on d1 d2)   ;disc one is on disc 2
  )

  ; The goal state describe what we desire to achieve
  (:goal (and
    ; Discs stacked on peg3
    (on d3 pegC)
    (on d2 d3)
    (on d1 d2)
  ))
)
