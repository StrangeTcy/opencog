# This file was automatically generated by SWIG (http://www.swig.org).
# Version 3.0.10
#
# Do not make changes to this file unless you know what you are doing--modify
# the SWIG interface file instead.





from sys import version_info as _swig_python_version_info
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_clinkgrammar')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_clinkgrammar')
    _clinkgrammar = swig_import_helper()
    del swig_import_helper
elif _swig_python_version_info >= (2, 6, 0):
    def swig_import_helper():
        from os.path import dirname
        import imp
        fp = None
        try:
            fp, pathname, description = imp.find_module('_clinkgrammar', [dirname(__file__)])
        except ImportError:
            import _clinkgrammar
            return _clinkgrammar
        if fp is not None:
            try:
                _mod = imp.load_module('_clinkgrammar', fp, pathname, description)
            finally:
                fp.close()
            return _mod
    _clinkgrammar = swig_import_helper()
    del swig_import_helper
else:
    import _clinkgrammar
del _swig_python_version_info
try:
    _swig_property = property
except NameError:
    pass  # Python < 2.2 doesn't have 'property'.

try:
    import builtins as __builtin__
except ImportError:
    import __builtin__

def _swig_setattr_nondynamic(self, class_type, name, value, static=1):
    if (name == "thisown"):
        return self.this.own(value)
    if (name == "this"):
        if type(value).__name__ == 'SwigPyObject':
            self.__dict__[name] = value
            return
    method = class_type.__swig_setmethods__.get(name, None)
    if method:
        return method(self, value)
    if (not static):
        if _newclass:
            object.__setattr__(self, name, value)
        else:
            self.__dict__[name] = value
    else:
        raise AttributeError("You cannot add attributes to %s" % self)


def _swig_setattr(self, class_type, name, value):
    return _swig_setattr_nondynamic(self, class_type, name, value, 0)


def _swig_getattr(self, class_type, name):
    if (name == "thisown"):
        return self.this.own()
    method = class_type.__swig_getmethods__.get(name, None)
    if method:
        return method(self)
    raise AttributeError("'%s' object has no attribute '%s'" % (class_type.__name__, name))


def _swig_repr(self):
    try:
        strthis = "proxy of " + self.this.__repr__()
    except __builtin__.Exception:
        strthis = ""
    return "<%s.%s; %s >" % (self.__class__.__module__, self.__class__.__name__, strthis,)

try:
    _object = object
    _newclass = 1
except __builtin__.Exception:
    class _object:
        pass
    _newclass = 0

lg_Fatal = _clinkgrammar.lg_Fatal
lg_Error = _clinkgrammar.lg_Error
lg_Warn = _clinkgrammar.lg_Warn
lg_Info = _clinkgrammar.lg_Info
lg_Debug = _clinkgrammar.lg_Debug
lg_Trace = _clinkgrammar.lg_Trace
lg_None = _clinkgrammar.lg_None
class lg_errinfo(_object):
    __swig_setmethods__ = {}
    __setattr__ = lambda self, name, value: _swig_setattr(self, lg_errinfo, name, value)
    __swig_getmethods__ = {}
    __getattr__ = lambda self, name: _swig_getattr(self, lg_errinfo, name)
    __repr__ = _swig_repr
    __swig_getmethods__["severity"] = _clinkgrammar.lg_errinfo_severity_get
    if _newclass:
        severity = _swig_property(_clinkgrammar.lg_errinfo_severity_get)
    __swig_getmethods__["severity_label"] = _clinkgrammar.lg_errinfo_severity_label_get
    if _newclass:
        severity_label = _swig_property(_clinkgrammar.lg_errinfo_severity_label_get)
    __swig_getmethods__["text"] = _clinkgrammar.lg_errinfo_text_get
    if _newclass:
        text = _swig_property(_clinkgrammar.lg_errinfo_text_get)

    def formatmsg(self):
        return _lg_error_formatmsg(self)
    __swig_destroy__ = _clinkgrammar.delete_lg_errinfo
    __del__ = lambda self: None


    def __init__(self):
        this = _clinkgrammar.new_lg_errinfo()
        try:
            self.this.append(this)
        except __builtin__.Exception:
            self.this = this
