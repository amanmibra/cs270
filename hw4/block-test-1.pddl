; Reverse the order of blocks in a row.
;
; Initial State:
; B1--B2--B3--B4
;
; Goal:
; B4--B3--B2--B1
;
(define (problem block-test-1)
  (:domain stacking-domain)
  (:objects b1 b2 b3 b4)
  (:init (empty-hand) 
    (on-table b1) (nothing-to-left b1) (left-clear b1) (right-clear b1) (touching b1 b2) 
    (on-table b2) (left-clear b2) (right-clear b2) (touching b2 b3)
    (on-table b3) (left-clear b3) (right-clear b3) (touching b3 b4)
    (on-table b4) (nothing-to-right b4) (left-clear b4) (right-clear b4)
  )
  (:goal (and (touching b4 b3) (touching b3 b2) (touching b2 b1))))
