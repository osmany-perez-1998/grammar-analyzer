from pycmp.grammar import Grammar
from pycmp.automata import NFA, DFA


def check_regular_grammar(grammar: Grammar):
    for _, right in grammar.productions:
        if not right[0].is_terminal:
            return False
        if len(right) >= 2 and not right[1].is_nonterminal:
            return False
        if len(right) > 2:
            return False
    return True


def grammar_to_automaton(grammar: Grammar):
    nonterminals = (nt for nt in grammar.nonterminals if nt != grammar.start_symbol)
    state_map = {nt: i + 1 for i, nt in enumerate(nonterminals)}
    state_map[grammar.start_symbol] = 0

    states = final = len(grammar.nonterminals)
    transitions = {}

    for left, right in grammar.productions:
        origin = state_map[left]
        symbol = right[0].name
        dest = state_map[right[1]] if len(right) == 2 else final
        transitions[origin, symbol] = dest

    return DFA(states, {final}, transitions)


def automaton_to_regex(automaton: NFA) -> str:
    states, transitions = to_gnfa(automaton)
    return gnfa_to_regex(list(range(states)), transitions)


def gnfa_to_regex(states: list, transitions: dict) -> str:
    if len(states) == 2:
        return transitions[states[0], states[-1]]

    # remove state
    qrip = states.pop(1)
    for qi in states[:-1]:
        for qj in states[1:]:
            r1, r2, r3, r4 = (
                transitions[qi, qrip],
                transitions[qrip, qrip],
                transitions[qrip, qj],
                transitions[qi, qj],
            )
            transitions[qi, qj] = f"(({r1})({r2})*({r3}))|({r4})"

    return gnfa_to_regex(states, transitions)


def to_gnfa(automaton: NFA) -> tuple:
    start, old_start = 0, 1
    final = automaton.states + old_start
    states = automaton.states + 2

    transitions = {}
    for origin in range(automaton.states):
        for dest in range(automaton.states):
            trans_syms = []
            for symbol in automaton.vocabulary:
                dests = automaton.transitions[origin].get(symbol)
                if dests is not None and dest in dests:
                    trans_syms.append(symbol)
            trans_regex = "<nosymbol>" if not trans_syms else "|".join(trans_syms)
            transitions[old_start + origin, old_start + dest] = trans_regex

    ## Add transitions from start state ...
    transitions[start, old_start] = ""
    for state in automaton.states:
        transitions[start, state] = "<nosymbol>"

    ## Add transitions to final state ...
    for state in automaton.states:
        symbol = "" if state in automaton.finals else "<nosymbol>"
        transitions[old_start + state, final] = symbol

    return states, transitions