lg_errinfo_swigregister = _clinkgrammar.lg_errinfo_swigregister
lg_errinfo_swigregister(lg_errinfo)

VDAL = _clinkgrammar.VDAL
CORPUS = _clinkgrammar.CORPUS
NO_DISPLAY = _clinkgrammar.NO_DISPLAY
MULTILINE = _clinkgrammar.MULTILINE
BRACKET_TREE = _clinkgrammar.BRACKET_TREE
SINGLE_LINE = _clinkgrammar.SINGLE_LINE
MAX_STYLES = _clinkgrammar.MAX_STYLES

def linkgrammar_get_version() -> "char const *":
    return _clinkgrammar.linkgrammar_get_version()
linkgrammar_get_version = _clinkgrammar.linkgrammar_get_version

def linkgrammar_get_dict_version(dict: 'Dictionary') -> "char const *":
    return _clinkgrammar.linkgrammar_get_dict_version(dict)
linkgrammar_get_dict_version = _clinkgrammar.linkgrammar_get_dict_version

def linkgrammar_get_dict_locale(dict: 'Dictionary') -> "char const *":
    return _clinkgrammar.linkgrammar_get_dict_locale(dict)
linkgrammar_get_dict_locale = _clinkgrammar.linkgrammar_get_dict_locale

def dictionary_create_lang(lang: 'char const *') -> "Dictionary":
    return _clinkgrammar.dictionary_create_lang(lang)
dictionary_create_lang = _clinkgrammar.dictionary_create_lang

def dictionary_create_default_lang() -> "Dictionary":
    return _clinkgrammar.dictionary_create_default_lang()
dictionary_create_default_lang = _clinkgrammar.dictionary_create_default_lang

def dictionary_get_lang(dict: 'Dictionary') -> "char const *":
    return _clinkgrammar.dictionary_get_lang(dict)
dictionary_get_lang = _clinkgrammar.dictionary_get_lang

def dictionary_delete(dict: 'Dictionary') -> "void":
    return _clinkgrammar.dictionary_delete(dict)
dictionary_delete = _clinkgrammar.dictionary_delete

def dictionary_set_data_dir(path: 'char const *') -> "void":
    return _clinkgrammar.dictionary_set_data_dir(path)
dictionary_set_data_dir = _clinkgrammar.dictionary_set_data_dir

def dictionary_get_data_dir() -> "char *":
    return _clinkgrammar.dictionary_get_data_dir()
dictionary_get_data_dir = _clinkgrammar.dictionary_get_data_dir

def parse_options_create() -> "Parse_Options":
    return _clinkgrammar.parse_options_create()
parse_options_create = _clinkgrammar.parse_options_create

