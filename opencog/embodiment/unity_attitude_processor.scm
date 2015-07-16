;
; @file embodiment/unity_attitude_processor.scm
;
; @author Troy Huang <huangdeheng@gmail.com>
;
; This module processes the avatar's attitudes that are generated by event 
; responder by applying the changes on its own feeling level.
;
; e.g. anger or fear level might be amplified if being harmed by other avatars, 
; anger might be suppressed if the avatar is interacting with its owner, etc.
;
; Currently, the appraisal for the stimulus is based on rules. But once 
; incorporating learning algorithms like fishgram(sushigram etc.), hopefully
; we can make the avatar learn rules based on experience.
;
; According to the table that mapping modulator to feelings in  
; embodiment/feeling_updaters.scm, we can have following reversal mapping for 
; attitude to make impact on modulators.
;       
;   Attitude      ||    Activation    Resolution    SecuringThreshold    SelectionThreshold    Pleasure
;  ======================================================================================================
;   anger         ||        U             D                U                      D                D
;  ------------------------------------------------------------------------------------------------------ 
;   fear          ||        U             D                D                      U                D
;  ------------------------------------------------------------------------------------------------------ 
;   happiness     ||        U             D                U                      U                U
;  ------------------------------------------------------------------------------------------------------ 
;   sadness       ||        D             U                D                      D                D
;  ------------------------------------------------------------------------------------------------------ 
;   pride         ||                      D                U                      U                U
;  ------------------------------------------------------------------------------------------------------ 
;   love          ||                      DD               UU                     UU               UU
;  ------------------------------------------------------------------------------------------------------ 
;   hate          ||        UU            DD               UU                                      DD
;  ------------------------------------------------------------------------------------------------------ 
;   gratitude     ||                                                              U                U
;
;   ( U = Up, D = Down, UU = Up Up, DD = Down Down )

(define LATEST_STIMULUS_TIMESTAMP 0)
(define attitude_to_modulator_impact_func_map (list))

(define (get_latest_stimulus_timestamp)
    LATEST_STIMULUS_TIMESTAMP
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Interface to be invoked
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
(define (do_attitude_processing timestamp)
    (let* (
             (attitude_link_list
                (unpack_query_result (retrieve_attitudes timestamp))
             )
          )

         (begin 
            (map-in-order
                (lambda (attitude_eval_link)
                    (let* ( (intensity (get_truth_value_mean (cog-tv attitude_eval_link)))
                            ; get the list link that contains the detail of this attitude, e.g.
                            ; attitude target, attitude type
                            (attitude_detail_link (list-ref (cog-outgoing-set attitude_eval_link) 1))
                            ; get attitude type from attitude detail link
                            (attitude_type (list-ref (cog-outgoing-set attitude_detail_link) 2))
                          )

                        (map-in-order
                            (lambda (impact_func)
                                (impact_func intensity)
                            ); lambda

                            (get_impact_func_from_map (cog-name attitude_type) )
                        ); map-in-order
                    ); let*
                ); lambda

                attitude_link_list
            ); map-in-order

            attitude_link_list
        ); begin

        ; If any stimulus is processed, record the latest timestamp
        (if (not (null? attitude_link_list) )
            (set! LATEST_STIMULUS_TIMESTAMP timestamp)
        ); if
    ); let*
)

; Get a list of methods that maps to 
(define (get_impact_func_from_map attitude_type)
    (if 
        (list? (assoc attitude_type attitude_to_modulator_impact_func_map))
        (car (cdr (assoc attitude_type attitude_to_modulator_impact_func_map)))
        (list)
    )
)

; Retrieve all evaluation links for attitude with a given timestamp
(define (retrieve_attitudes timestamp)
    (cog-bind
        (BindLink
            (ListLink
                (VariableNode "$var_attitude")
                (VariableNode "$var_target")
            )

            ; Pattern
            (AtTimeLink
                (TimeNode (number->string timestamp))
                (EvaluationLink
                    (PredicateNode "attitude_towards")
                    (ListLink
                        PET_HANDLE
                        (VariableNode "$var_target")
                        (VariableNode "$var_attitude")
                    )
                )
            )

            ; Result
            (EvaluationLink
                (PredicateNode "attitude_towards")
                (ListLink
                    PET_HANDLE
                    (VariableNode "$var_target")
                    (VariableNode "$var_attitude")
                )
            )
        ); BindLink
    ); cog-bind
)

;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;
;;; Mapping attitude to modulator value
;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;

(define (attitude_impact_on_modulator stimulus_name 
                                      impact_factor 
        )
        
        (let* ( 
                ; get latest modulator value by its name
                (latest_stimulus_value 
                    (get_predicate_truth_value_mean stimulus_name)
                ) 

                ; set the updated value by applying impact factor
                (updated_value (+ latest_stimulus_value impact_factor))
              )
              
              ; renew the stimulus value by adding change
              (set_predicate_truth_value stimulus_name 
                  (cog-new-stv updated_value 1.0)
              )
        ); let*
)

(define (modulator_impact activation_impact_factor
                          resolution_impact_factor
                          securing_threshold_impact_factor
                          selection_threshold_impact_factor
                          pleasure_impact_factor

                          intensity
        )

        (let 
             ; Here we should scale the intensity by dividing 2 in order to
             ; limit the range of stimulus in [0, 1]
             ( (scale_intensity (/ intensity 2))
             )

              (attitude_impact_on_modulator 
                  "ActivationStimulus"
                  (* activation_impact_factor scale_intensity)
              )

              (attitude_impact_on_modulator
                  "ResolutionStimulus" 
                  (* resolution_impact_factor scale_intensity)
              )

              (attitude_impact_on_modulator 
                  "SecuringThresholdStimulus" 
                  (* securing_threshold_impact_factor scale_intensity)
              )

              (attitude_impact_on_modulator 
                  "SelectionThresholdStimulus" 
                  (* selection_threshold_impact_factor scale_intensity)
              )

              (attitude_impact_on_modulator 
                  "PleasureStimulus"
                  (* pleasure_impact_factor scale_intensity)
              )
        ); let
)

; Specific attitude to apply changes on modulator
(define (angerModulatorImpact intensity)
    (modulator_impact 0.35
                      -0.4
                      0.3
                      -0.35
                      -0.5

                      intensity
    )
)

(define (loveModulatorImpact intensity)
    (modulator_impact 0
                      -0.4
                      0.4
                      0.4
                      0.4

                      intensity
    )
)

(define attitude_to_modulator_impact_func_map
    ; this association list contains mapping from attitude name to modulator impacting method
    (list
        ; The format is: (action_name (list rule1 rule2 ...))
        (list "angry" (list angerModulatorImpact) )
        (list "love"  (list loveModulatorImpact) )
    )
)