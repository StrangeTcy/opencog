;; Shared variables for all terms
(define atomese-variable-template
  (list (TypedVariable (Variable "$S") (Type "SentenceNode"))
        (TypedVariable (Variable "$P") (Type "ParseNode"))))

;; Shared conditions for all terms
(define atomese-condition-template
  (list (Parse (Variable "$P") (Variable "$S"))
        (State ghost-anchor (Variable "$S"))))

(define (order-terms TERMS)
  "Order the terms in the intended order, and insert wildcards into
   appropriate positions of the sequence.
   No operation is needed if the pattern is supposed to be matched in
   any order."
  (let* ((as (cons 'anchor-start "<"))
         (ae (cons 'anchor-end ">"))
         (wc (cons 'wildcard (cons 0 -1)))
         (unordered? (any (lambda (t) (equal? 'unordered-matching (car t))) TERMS))
         (start-anchor? (any (lambda (t) (equal? as t)) TERMS))
         (end-anchor? (any (lambda (t) (equal? ae t)) TERMS))
         (start (if start-anchor? (cdr (member as TERMS)) (list wc)))
         (end (if end-anchor?
                  (take-while (lambda (t) (not (equal? ae t))) TERMS)
                  (list wc))))
        (cond (unordered? TERMS)  ; Nothing needs to be done
              ((and start-anchor? end-anchor?)
               (if (equal? start-anchor? end-anchor?)
                   ; If they are equal, we are not expecting
                   ; anything else, either one of them is
                   ; the whole sequence
                   (drop-right start 1)
                   ; If they are not equal, put a wildcard
                   ; in between them
                   (append start (list wc) end)))
               ; If there is only a start-anchor, append it and
               ; a wildcard with the main-seq
              (start-anchor?
               (let ((before-anchor-start
                       (take-while (lambda (t) (not (equal? as t))) TERMS)))
                    (if (null? before-anchor-start)
                        (append start end)
                        ; In case there are terms before anchor-start,
                        ; get it and add an extra wildcard
                        (append start (list wc) before-anchor-start end))))
              ; If there is only an end-anchor, the main-seq should start
              ; with a wildcard, follow by another wildcard and finally
              ; the end-seq
              (end-anchor?
               (let ((after-anchor-end (cdr (member ae TERMS))))
                    (if (null? after-anchor-end)
                        (append start end)
                        ; In case there are still terms after anchor-end,
                        ; get it and add an extra wildcard
                        (append start after-anchor-end (list wc) end))))
              ; If there is no anchor, the main-seq should start and
              ; end with a wildcard
              (else (append (list wc) TERMS (list wc))))))

(define (process-pattern-terms TERMS)
  "Generate the atomese (i.e. the variable declaration and the pattern)
   for each of the TERMS."
  (define is-unordered? #f)
  (define (process terms)
    (define v '())
    (define c '())
    (define ws '())
    (define ls '())
    (define (update-lists t)
      (set! v (append v (list-ref t 0)))
      (set! c (append c (list-ref t 1)))
      (set! ws (append ws (list-ref t 2)))
      (set! ls (append ls (list-ref t 3))))
    (for-each (lambda (t)
      (cond ((equal? 'unordered-matching (car t))
             (update-lists (process (cdr t)))
             (set! is-unordered? #t))
            ((equal? 'word (car t))
             (update-lists (word (cdr t))))
            ((equal? 'lemma (car t))
             (update-lists (lemma (cdr t))))
            ((equal? 'phrase (car t))
             (update-lists (phrase (cdr t))))
            ((equal? 'concept (car t))
             (update-lists (concept (cdr t))))
            ((equal? 'choices (car t))
             (update-lists (choices (cdr t))))
            ((equal? 'negation (car t))
             (update-lists (negation (cdr t))))
            ((equal? 'wildcard (car t))
             (update-lists (wildcard (cadr t) (cddr t))))
            ((equal? 'variable (car t))
             (update-lists (process (cdr t)))
             (set! pat-vars (append pat-vars (last-pair ws))))
            ((equal? 'uvar_exist (car t))
             (set! conds (append conds (list (uvar-exist? (cdr t))))))
            ((equal? 'uvar_equal (car t))
             (set! conds (append conds (list (uvar-equal? (cadr t) (caddr t))))))
            ((equal? 'function (car t))
             (set! conds (append conds
               (list (context-function (cadr t)
                 (map (lambda (a)
                   (cond ((equal? 'get_wvar (car a))
                          (list-ref pat-vars (cdr a)))
                         ((equal? 'get_lvar (car a))
                          (get-var-lemmas (list-ref pat-vars (cdr a))))
                         ((equal? 'get_uvar (car a))
                          (get-user-variable (cdr a)))
                         (else (WordNode (cdr a)))))
                   (cddr t)))))))
            ((equal? 'sequence (car t))
             (let ((pt (process (cdr t))))
                  ; Wrap the sequences with a ListLink
                  (list-set! pt 2 (list (List (list-ref pt 2))))
                  (list-set! pt 3 (list (List (list-ref pt 3))))
                  (update-lists pt)))
            (else (feature-not-supported (car t) (cdr t)))))
      terms)
    (list v c ws ls))

  (define (generate-eval pred seq)
    ; If there is a ListLink in seq, e.g.
    ; ((Word "good") (Word "to") (List (Word "see") (Word "you")))
    ; get the outgoing set of it.
    (define proc-seq
      (map
        (lambda (s)
          (if (equal? 'ListLink (cog-type s))
            (cog-outgoing-set s)
            s))
        seq))
    (Evaluation pred (List (Variable "$S") (List proc-seq))))

  ; Start the processing
  (define terms (process TERMS))
  (define vars (list-ref terms 0))
  (define conds (list-ref terms 1))
  (define word-seq (list-ref terms 2))
  (define lemma-seq (list-ref terms 3))

  (if is-unordered?
      ; Generate an EvaluationLink for each of the term in the seq
      ; if it's an unordered match
      (begin
        (for-each
          (lambda (t)
            (let ((wc (wildcard 0 -1)))
              (set! vars (append vars (list-ref wc 0)))
              (set! conds (append conds (list (generate-eval ghost-word-seq
                (list (car (list-ref wc 2)) t (car (list-ref wc 3)))))))))
          word-seq)
        (for-each
          (lambda (t)
            (let ((wc (wildcard 0 -1)))
              (set! vars (append vars (list-ref wc 0)))
              (set! conds (append conds (list (generate-eval ghost-lemma-seq
                (list (car (list-ref wc 2)) t (car (list-ref wc 3)))))))))
          lemma-seq))
      ; Otherwise it's an ordered match
      (set! conds (append conds (list
        (generate-eval ghost-word-seq word-seq)
        (generate-eval ghost-lemma-seq lemma-seq)))))

  ; DualLink couldn't match patterns with no constant terms in it
  ; Mark the rules with no constant terms so that they can be found
  ; easily during the matching process
  (if (equal? (length lemma-seq)
              (length (filter (lambda (x) (equal? 'GlobNode (cog-type x)))
                              lemma-seq)))
      (MemberLink (List lemma-seq) ghost-no-constant))

  (list vars conds))

(define (process-action ACTION)
  "Convert ACTION into atomese."
  (define reuse #f)
  (define (to-atomese actions)
    (define choices '())
    (append
      ; Iterate through the output word-by-word
      (map (lambda (n)
        (cond ; Gather all the action choices, i.e. a list of actions
              ; available but only one of them will be executed
              ((equal? 'action-choices (car n))
               (set! choices (append choices (list (List (to-atomese (cdr n))))))
               '())
              ; Generate the DefinedSchema once we have finished going through
              ; all the choices
              ((not (null? choices))
               (let ((ac (action-choices choices)))
                    (set! choices '())
                    ; Generate the atoms for the current one
                    (append (list ac) (to-atomese (list n)))))
              ; The grounding of a variable in original words
              ((equal? 'get_wvar (car n))
               (list-ref pat-vars (cdr n)))
              ; The grounding of a variable in lemmas
              ((equal? 'get_lvar (car n))
               (get-var-lemmas (list-ref pat-vars (cdr n))))
              ; Get the value of a user variable
              ((equal? 'get_uvar (car n)) (get-user-variable (cdr n)))
              ; Assign a value to a user variable
              ((equal? 'assign_uvar (car n))
               (set-user-variable (cadr n) (car (to-atomese (cddr n)))))
              ; A function call
              ((equal? 'function (car n))
               (if (equal? "reuse" (cadr n)) (set! reuse #t))
               (action-function (cadr n) (to-atomese (cddr n))))
              (else (Word (cdr n)))))
        actions)
      (if (null? choices)
          '()
          (list (action-choices choices)))))
  (define action-atomese (to-atomese (cdar ACTION)))
  (True (if reuse action-atomese
                  (ExecutionOutput (GroundedSchema "scm: ghost-execute-action")
                                   (List action-atomese)))))

(define (process-goal GOAL)
  "Go through each of the goals, including the shared ones."
  (if (null? GOAL)
      (list (cons (ghost-prefix "Default Goal") 0.9))
      ; The shared goals will be overwritten if the same goal is specified
      ; to this rule
      (append GOAL
        (remove (lambda (sg) (any (lambda (g) (equal? (car sg) (car g))) GOAL))
                shared-goals))))

(define (create-rule PATTERN ACTION GOAL TOPIC NAME)
  "Top level translation function. Pattern is a quoted list of terms,
   and action is a quoted list of actions or a single action."
  (cog-logger-debug "In create-rule\nPATTERN = ~a\nACTION = ~a" PATTERN ACTION)
  (let* ((ordered-terms (order-terms PATTERN))
         (proc-terms (process-pattern-terms ordered-terms))
         (vars (append atomese-variable-template (list-ref proc-terms 0)))
         (conds (append atomese-condition-template (list-ref proc-terms 1)))
         (action (process-action ACTION))
         (goals (process-goal GOAL)))
        (set! pat-vars '())
        (cog-logger-debug ghost-logger "Context: ~a" ordered-terms)
        (cog-logger-debug ghost-logger "Procedure: ~a" ACTION)
        (cog-logger-debug ghost-logger "Goal(s): ~a" goals)
        (map (lambda (goal)
               (psi-rule
                 (list (Satisfaction (VariableList vars) (And conds)))
                 action
                 (psi-goal (car goal))
                 (stv (cdr goal) .9)
                 (if (null? TOPIC) default-topic TOPIC)
                 NAME))
             goals)))

; ----------
; Topic
; ----------
(define default-topic '())

(define-public (create-topic TOPIC-NAME)
"
  create-topic TOPIC-NAME

  Creates a psi-demand named as TOPIC-NAME, sets the default-topic to be it
  and returns ConceptNode that represent the topic(aka demand).
"
  ; NOTE:The intention is to follow chatscript like authoring approach. Once a
  ; topic is created, then the rules that are added after that will be under
  ; that topic.

  ; TODO:
  ; 1. Should this be a skipped demand, so as to separate the dialogue loop
  ; be independent of the psi-loop? Or, is it better to resturcture openpsi to
  ; allow as many loops as possilbe as that might be required for the DMT
  ; implementation?
  ; 2. Should the weight be accessable? Specially if the execution graph is
  ; separate from the content, thus allowing learing, why?

  (set! default-topic (psi-demand TOPIC-NAME))
  default-topic)

; This is the default topic.
(create-topic "Yakking")
