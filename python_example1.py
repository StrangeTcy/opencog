from opencog.atomspace import AtomSpace, TruthValue
from opencog.atomspace import types
from opencog.scheme_wrapper import scheme_eval_h, scheme_eval_as

stuff = "stuff"

# Get the atomspace that guile is using
asp = scheme_eval_as('(cog-atomspace)') 

# Add a node to the atomspace
TV = TruthValue(0.42, 0.69)
a1 = asp.add_node(types.ConceptNode, 'Apple', TV)

stuff = asp

# Get the same atom, from guile's point of view:
#a2 = scheme_eval_h('(cog-node \'ConceptNode "Apple")', stuff)
a2 = scheme_eval_h(stuff, '(cog-node \'ConceptNode "Apple")')

# Print true if they are the same atom.  They should be!
print ("Are they equal?")
print("Yes") if a1 == a2 else print ("No, for some reason")