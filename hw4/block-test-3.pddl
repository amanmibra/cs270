; Destruct a pyramid.
;
; Initial State:
;     B6
;   B4--B5
; B1--B2--B3
;
; Goal:
; B6--B5--B4--B3--B2--B1
;
(define (problem block-test-3)
  (:domain stacking-domain)
  (:objects b1 b2 b3 b4 b5 b6)
  (:init (empty-hand) 
    (on-table b1) (nothing-to-left b1) (left-clear b1) (touching b1 b2)
    (on-table b2) (touching b2 b3) 
    (on-table b3) (nothing-to-right b3) (right-clear b3) 
    (on-right b4 b1) (on-left b4 b2) (nothing-to-left b4) (left-clear b4) (touching b4 b5) 
    (on-right b5 b2) (on-left b5 b3) (nothing-to-right b5) (right-clear b5)
    (on-right b6 b4) (on-left b6 b5) (nothing-to-left b6) (nothing-to-right b6) (left-clear b6) (right-clear b6) 
  )
  (:goal (and (touching b6 b5) (touching b5 b4) (touching b4 b3) (touching b3 b2) (touching b2 b1))))
