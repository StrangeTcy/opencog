from opencog.atomspace import AtomSpace, Atom, get_type, types
from copy import copy, deepcopy
from functools import *
import sys
from itertools import permutations
from util import *

class FakeHandle:
    '''A simple class to imitate Handle for use with FakeAtom.'''
    def __init__(self, id):
        self.id = id
    
    def value(self):
        return self.id

class FakeAtom:
    '''A simple pure Python class that can emulate the Cython Atom class. It supports pickling
    and is safe to use for Python multiprocessing. It is also compatible with PyPy.'''
    def __init__(self, type_name, name, id):
        self.type_name = type_name
        self.name = name
        self._handle = FakeHandle(id)
    
    def __str__(self):
        return 'fake%s%s' % (self.type_name,  self.name)

    def __eq__(self, other):
        return self._handle_value == other._handle_value

    def h(self):
        return self._handle

    def is_a(self, _type):
        assert _type == types.Link
        return False

def fake_from_real_Atom(atom):
    return FakeAtom(atom.type_name, atom.name, atom.h.value())

def tree_with_fake_atoms(tr):
    if isinstance(tr.op, Atom):
        return tree(fake_from_real_Atom(tr.op), [])
    elif tr.is_leaf():
        return tr
    else:
        return tree(tr.op, map(tree_with_fake_atoms, tr.args))


def coerce_tree(x):
    assert type(x) != type(None)
    if isinstance(x, tree):
        return x
    else:
        return tree(x)

class tree:
#    cdef public object op
#    cdef public list args
#    cdef tuple _tuple
    
    def __init__(self, op, *args):
        # Transparently allow using passing a list or using it in the more streamlined way
        # (better for constructing trees by hand)
        if len(args) and isinstance(args[0], list):
            args = args[0]
        # Transparently record Links as strings rather than Handles
        assert type(op) != type(None)
        if len(args):
            if isinstance(op, Atom):
                assert not op.is_a(types.Link)
                self.op = op.type_name
            else:
                self.op = op
            self.args = [coerce_tree(x) for x in args]
        else:
            self.op = op
            self.args = []
        
        self._tuple = None

    def __str__(self):
        if self.is_leaf():
            if isinstance(self.op, Atom):
                return self.op.name+':'+self.op.type_name
            else:
                return 'tree:'+str(self.op)
        else:
            return '(' + str(self.op) + ' '+ ' '.join(map(str, self.args)) + ')'

    # TODO add doctests
    def __repr__(self):
        # Display it as code to create the corresponding Atom
#        if self.is_variable():
#            return "a.add(t.VariableNode, name='$%s')" % (str(self.op),)
#        elif self.is_leaf() and isinstance(self.op, Atom):
#            # a.add(t.ConceptNode, name='cat')
#            return "a.add(t.%s, '%s')" % (self.op.type_name, self.op.name)
#        else:
#            # a.add(t.ListLink, out=[ a.add(t.ConceptNode, name='eat') ])
#            return "a.add(t.%s, out=%s)" % (self.op, repr(self.args))
        # Display it as code to create the Tree and required Nodes
        if self.is_variable():
            # e.g. T(123)
            return "T(%s)" % (str(int(self.op)),)
        elif self.is_leaf() and isinstance(self.op, Atom):
            # a.add(t.ConceptNode, name='cat')
            return "a.add(t.%s, '%s')" % (self.op.type_name, self.op.name)
        else:
            # T('ListLink', T(a.add(t.ConceptNode, name='eat')) )
            return "T('%s', %s)" % (self.op, repr(self.args))

    def __hash__(self):
        return hash( self.to_tuple() )

    def is_variable(self):
        "A variable is an int starting from 0"
        return isinstance(self.op, int)
    
    def get_type(self):
        if isinstance(self.op, int):
            return types.Atom
        elif isinstance(self.op, Atom):
            return self.op.t
        else:
            return get_type(self.op)
    
    def is_leaf(self):
        return len(self.args) == 0
    
    def __cmp__(self, other):
        if not isinstance(other, tree):
            return cmp(tree, type(other))
        #print self.to_tuple(), other.to_tuple()
        return cmp(self.to_tuple(), other.to_tuple())
    
    def to_tuple(self):
        # Simply cache the tuple.
        # TODO: A more efficient alternative would be to adapt the hash function and compare function
        # to work on Trees directly.
        if self._tuple != None:
            # Atom doesn't support comparing to different types in the Python-standard way.
            if isinstance(self.op, Atom):
                #assert type(self.op.h) != type(None)
                self._tuple = self.op.h.value()
                return self._tuple
                #return self.op.type_name+':'+self.op.name # Easier to understand, though a bit less efficient
            else:
                self._tuple = tuple([self.op]+[x.to_tuple() for x in self.args])
                return self._tuple