def parse_options_delete(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_delete(opts)
parse_options_delete = _clinkgrammar.parse_options_delete

def parse_options_set_verbosity(opts: 'Parse_Options', verbosity: 'int') -> "void":
    return _clinkgrammar.parse_options_set_verbosity(opts, verbosity)
parse_options_set_verbosity = _clinkgrammar.parse_options_set_verbosity

def parse_options_get_verbosity(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_verbosity(opts)
parse_options_get_verbosity = _clinkgrammar.parse_options_get_verbosity

def parse_options_set_linkage_limit(opts: 'Parse_Options', linkage_limit: 'int') -> "void":
    return _clinkgrammar.parse_options_set_linkage_limit(opts, linkage_limit)
parse_options_set_linkage_limit = _clinkgrammar.parse_options_set_linkage_limit

def parse_options_get_linkage_limit(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_linkage_limit(opts)
parse_options_get_linkage_limit = _clinkgrammar.parse_options_get_linkage_limit

def parse_options_set_disjunct_cost(opts: 'Parse_Options', disjunct_cost: 'double') -> "void":
    return _clinkgrammar.parse_options_set_disjunct_cost(opts, disjunct_cost)
parse_options_set_disjunct_cost = _clinkgrammar.parse_options_set_disjunct_cost

def parse_options_get_disjunct_cost(opts: 'Parse_Options') -> "double":
    return _clinkgrammar.parse_options_get_disjunct_cost(opts)
parse_options_get_disjunct_cost = _clinkgrammar.parse_options_get_disjunct_cost

def parse_options_set_min_null_count(opts: 'Parse_Options', null_count: 'int') -> "void":
    return _clinkgrammar.parse_options_set_min_null_count(opts, null_count)
parse_options_set_min_null_count = _clinkgrammar.parse_options_set_min_null_count

def parse_options_get_min_null_count(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_min_null_count(opts)
parse_options_get_min_null_count = _clinkgrammar.parse_options_get_min_null_count

def parse_options_set_max_null_count(opts: 'Parse_Options', null_count: 'int') -> "void":
    return _clinkgrammar.parse_options_set_max_null_count(opts, null_count)
parse_options_set_max_null_count = _clinkgrammar.parse_options_set_max_null_count

def parse_options_get_max_null_count(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_max_null_count(opts)
parse_options_get_max_null_count = _clinkgrammar.parse_options_get_max_null_count

def parse_options_set_islands_ok(opts: 'Parse_Options', islands_ok: 'int') -> "void":
    return _clinkgrammar.parse_options_set_islands_ok(opts, islands_ok)
parse_options_set_islands_ok = _clinkgrammar.parse_options_set_islands_ok

def parse_options_get_islands_ok(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_islands_ok(opts)
parse_options_get_islands_ok = _clinkgrammar.parse_options_get_islands_ok

def parse_options_set_short_length(opts: 'Parse_Options', short_length: 'int') -> "void":
    return _clinkgrammar.parse_options_set_short_length(opts, short_length)
parse_options_set_short_length = _clinkgrammar.parse_options_set_short_length

def parse_options_get_short_length(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_short_length(opts)
parse_options_get_short_length = _clinkgrammar.parse_options_get_short_length

def parse_options_set_max_memory(opts: 'Parse_Options', mem: 'int') -> "void":
    return _clinkgrammar.parse_options_set_max_memory(opts, mem)
parse_options_set_max_memory = _clinkgrammar.parse_options_set_max_memory

def parse_options_get_max_memory(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_max_memory(opts)
parse_options_get_max_memory = _clinkgrammar.parse_options_get_max_memory

def parse_options_set_max_parse_time(opts: 'Parse_Options', secs: 'int') -> "void":
    return _clinkgrammar.parse_options_set_max_parse_time(opts, secs)
parse_options_set_max_parse_time = _clinkgrammar.parse_options_set_max_parse_time

def parse_options_get_max_parse_time(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_max_parse_time(opts)
parse_options_get_max_parse_time = _clinkgrammar.parse_options_get_max_parse_time

def parse_options_set_cost_model_type(opts: 'Parse_Options', cm: 'Cost_Model_type') -> "void":
    return _clinkgrammar.parse_options_set_cost_model_type(opts, cm)
parse_options_set_cost_model_type = _clinkgrammar.parse_options_set_cost_model_type

def parse_options_get_cost_model_type(opts: 'Parse_Options') -> "Cost_Model_type":
    return _clinkgrammar.parse_options_get_cost_model_type(opts)
parse_options_get_cost_model_type = _clinkgrammar.parse_options_get_cost_model_type

def parse_options_timer_expired(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_timer_expired(opts)
parse_options_timer_expired = _clinkgrammar.parse_options_timer_expired

def parse_options_memory_exhausted(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_memory_exhausted(opts)
parse_options_memory_exhausted = _clinkgrammar.parse_options_memory_exhausted

def parse_options_resources_exhausted(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_resources_exhausted(opts)
parse_options_resources_exhausted = _clinkgrammar.parse_options_resources_exhausted

def parse_options_set_display_morphology(opts: 'Parse_Options', val: 'int') -> "void":
    return _clinkgrammar.parse_options_set_display_morphology(opts, val)
parse_options_set_display_morphology = _clinkgrammar.parse_options_set_display_morphology

def parse_options_get_display_morphology(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_display_morphology(opts)
parse_options_get_display_morphology = _clinkgrammar.parse_options_get_display_morphology

def parse_options_set_spell_guess(opts: 'Parse_Options', val: 'int') -> "void":
    return _clinkgrammar.parse_options_set_spell_guess(opts, val)
parse_options_set_spell_guess = _clinkgrammar.parse_options_set_spell_guess

def parse_options_get_spell_guess(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_spell_guess(opts)
parse_options_get_spell_guess = _clinkgrammar.parse_options_get_spell_guess

def parse_options_set_all_short_connectors(opts: 'Parse_Options', val: 'int') -> "void":
    return _clinkgrammar.parse_options_set_all_short_connectors(opts, val)
parse_options_set_all_short_connectors = _clinkgrammar.parse_options_set_all_short_connectors

def parse_options_get_all_short_connectors(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_all_short_connectors(opts)
parse_options_get_all_short_connectors = _clinkgrammar.parse_options_get_all_short_connectors

def parse_options_reset_resources(opts: 'Parse_Options') -> "void":
    return _clinkgrammar.parse_options_reset_resources(opts)
parse_options_reset_resources = _clinkgrammar.parse_options_reset_resources

def parse_options_set_use_sat_parser(opts: 'Parse_Options', val: 'int') -> "void":
    return _clinkgrammar.parse_options_set_use_sat_parser(opts, val)
parse_options_set_use_sat_parser = _clinkgrammar.parse_options_set_use_sat_parser

def parse_options_get_use_sat_parser(opts: 'Parse_Options') -> "int":
    return _clinkgrammar.parse_options_get_use_sat_parser(opts)
parse_options_get_use_sat_parser = _clinkgrammar.parse_options_get_use_sat_parser

def sentence_create(input_string: 'char const *', dict: 'Dictionary') -> "Sentence":
    return _clinkgrammar.sentence_create(input_string, dict)
sentence_create = _clinkgrammar.sentence_create

def sentence_delete(sent: 'Sentence') -> "void":
    return _clinkgrammar.sentence_delete(sent)
sentence_delete = _clinkgrammar.sentence_delete

def sentence_split(sent: 'Sentence', opts: 'Parse_Options') -> "int":
    return _clinkgrammar.sentence_split(sent, opts)
sentence_split = _clinkgrammar.sentence_split

def sentence_parse(sent: 'Sentence', opts: 'Parse_Options') -> "int":
    return _clinkgrammar.sentence_parse(sent, opts)
sentence_parse = _clinkgrammar.sentence_parse

def sentence_length(sent: 'Sentence') -> "int":
    return _clinkgrammar.sentence_length(sent)
sentence_length = _clinkgrammar.sentence_length

def sentence_null_count(sent: 'Sentence') -> "int":
    return _clinkgrammar.sentence_null_count(sent)
sentence_null_count = _clinkgrammar.sentence_null_count

def sentence_num_linkages_found(sent: 'Sentence') -> "int":
    return _clinkgrammar.sentence_num_linkages_found(sent)
sentence_num_linkages_found = _clinkgrammar.sentence_num_linkages_found

def sentence_num_valid_linkages(sent: 'Sentence') -> "int":
    return _clinkgrammar.sentence_num_valid_linkages(sent)
sentence_num_valid_linkages = _clinkgrammar.sentence_num_valid_linkages

def sentence_num_linkages_post_processed(sent: 'Sentence') -> "int":
    return _clinkgrammar.sentence_num_linkages_post_processed(sent)
sentence_num_linkages_post_processed = _clinkgrammar.sentence_num_linkages_post_processed

def sentence_num_violations(sent: 'Sentence', i: 'int') -> "int":
    return _clinkgrammar.sentence_num_violations(sent, i)
sentence_num_violations = _clinkgrammar.sentence_num_violations

def sentence_disjunct_cost(sent: 'Sentence', i: 'int') -> "double":
    return _clinkgrammar.sentence_disjunct_cost(sent, i)
sentence_disjunct_cost = _clinkgrammar.sentence_disjunct_cost

def sentence_link_cost(sent: 'Sentence', i: 'int') -> "int":
    return _clinkgrammar.sentence_link_cost(sent, i)
sentence_link_cost = _clinkgrammar.sentence_link_cost

def linkage_create(index: 'int', sent: 'Sentence', opts: 'Parse_Options') -> "Linkage":
    return _clinkgrammar.linkage_create(index, sent, opts)
linkage_create = _clinkgrammar.linkage_create

def linkage_delete(linkage: 'Linkage') -> "void":
    return _clinkgrammar.linkage_delete(linkage)
linkage_delete = _clinkgrammar.linkage_delete

def linkage_print_diagram(linkage: 'Linkage', display_walls: 'int', screen_width: 'size_t') -> "char *":
    return _clinkgrammar.linkage_print_diagram(linkage, display_walls, screen_width)
linkage_print_diagram = _clinkgrammar.linkage_print_diagram

def linkage_print_postscript(linkage: 'Linkage', display_walls: 'int', print_ps_header: 'int') -> "char *":
    return _clinkgrammar.linkage_print_postscript(linkage, display_walls, print_ps_header)
linkage_print_postscript = _clinkgrammar.linkage_print_postscript

def linkage_print_links_and_domains(linkage: 'Linkage') -> "char *":
    return _clinkgrammar.linkage_print_links_and_domains(linkage)
linkage_print_links_and_domains = _clinkgrammar.linkage_print_links_and_domains

def linkage_print_senses(linkage: 'Linkage') -> "char *":
    return _clinkgrammar.linkage_print_senses(linkage)
linkage_print_senses = _clinkgrammar.linkage_print_senses

def linkage_print_constituent_tree(linkage: 'Linkage', mode: 'ConstituentDisplayStyle') -> "char *":
    return _clinkgrammar.linkage_print_constituent_tree(linkage, mode)
linkage_print_constituent_tree = _clinkgrammar.linkage_print_constituent_tree

def linkage_print_disjuncts(linkage: 'Linkage const') -> "char *":
    return _clinkgrammar.linkage_print_disjuncts(linkage)
linkage_print_disjuncts = _clinkgrammar.linkage_print_disjuncts

def linkage_print_pp_msgs(linkage: 'Linkage') -> "char *":
    return _clinkgrammar.linkage_print_pp_msgs(linkage)
linkage_print_pp_msgs = _clinkgrammar.linkage_print_pp_msgs

def linkage_get_num_words(linkage: 'Linkage') -> "int":
    return _clinkgrammar.linkage_get_num_words(linkage)
linkage_get_num_words = _clinkgrammar.linkage_get_num_words

def linkage_get_num_links(linkage: 'Linkage') -> "int":
    return _clinkgrammar.linkage_get_num_links(linkage)
linkage_get_num_links = _clinkgrammar.linkage_get_num_links

def linkage_get_link_lword(linkage: 'Linkage', index: 'int') -> "int":
    return _clinkgrammar.linkage_get_link_lword(linkage, index)
linkage_get_link_lword = _clinkgrammar.linkage_get_link_lword

def linkage_get_link_rword(linkage: 'Linkage', index: 'int') -> "int":
    return _clinkgrammar.linkage_get_link_rword(linkage, index)
linkage_get_link_rword = _clinkgrammar.linkage_get_link_rword

def linkage_get_link_length(linkage: 'Linkage', index: 'int') -> "int":
    return _clinkgrammar.linkage_get_link_length(linkage, index)
linkage_get_link_length = _clinkgrammar.linkage_get_link_length

def linkage_get_link_label(linkage: 'Linkage', index: 'int') -> "char const *":
    return _clinkgrammar.linkage_get_link_label(linkage, index)
linkage_get_link_label = _clinkgrammar.linkage_get_link_label

def linkage_get_link_llabel(linkage: 'Linkage', index: 'int') -> "char const *":
    return _clinkgrammar.linkage_get_link_llabel(linkage, index)
linkage_get_link_llabel = _clinkgrammar.linkage_get_link_llabel

def linkage_get_link_rlabel(linkage: 'Linkage', index: 'int') -> "char const *":
    return _clinkgrammar.linkage_get_link_rlabel(linkage, index)
linkage_get_link_rlabel = _clinkgrammar.linkage_get_link_rlabel

def linkage_get_link_num_domains(linkage: 'Linkage', index: 'int') -> "int":
    return _clinkgrammar.linkage_get_link_num_domains(linkage, index)
linkage_get_link_num_domains = _clinkgrammar.linkage_get_link_num_domains

def linkage_get_link_domain_names(linkage: 'Linkage', index: 'int') -> "char const **":
    return _clinkgrammar.linkage_get_link_domain_names(linkage, index)
linkage_get_link_domain_names = _clinkgrammar.linkage_get_link_domain_names

def linkage_get_words(linkage: 'Linkage') -> "char const **":
    return _clinkgrammar.linkage_get_words(linkage)
linkage_get_words = _clinkgrammar.linkage_get_words

def linkage_get_word(linkage: 'Linkage', w: 'int') -> "char const *":
    return _clinkgrammar.linkage_get_word(linkage, w)
linkage_get_word = _clinkgrammar.linkage_get_word

def linkage_get_word_byte_start(linkage: 'Linkage', index: 'int') -> "int":
    return _clinkgrammar.linkage_get_word_byte_start(linkage, index)
linkage_get_word_byte_start = _clinkgrammar.linkage_get_word_byte_start

def linkage_get_word_byte_end(linkage: 'Linkage', index: 'int') -> "int":
    return _clinkgrammar.linkage_get_word_byte_end(linkage, index)
linkage_get_word_byte_end = _clinkgrammar.linkage_get_word_byte_end

def linkage_get_word_char_start(linkage: 'Linkage', index: 'int') -> "int":
    return _clinkgrammar.linkage_get_word_char_start(linkage, index)
linkage_get_word_char_start = _clinkgrammar.linkage_get_word_char_start

def linkage_get_word_char_end(linkage: 'Linkage', index: 'int') -> "int":
    return _clinkgrammar.linkage_get_word_char_end(linkage, index)
linkage_get_word_char_end = _clinkgrammar.linkage_get_word_char_end

def linkage_unused_word_cost(linkage: 'Linkage') -> "int":
    return _clinkgrammar.linkage_unused_word_cost(linkage)
linkage_unused_word_cost = _clinkgrammar.linkage_unused_word_cost

def linkage_disjunct_cost(linkage: 'Linkage') -> "double":
    return _clinkgrammar.linkage_disjunct_cost(linkage)
linkage_disjunct_cost = _clinkgrammar.linkage_disjunct_cost

def linkage_link_cost(linkage: 'Linkage') -> "int":
    return _clinkgrammar.linkage_link_cost(linkage)
linkage_link_cost = _clinkgrammar.linkage_link_cost

def linkage_corpus_cost(linkage: 'Linkage') -> "double":
    return _clinkgrammar.linkage_corpus_cost(linkage)
linkage_corpus_cost = _clinkgrammar.linkage_corpus_cost

def linkage_get_violation_name(linkage: 'Linkage') -> "char const *":
    return _clinkgrammar.linkage_get_violation_name(linkage)
linkage_get_violation_name = _clinkgrammar.linkage_get_violation_name

def _lg_error_formatmsg(lge: 'lg_errinfo') -> "char *":
    return _clinkgrammar._lg_error_formatmsg(lge)
_lg_error_formatmsg = _clinkgrammar._lg_error_formatmsg

def lg_error_clearall() -> "int":
    return _clinkgrammar.lg_error_clearall()
lg_error_clearall = _clinkgrammar.lg_error_clearall

def _prt_error(arg1: 'char const *', arg2: 'char const *') -> "int":
    return _clinkgrammar._prt_error(arg1, arg2)
_prt_error = _clinkgrammar._prt_error

def lg_error_flush() -> "int":
    return _clinkgrammar.lg_error_flush()
lg_error_flush = _clinkgrammar.lg_error_flush

def _py_error_default_handler(lge: 'lg_errinfo', pedh_data: 'int *') -> "void":
    return _clinkgrammar._py_error_default_handler(lge, pedh_data)
_py_error_default_handler = _clinkgrammar._py_error_default_handler

def _py_error_set_handler(func_and_data: 'PyObject *') -> "PyObject *":
    return _clinkgrammar._py_error_set_handler(func_and_data)
_py_error_set_handler = _clinkgrammar._py_error_set_handler

def _py_error_printall(func_and_data: 'PyObject *') -> "PyObject *":
    return _clinkgrammar._py_error_printall(func_and_data)
_py_error_printall = _clinkgrammar._py_error_printall

def delete_lg_errinfo(lge: 'lg_errinfo') -> "void":
    return _clinkgrammar.delete_lg_errinfo(lge)
delete_lg_errinfo = _clinkgrammar.delete_lg_errinfo
# This file is compatible with both classic and new-style classes.


