; Construct a pyramid using the blocks in the bag.
;
; Goal:
;     B3
;   XX--B2
; XX--XX--B1
;
(define (problem block-test-2)
  (:domain stacking-domain)
  (:objects b1 b2 b3 b4 b5 b6)
  (:init (empty-hand) (in-bag b1) (in-bag b2) (in-bag b3) (in-bag b4) (in-bag b5) (in-bag b6))
  (:goal (and (on-table b1) (on-left b2 b1) (on-left b3 b2))))