def tree_from_atom(atom, dic = {}):
    if atom.is_node():
        if atom.t in [types.VariableNode, types.FWVariableNode]:
            try:
                return dic[atom]
            except:
                var = new_var()
                dic[atom] = new_var()
                return var
        else:
            return tree(atom)
    else:
        args = [tree_from_atom(x, dic) for x in atom.out]
        return tree(atom.type_name, args)

def atom_from_tree(tree, a):
    if tree.is_variable():
        return a.add(types.VariableNode, name='$'+str(tree.op))
    elif tree.is_leaf():
        # Node (simply the handle)
        if isinstance (tree.op, Atom):
            return tree.op
        # Empty Link
        else:
            return a.add(get_type(tree.op), out = [])
    else:
        out = [atom_from_tree(x, a) for x in tree.args]
        return a.add(get_type(tree.op), out=out)

def find(template, atoms):
    return [a for a in atoms if unify(tree_from_atom(a), template, {}) != None]

class Match(object):
    def __init__(self, subst = {}, atoms = [], conj = ()):
        self.subst = subst
        self.atoms = atoms
        self.conj = conj
    
    def __eq__(self, other):
        return self.subst == other.subst and self.atoms == other.atoms and self.conj == other.conj

def find_conj(conj, atom_provider, match = Match()):
    """Find all combinations of Atoms matching the given conjunction.
    atom_provider can be either an AtomSpace or a list of Atoms.
    Returns a list of (unique) Match objects."""
    if conj == ():
        return [match]
    
    tr = conj[0]
    
    if isinstance(atom_provider, AtomSpace):
        root_type = tr.get_type()
        atoms = atomspace.get_atoms_by_type(root_type)
    else:
        atoms = atom_provider
    
    ret = []
    for a in atoms:
        s2 = unify(tr, tree_from_atom(a), match.subst)
        if s2 != None:
            match2 = Match(s2, match.atoms+[a])
            
            #print pp(match2.subst), pp(match2.atoms)
            
            later = find_conj(conj[1:], atoms, match2)
            
            for final_match in later:
                if final_match not in ret:
                    ret.append(final_match)
    return ret

def find_matching_conjunctions(conj, trees, match = Match()):
    if conj == ():
        #return [match]
        partially_bound_conj = subst_conjunction(match.subst, match.conj)
        m2 = Match(conj = partially_bound_conj, subst = match.subst)
        return [m2]
    
    ret = []
    for tr in trees:
        tr = standardize_apart(tr)
        s2 = unify(conj[0], tr, match.subst)
        if s2 != None:
            # partly_bound_tr is like conj[0] but with its variables replaced by the specific
            # values in this tree. e.g. if we were looking for:
            # (AtTimeLink tree:1000001 (EvaluationLink actionDone:PredicateNode (ListLink tree:1000003)))
            # we could get:
            # (AtTimeLink tree:1000005 (EvaluationLink actionDone:PredicateNode (ListLink
            #       (ExecutionLink eat:GroundedSchemaNode (ListLink tree:1000006)))))
            #partly_bound_tr = subst(s2, conj[0])
            match2 = Match(conj=match.conj+(conj[0],), subst=s2)
            
            #print pp(match2.conj), pp(match2.subst)
            
            later = find_matching_conjunctions(conj[1:], trees, match2)
            
            for final_match in later:
                if final_match not in ret:
                    ret.append(final_match)
    return ret

def apply_rule(precedent, conclusion, atoms):
    ret = []
    for x in atoms:
        if isinstance(x, Atom):
            x = tree_from_atom(x)
        s = unify(precedent, x, {})
        if s != None:
            ret.append( subst(s, conclusion) )
    return ret

# Further code adapted from AIMA-Python under the MIT License (see http://code.google.com/p/aima-python/)

def unify(x, y, s):
    """Unify expressions x,y with substitution s; return a substitution that
    would make x,y equal, or None if x,y can not unify. x and y can be
    variables (e.g. 1, Nodes, or tuples of the form ('link type name', arg0, arg1...)
    where arg0 and arg1 are any of the above. NOTE: If you unify two Links, they 
    must both be in tuple-tree format, and their variables must be standardized apart.
    If you use the vars_only flag, a variable can only unify to a corresponding variable.
    In other words, normally this function finds the most-general unification of two things;
    in this case they both have to be exactly as general as each other. Basically tree isomorphism or
    conjunction isomorphism.
    >>> ppsubst(unify(x + y, y + C, {}))
    {x: y, y: C}
    """
    #print "unify %s %s" % (str(x), str(y))

    if s == None:
        return None
    elif type(x) != type(y):
        return None
    elif x == y:
        return s
    elif isinstance(x, tree) and x.is_variable():
        return unify_var(x, y, s)
    elif isinstance(y, tree) and y.is_variable():
        return unify_var(y, x, s)
        
    elif isinstance(x, tree) and isinstance(y, tree):
        s2 = unify(x.op, y.op, s)
        return unify(x.args,  y.args, s2)

    # Recursion to handle arguments.
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        # unify all the arguments (works with any number of arguments, including 0)
        s2 = unify(x[0], y[0], s)
        return unify(x[1:], y[1:], s2)
        
    else:
        return None

