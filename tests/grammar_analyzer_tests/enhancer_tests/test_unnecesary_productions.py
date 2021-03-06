from grammar_analyzer.enhancer.unnecesary_productions import remove_unnecesary_productions, remove_unreachable_prods, remove_unit_prods
from grammar_analyzer.enhancer.converter import graph_to_grammar, grammar_to_graph
from pycmp.parsing import compute_firsts
from pycmp.utils import ContainerSet
from pycmp.grammar import Grammar, Sentence, Production
from pycmp.grammar import Item


def test_remove_unreachable_prods():
    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= A
    S %= b

    A %= B

    B %= a

    C %= a

    new_grammar = remove_unreachable_prods(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["A"], ["b"]]
    _graph["A"] = [["B"]]
    _graph["B"] = [["a"]]

    assert new_grammar == _graph

    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= A + b
    S %= C

    A %= B + a

    B %= S + b

    C %= b

    new_grammar = remove_unreachable_prods(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["A", "b"], ["C"]]
    _graph["A"] = [["B", "a"]]
    _graph["B"] = [["S", "b"]]
    _graph["C"] = [["b"]]
    assert new_grammar == _graph

    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= A + B
    S %= b
    S %= a

    A %= B + a

    B %= S + b

    C %= b
    C %= a

    new_grammar = remove_unreachable_prods(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["A", "B"], ["b"], ["a"]]
    _graph["A"] = [["B", "a"]]
    _graph["B"] = [["S", "b"]]

    assert new_grammar == _graph

    # _graph = {}
    # _graph["S"] = [["a"], ["b"], ["C", "b"]]
    # _graph["A"] = [["a"], ["C", "b"]]
    # _graph["B"] = [["a"], ["C", "b"]]
    # _graph["C"] = [["a"]]

    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= a
    S %= b
    S %= C + b

    A %= a
    A %= C + b

    B %= a
    B %= C + b

    C %= a

    new_grammar = remove_unreachable_prods(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["a"], ["b"], ["C", "b"]]
    _graph["C"] = [["a"]]

    print(_graph)
    print(new_grammar)
    assert new_grammar == _graph


def test_remove_unit_prods():
    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= A
    S %= b

    A %= B
    A %= a

    B %= a
    B %= C + b

    C %= a

    new_grammar = remove_unnecesary_productions(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["a"], ["b"], ["C", "b"]]
    _graph["C"] = [["a"]]

    assert new_grammar == _graph

    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= A + B
    S %= C

    A %= A + b
    A %= a

    B %= b

    C %= a
    C %= b

    new_grammar = remove_unnecesary_productions(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    # _graph = {}
    # _graph["S"] = [["b"], ["a"], ["A", "B"]]
    # _graph["A"] = [["A", "b"], ["a"]]
    # _graph["B"] = [["b"]]

    # print(_graph)
    # print(new_grammar)
    # assert (new_grammar == _graph)

    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    A, B, C = grammar.add_nonterminals("A B C")
    a, b = grammar.add_terminals("a b")

    S %= A
    S %= b

    A %= B
    A %= a

    B %= a
    B %= C + b

    C %= a

    new_grammar = remove_unnecesary_productions(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["a"], ["b"], ["C", "b"]]
    _graph["C"] = [["a"]]

    assert new_grammar == _graph

    grammar = Grammar()
    S = grammar.add_nonterminal("S", True)
    X, Y = grammar.add_nonterminals("X Y")
    a, b = grammar.add_terminals("a b")

    S %= X + a
    S %= Y

    X %= b
    Y %= a

    new_grammar = remove_unnecesary_productions(grammar)

    _, new_grammar = grammar_to_graph(new_grammar)

    _graph = {}
    _graph["S"] = [["X", "a"], ["b"]]
    _graph["X"] = [["b"]]


# s -> X a | Y
# X -> b
# Y -> a
