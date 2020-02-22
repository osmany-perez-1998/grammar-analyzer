import streamlit as st
from grammar_analyzer.interpreter import eval_input
from pycmp.exceptions import ParsingError

# pylint: disable=no-value-for-parameter


def ll_analysis():
    pass


def slr_analysis():
    pass


def lr_analysis():
    pass


def regular_analysis():
    pass


def enhacement_analysis():
    pass


def input_grammar():
    input_text = st.text_area(
        label="Please input your grammar here",
        value="balanced -> ( balanced ) | balanced ( ) | ( ) balanced | eps",
    )
    grammar = eval_input(input_text)
    return grammar


def run():
    st.title("Grammar Analyzer")

    grammar = input_grammar()

    if grammar is None:
        return

    option = st.selectbox(
        label="Select type of analysis to be made",
        options=("LL", "SLR", "LR", "Regular", "Enhancement"),
    )

    if option == "LL":
        ll_analysis()

    if option == "SLR":
        slr_analysis()

    if option == "LR":
        lr_analysis()

    if option == "Regular":
        regular_analysis()

    if option == "Enhancement":
        enhacement_analysis()


if __name__ == "__main__":
    run()