def unify_var(var, x, s):
    if var in s:
        return unify(s[var], x, s)
    elif occur_check(var, x, s):
        return None
    else:
        return extend(s, var, x)

def occur_check(var, x, s):
    """Return true if variable var occurs anywhere in x
    (or in subst(s, x), if s has a binding for x)."""

    if x.is_variable() and var == x:
        return True
    elif x.is_variable() and s.has_key(x):
        return occur_check(var, s[x], s)
    # What else might x be? 
    elif not x.is_leaf():
        # Compare link type and arguments
#        return (occur_check(var, x.op, s) or # Not sure that's necessary
#                occur_check(var, x.args, s))
        return any([occur_check(var, a, s) for a in x.args])
    else:
        return False

def extend(s, var, val):
    """Copy the substitution s and extend it by setting var to val;
    return copy.
    
    >>> initial = {'x': 1}
    >>> extend({'x': 1}, 'y', 2)
    {'y': 2, 'x': 1}
    >>> initial
    {'x': 1}
    """
    s2 = s.copy()
    s2[var] = val
    return s2
    
def subst(s, x):
    """Substitute the substitution s into the expression x.
    >>> subst({x: 42, y:0}, F(x) + y)
    (F(42) + 0)
    """
#    if isinstance(x, Atom):
#        return x
#    elif x.is_variable(): 
#        # Notice recursive substitutions. i.e. $1->$2, $2->$3
#        # This recursion should also work for e.g. $1->foo($2), $2->bar
#        return subst(s, s.get(x, x))
    if x.is_variable():
        return s.get(x, x)
    elif x.is_leaf(): 
        return x
    else: 
        #return tuple([x[0]]+ [subst(s, arg) for arg in x[1:]])
        return tree(x.op, [subst(s, arg) for arg in x.args])

def subst_conjunction(substitution, conjunction):
    ret = []
    for tr in conjunction:
        ret.append(subst(substitution, tr))
    return tuple(ret)

def subst_from_binding(binding):
    return dict([ (tree(i), obj) for i, obj in enumerate(binding)])

def binding_from_subst(subst, atomspace):
    return [ atom_from_tree(obj_tree, atomspace) for (var, obj_tree) in sorted(subst.items()) ]

def bind_conj(conj, b):
    return subst_conjunction(subst_from_binding(b), conj)

def standardize_apart(tr, dic=None):
    """Replace all the variables in tree with new variables."""

    if dic == None:
        dic = {}

    if isinstance(tr, tuple):
        return tuple([standardize_apart(a, dic) for a in tr])
    elif tr.is_variable():
        if tr in dic:
            return dic[tr]
        else:
            v = new_var()
            dic[tr] = v
            return v
    else:
        return tree(tr.op, [standardize_apart(a, dic) for a in tr.args])

#def standardize_apart_subst(s, dic={}):
#    """Replace all the variables in subst with new variables."""
#    new_s = dict(
#                 ( (new_var(), new_var()) for (v1, v2) in s.items() )
#                 )

def new_var():
    global _new_var_counter
    _new_var_counter += 1
    return tree(_new_var_counter)

_new_var_counter = 10**6

def isomorphic_conjunctions(xs, ys):
    # Handle conjunctions.
    if isinstance(xs, tuple) and isinstance(ys, tuple) and len(xs) == len(ys):
        for perm in permutations(xs):
            if isomorphic_conjunctions_ordered(perm, ys):
                return True
    return False

def isomorphic_conjunctions_ordered(xs, ys):
    xs, ys = canonical_trees(xs), canonical_trees(ys)
    return xs == ys

def canonical_trees(trs, dic = {}):
    '''Returns the canonical version of this tree, i.e. with the variables renamed (consistently) from 0,1,2.'''
    tmp = new_var.counter
    new_var.counter = 0
    ret = []
    for tr in trs:
        tr = standardize_apart(tr)
        ret.append(tr)
    new_var.counter = tmp
    return tr

def get_varlist(t):
    """Return a list of variables in tree, in the order they appear (with depth-first traversal). Would also work on a conjunction."""
    if isinstance(t, tree) and t.is_variable():
        return [t]
    elif isinstance(t, tree):
        ret = []
        for arg in t.args:
            ret+=([x for x in get_varlist(arg) if x not in ret])
        return ret
    # Representing a conjunction as a tuple of trees.
    elif isinstance(t, tuple):
        ret = []
        for arg in t:
            ret+=([x for x in get_varlist(arg) if x not in ret])
        return ret
    else:
        return []


# These functions print their arguments in a standard order
# to compensate for the random order in the standard representation

def ppsubst(s):
    """Print substitution s"""
    ppdict(s)
