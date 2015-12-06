(deftemplate adjacent-countries (slot country) (multislot adjacent-to))
(deftemplate player-info (slot player) (slot armies) (multislot card-countries))
(deftemplate card (slot country) (slot type))
(deftemplate book-selection (multislot card-countries))

(defrule choose-if-select-book
  ?bs <- (phase book-select)
  (bookArmiesBonusList ?current $?)
  =>
  (retract ?bs)
  (if (>= ?current 10)
    then
      (assert (select-book True))
    else
      (assert (select-book False))
  )
)

(defrule build-book
  ?sb <- (select-book True)
  (card (country ?c1) (type ?t1))
  (card (country ?c2&~?c1) (type ?t2))
  (card (country ?c3&~?c2&~?c1) (type ?t3))
  (or
    (test(eq ?t1 ?t2 ?t3))
    (and
      (test(neq ?t1 ?t2))
      (test(neq ?t2 ?t3))
    )
    (test(eq wild ?t1))
    (test(eq wild ?t2))
    (test(eq wild ?t3))
  )
  =>
  (retract ?sb)
  (assert (book-selection (card-countries ?c1 ?c2 ?c3)))
)

(defrule not-selecting-book
  ?sb <- (select-book False)
  =>
  (printout t "[]")
)

(defrule return-book-selection
  (book-selection (card-countries ?c1 ?c2 ?c3))
  =>
  (format t "['%s', '%s', '%s']" ?c1 ?c2 ?c3)
)
