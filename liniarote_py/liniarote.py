# -*- coding: utf-8 -*-

# ╔════════════════════════════════════════════════════════════════════╗
# ║   LINIAROTE: The programming language for performing operations    ║
# ║   in transvalent mathematics                                       ║
# ║                                                                    ║
# ║   Developed by Matthew E. Gladden                                  ║
# ║   Software and documentation ©2022-2023 Cognitive Firewall LLC     ║
# ║                                                                    ║
# ║   This software is made available for use under                    ║
# ║   GNU General Public License Version 3                             ║
# ║   (please see https://www.gnu.org/licenses/gpl-3.0.html).          ║
# ╚════════════════════════════════════════════════════════════════════╝

"""
This module handles all of the programming language's input/output
mechanisms and internal logic.
"""

# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ PRELIMINARY STEPS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import standard modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import time
import math
import signal


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import readchar
from sly import Lexer, Parser


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import other modules from the WorkforceSim package
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

# Imports of the form "from . import X as x" have been added for use
# in the distributed package; imports of the form "import X as x" are
# retained for use when debugging the modules in VS Code.

if __name__ == "__main__":
    import config as cfg
else:
    try:
        from . import config as cfg
    except:
        import config as cfg


# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████
# ███
# ███ DEFINE CLASSES AND FUNCTIONS
# ███
# ██████████████████████████████████████████████████████████████████████
# ██████████████████████████████████████████████████████████████████████

# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Lexer and Parser
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

class LiniaroteLexer(Lexer):
    """
    Liniarote's core lexer, for recognizing inputted characters as tokens.
    """

    # Tokens to be recognized.
    tokens = {
        PLUS,
        MINUS,
        TIMES,
        #DIVIDE,
        LPAREN,
        RPAREN,
        NUM,
        ID,
        TRANSVALENT_SYMBOL_INPUT,
        HELP,
        }

    # Input to be ignored.
    ignore = ' \t\r\n'

    # Character strings to be recognized as tokens.
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    #DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    NUM = r"-?[0-9]+(\.[0-9]*)?"
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    ID['w'] = TRANSVALENT_SYMBOL_INPUT
    ID['W'] = TRANSVALENT_SYMBOL_INPUT
    ID['help'] = HELP
    ID['?'] = HELP


class LiniaroteParser(Parser):
    """
    Liniarote's core parser, for performing operations on tokenized input.
    """

    # Uncomment the line below to generate a debug file (e.g., for 
    # debugging shift/reduce or reduce/reduce conflicts).
    #debugfile = "parser.out"

    # ------------------------------------------------------------------
    # Specify tokens and the order of operations.
    # ------------------------------------------------------------------

    tokens = LiniaroteLexer.tokens

    # Specify the order in which operations should be processed.
    precedence = (
        ('left', PLUS, MINUS),
        #('left', TIMES, DIVIDE),
        ('left', TIMES),
        ('right', UMINUS),
        )


    # ------------------------------------------------------------------
    # Define internal functions.
    # ------------------------------------------------------------------

    def __init__(self):
        """
        Constructor for the class object.
        """
        self.vars = {
            "pi": math.pi,
            "e": math.e,
            }


    @_('HELP')
    def expr(self, p):
        """
        Displays help text when the HELP token is recognized.
        """
        return print_help_text()


    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        """
        Gives precedence to the processing of a unary minus sign
        (over the subtraction operation).
        """

        if p.expr == cfg.transval_sym_pos:
            return cfg.transval_sym_neg
        if p.expr == cfg.transval_sym_neg:
            return cfg.transval_sym_pos
        return -p.expr


    @_('expr MINUS expr')
    def expr(self, p):
        """
        Specifies how the subtraction operation is evaluated
        within the context of transvalent mathematics.
        """

        # ------------------------------------------------------------------
        # Process subtraction between lone elements (e.g., a transvalent 
        # symbol *or* float with another such variable), generating a
        # well-formed transvalent tuple as output.
        # ------------------------------------------------------------------

        # Process "float - float".
        if isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return (p.expr0 - p.expr0, 0.0)

        # Process "float - positive transvalent".
        elif isinstance(p.expr0, float) and (p.expr1 == cfg.transval_sym_pos):
            return (p.expr0, cfg.transval_sym_neg)

        # Process "float - negative transvalent".
        elif isinstance(p.expr0, float) and (p.expr1 == cfg.transval_sym_neg):
            return (p.expr0, cfg.transval_sym_pos)

        # Process "positive transvalent - float".
        elif (p.expr0 == cfg.transval_sym_pos) and isinstance(p.expr1, float):
            return (-p.expr1, cfg.transval_sym_pos)

        # Process "negative transvalent - float".
        elif (p.expr0 == cfg.transval_sym_neg) and isinstance(p.expr1, float):
            return (-p.expr1, cfg.transval_sym_neg)

        # Process "positive transvalent - positive transvalent".
        elif (p.expr0 == cfg.transval_sym_pos) and (p.expr1 == cfg.transval_sym_pos):
            return (0.0, 0.0)

        # Process "positive transvalent - negative transvalent".
        elif (p.expr0 == cfg.transval_sym_pos) and (p.expr1 == cfg.transval_sym_neg):
            return (0.0, cfg.transval_sym_pos)

        # Process "negative transvalent - positive transvalent".
        elif (p.expr0 == cfg.transval_sym_neg) and (p.expr1 == cfg.transval_sym_pos):
            return (0.0, cfg.transval_sym_neg)

        # Process "negative transvalent - negative transvalent".
        elif (p.expr0 == cfg.transval_sym_neg) and (p.expr1 == cfg.transval_sym_neg):
            return (0.0, 0.0)


        # ------------------------------------------------------------------
        # Process subtraction between a lone element and a tuple, generating
        # a well-formed transvalent tuple as output.
        # ------------------------------------------------------------------

        # Process "float - tuple".
        elif isinstance(p.expr0, float) and isinstance(p.expr1, tuple):
            if p.expr1[1] == cfg.transval_sym_pos:
                transvalent_elements_diff = cfg.transval_sym_neg
            elif p.expr1[1] == cfg.transval_sym_neg:
                transvalent_elements_diff = cfg.transval_sym_pos
            elif p.expr1[1] == 0:
                transvalent_elements_diff = 0.0
            return (p.expr0 - p.expr1[0], transvalent_elements_diff)

        # Process "tuple - float".
        elif isinstance(p.expr0, tuple) and isinstance(p.expr1, float):
            if p.expr0[1] == cfg.transval_sym_pos:
                transvalent_elements_diff = cfg.transval_sym_pos
            elif p.expr0[1] == cfg.transval_sym_neg:
                transvalent_elements_diff = cfg.transval_sym_neg
            elif p.expr0[1] == 0:
                transvalent_elements_diff = 0.0
            return (p.expr0[0] - p.expr1, transvalent_elements_diff)

        # Process "transvalent - tuple".
        elif (p.expr0 == cfg.transval_sym_pos) and isinstance(p.expr1, tuple):
            if p.expr1[1] == cfg.transval_sym_pos:
                transvalent_elements_diff = 0.0
            elif p.expr1[1] == cfg.transval_sym_neg:
                transvalent_elements_diff = cfg.transval_sym_pos
            elif p.expr1[1] == 0:
                transvalent_elements_diff = cfg.transval_sym_pos
            return (p.expr0[0] - p.expr1, transvalent_elements_diff)

        elif (p.expr0 == cfg.transval_sym_neg) and isinstance(p.expr1, tuple):
            if p.expr1[1] == cfg.transval_sym_pos:
                transvalent_elements_diff = cfg.transval_sym_neg
            elif p.expr1[1] == cfg.transval_sym_neg:
                transvalent_elements_diff = 0.0
            elif p.expr1[1] == 0:
                transvalent_elements_diff = cfg.transval_sym_neg
            return (p.expr0[0] - p.expr1, transvalent_elements_diff)

        # NOTE: this is unnecessary, as it is already handled by
        # the case of "float - tuple".
        #
        #elif (p.expr0 == 0) and isinstance(p.expr1, tuple):
        #    if p.expr1[1] == cfg.transval_sym_pos:
        #        transvalent_elements_diff = cfg.transval_sym_neg
        #    elif p.expr1[1] == cfg.transval_sym_neg:
        #        transvalent_elements_diff = cfg.transval_sym_pos
        #    elif p.expr1[1] == 0:
        #        transvalent_elements_diff = 0.0
        #    return (p.expr0[0] - p.expr1, transvalent_elements_diff)

        # Process "tuple - transvalent".
        elif isinstance(p.expr0, tuple) and (p.expr1 == cfg.transval_sym_pos):
            if p.expr0[1] == cfg.transval_sym_pos:
                transvalent_elements_diff = 0.0
            elif p.expr0[1] == cfg.transval_sym_neg:
                transvalent_elements_diff = cfg.transval_sym_neg
            elif p.expr0[1] == 0:
                transvalent_elements_diff = cfg.transval_sym_neg
            return (p.expr0[0], transvalent_elements_diff)

        elif isinstance(p.expr0, tuple) and (p.expr1 == cfg.transval_sym_neg):
            if p.expr0[1] == cfg.transval_sym_pos:
                transvalent_elements_diff = cfg.transval_sym_pos
            elif p.expr0[1] == cfg.transval_sym_neg:
                transvalent_elements_diff = 0.0
            elif p.expr0[1] == 0:
                transvalent_elements_diff = cfg.transval_sym_pos
            return (p.expr0[0], transvalent_elements_diff)

        # NOTE: this is unnecessary, as it is already handled by
        # the case of "tuple - float".
        #
        #elif isinstance(p.expr0, tuple) and (p.expr1 == 0):
        #    if p.expr0[1] == cfg.transval_sym_pos:
        #        transvalent_elements_diff = cfg.transval_sym_pos
        #    elif p.expr0[1] == cfg.transval_sym_neg:
        #        transvalent_elements_diff = cfg.transval_sym_neg
        #    elif p.expr0[1] == 0:
        #        transvalent_elements_diff = 0.0
        #    return (p.expr0[0], transvalent_elements_diff)


        # ------------------------------------------------------------------
        # Process subtraction between two tuples.
        # ------------------------------------------------------------------

        elif isinstance(p.expr0, tuple) and isinstance(p.expr1, tuple):

            # Determine what the difference of the transvalent elements will be.
            if (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == cfg.transval_sym_pos):
                transvalent_elements_diff = 0.0
            elif (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == cfg.transval_sym_neg):
                transvalent_elements_diff = cfg.transval_sym_pos
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == cfg.transval_sym_neg):
                transvalent_elements_diff = 0.0
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == cfg.transval_sym_pos):
                transvalent_elements_diff = cfg.transval_sym_neg

            elif (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == 0):
                transvalent_elements_diff = cfg.transval_sym_pos
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == 0):
                transvalent_elements_diff = cfg.transval_sym_neg
            elif (p.expr0[1] == 0) and (p.expr0[1] == 0):
                transvalent_elements_diff = 0
            elif (p.expr0[1] == 0) and (p.expr0[1] == cfg.transval_sym_pos):
                transvalent_elements_diff = cfg.transval_sym_neg
            elif (p.expr0[1] == 0) and (p.expr0[1] == cfg.transval_sym_neg):
                transvalent_elements_diff = cfg.transval_sym_pos

            return (p.expr0[0] - p.expr1[0], transvalent_elements_diff)


    @_('expr PLUS expr')
    def expr(self, p):
        """
        Specifies how the addition operation is evaluated
        within the context of transvalent mathematics.
        """

        # ------------------------------------------------------------------
        # Process addition of lone elements (e.g., a transvalent 
        # symbol *or* float with another such variable), generating a
        # well-formed transvalent tuple as output.
        # ------------------------------------------------------------------

        # Process "float + float".
        if isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return (p.expr0 + p.expr0, 0.0)

        # Process "float + positive transvalent".
        elif isinstance(p.expr0, float) and (p.expr1 == cfg.transval_sym_pos):
            return (p.expr0, cfg.transval_sym_pos)

        # Process "float + negative transvalent".
        elif isinstance(p.expr0, float) and (p.expr1 == cfg.transval_sym_neg):
            return (p.expr0, cfg.transval_sym_neg)

        # Process "positive transvalent + float".
        elif (p.expr0 == cfg.transval_sym_pos) and isinstance(p.expr1, float):
            return (p.expr1, cfg.transval_sym_pos)

        # Process "negative transvalent + float".
        elif (p.expr0 == cfg.transval_sym_neg) and isinstance(p.expr1, float):
            return (p.expr1, cfg.transval_sym_neg)

        # Process "positive transvalent + positive transvalent".
        elif (p.expr0 == cfg.transval_sym_pos) and (p.expr1 == cfg.transval_sym_pos):
            return (0.0, cfg.transval_sym_pos)

        # Process "positive transvalent + negative transvalent".
        elif (p.expr0 == cfg.transval_sym_pos) and (p.expr1 == cfg.transval_sym_neg):
            return (0.0, 0.0)

        # Process "negative transvalent + positive transvalent".
        elif (p.expr0 == cfg.transval_sym_neg) and (p.expr1 == cfg.transval_sym_pos):
            return (0.0, 0.0)

        # Process "negative transvalent + negative transvalent".
        elif (p.expr0 == cfg.transval_sym_neg) and (p.expr1 == cfg.transval_sym_neg):
            return (0.0, cfg.transval_sym_neg)


        # ------------------------------------------------------------------
        # Process addition of a lone element and a tuple, generating
        # a well-formed transvalent tuple as output.
        # ------------------------------------------------------------------

        # Process "float + tuple".
        elif isinstance(p.expr0, float) and isinstance(p.expr1, tuple):
            return (p.expr0 + p.expr1[0], p.expr1[1])

        # Process "tuple + float".
        elif isinstance(p.expr0, tuple) and isinstance(p.expr1, float):
            return (p.expr0[0] + p.expr1, p.expr0[1])

        # Process "transvalent + tuple".
        elif (p.expr0 == cfg.transval_sym_pos) and isinstance(p.expr1, tuple):
            if p.expr1[1] == cfg.transval_sym_pos:
                transvalent_elements_sum = cfg.transval_sym_pos
            if p.expr1[1] == cfg.transval_sym_neg:
                transvalent_elements_sum = 0.0
            if p.expr1[1] == 0:
                transvalent_elements_sum = cfg.transval_sym_pos
            return (p.expr1[0], transvalent_elements_sum)

        elif (p.expr0 == cfg.transval_sym_neg) and isinstance(p.expr1, tuple):
            if p.expr1[1] == cfg.transval_sym_pos:
                transvalent_elements_sum = 0.0
            if p.expr1[1] == cfg.transval_sym_neg:
                transvalent_elements_sum = cfg.transval_sym_neg
            if p.expr1[1] == 0:
                transvalent_elements_sum = cfg.transval_sym_neg
            return (p.expr1[0], transvalent_elements_sum)

        # NOTE: this is unnecessary, as it is already handled by
        # the case of "float + tuple".
        #
        #elif (p.expr0 == 0) and isinstance(p.expr1, tuple):
        #    if p.expr1[1] == cfg.transval_sym_pos:
        #        transvalent_elements_sum = cfg.transval_sym_pos
        #    if p.expr1[1] == cfg.transval_sym_neg:
        #        transvalent_elements_sum = cfg.transval_sym_neg
        #    if p.expr1[1] == 0:
        #        transvalent_elements_sum = 0.0
        #    return (p.expr1[0], transvalent_elements_sum)

        # Process "tuple + transvalent".
        elif isinstance(p.expr0, tuple) and (p.expr1 == cfg.transval_sym_pos):
            if p.expr0[1] == cfg.transval_sym_pos:
                transvalent_elements_sum = cfg.transval_sym_pos
            elif p.expr0[1] == cfg.transval_sym_neg:
                transvalent_elements_sum = 0.0
            elif p.expr0[1] == 0:
                transvalent_elements_sum = cfg.transval_sym_pos
            return (p.expr0[0], transvalent_elements_sum)

        elif isinstance(p.expr0, tuple) and (p.expr1 == cfg.transval_sym_neg):
            if p.expr0[1] == cfg.transval_sym_pos:
                transvalent_elements_sum = 0.0
            elif p.expr0[1] == cfg.transval_sym_neg:
                transvalent_elements_sum = cfg.transval_sym_neg
            elif p.expr0[1] == 0:
                transvalent_elements_sum = cfg.transval_sym_neg
            return (p.expr0[0], transvalent_elements_sum)

        # NOTE: this is unnecessary, as it is already handled by
        # the case of "tuple + float".
        #
        #elif isinstance(p.expr0, tuple) and (p.expr1 == 0):
        #    if p.expr0[1] == cfg.transval_sym_pos:
        #        transvalent_elements_sum = cfg.transval_sym_pos
        #    if p.expr0[1] == cfg.transval_sym_neg:
        #        transvalent_elements_sum = cfg.transval_sym_neg
        #    if p.expr0[1] == 0:
        #        transvalent_elements_sum = 0.0
        #    return (p.expr0[0], transvalent_elements_sum)


        # ------------------------------------------------------------------
        # Process addition of two tuples.
        # ------------------------------------------------------------------

        elif isinstance(p.expr0, tuple) and isinstance(p.expr1, tuple):

            # Determine what the sum of the transvalent elements will be.
            if (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == cfg.transval_sym_pos):
                transvalent_elements_sum = cfg.transval_sym_pos
            elif (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == cfg.transval_sym_neg):
                transvalent_elements_sum = 0.0
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == cfg.transval_sym_neg):
                transvalent_elements_sum = cfg.transval_sym_neg
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == cfg.transval_sym_pos):
                transvalent_elements_sum = 0.0

            elif (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == 0):
                transvalent_elements_sum = cfg.transval_sym_pos
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == 0):
                transvalent_elements_sum = cfg.transval_sym_neg
            elif (p.expr0[1] == 0) and (p.expr0[1] == 0):
                transvalent_elements_sum = 0
            elif (p.expr0[1] == 0) and (p.expr0[1] == cfg.transval_sym_pos):
                transvalent_elements_sum = cfg.transval_sym_pos
            elif (p.expr0[1] == 0) and (p.expr0[1] == cfg.transval_sym_neg):
                transvalent_elements_sum = cfg.transval_sym_neg

            return (p.expr0[0] + p.expr1[0], transvalent_elements_sum)


    @_('term')
    def expr(self, p):
        """
        Defines the processing of a single term.
        """
        return p.term


    @_('expr TIMES expr')
    def expr(self, p):
        """
        Specifies how the multiplication operation is evaluated
        within the context of transvalent mathematics.
        """

        # ------------------------------------------------------------------
        # Process multiplication of lone elements (e.g., a transvalent 
        # symbol *or* float with another such variable), generating a
        # well-formed transvalent tuple as output.
        # ------------------------------------------------------------------

        # Process "float × float".
        if isinstance(p.expr0, float) and isinstance(p.expr1, float):
            return (p.expr0 * p.expr1, 0.0)

        # Process "float × positive transvalent".
        elif isinstance(p.expr0, float) and (p.expr1 == cfg.transval_sym_pos):
            if (p.expr0 > 0):
                return (0.0, cfg.transval_sym_pos)
            elif (p.expr0 == 0):
                return (1.0, 0.0)
            elif (p.expr0 < 0):
                return (0.0, cfg.transval_sym_neg)

        # Process "float × negative transvalent".
        elif isinstance(p.expr0, float) and (p.expr1 == cfg.transval_sym_neg):
            if (p.expr0 > 0):
                return (0.0, cfg.transval_sym_neg)
            elif (p.expr0 == 0):
                return (-1.0, 0.0)
            elif (p.expr0 < 0):
                return (0.0, cfg.transval_sym_pos)

        # Process "positive transvalent × float".
        elif (p.expr0 == cfg.transval_sym_pos) and isinstance(p.expr1, float):
            if (p.expr1 > 0):
                return (0.0, cfg.transval_sym_pos)
            elif (p.expr1 == 0):
                return (1.0, 0.0)
            elif (p.expr1 < 0):
                return (0.0, cfg.transval_sym_neg)

        # Process "negative transvalent × float".
        elif (p.expr0 == cfg.transval_sym_neg) and isinstance(p.expr1, float):
            if (p.expr1 > 0):
                return (0.0, cfg.transval_sym_neg)
            elif (p.expr1 == 0):
                return (-1.0, 0.0)
            elif (p.expr1 < 0):
                return (0.0, cfg.transval_sym_pos)

        # Process "positive transvalent × positive transvalent".
        elif (p.expr0 == cfg.transval_sym_pos) and (p.expr1 == cfg.transval_sym_pos):
            return (0.0, cfg.transval_sym_pos)

        # Process "positive transvalent × negative transvalent".
        elif (p.expr0 == cfg.transval_sym_pos) and (p.expr1 == cfg.transval_sym_neg):
            return (0.0, cfg.transval_sym_neg)

        # Process "negative transvalent × positive transvalent".
        elif (p.expr0 == cfg.transval_sym_neg) and (p.expr1 == cfg.transval_sym_pos):
            return (0.0, cfg.transval_sym_neg)

        # Process "negative transvalent × negative transvalent".
        elif (p.expr0 == cfg.transval_sym_neg) and (p.expr1 == cfg.transval_sym_neg):
            return (0.0, cfg.transval_sym_pos)


        # ------------------------------------------------------------------
        # Process multiplication of a lone element and a tuple, generating
        # a well-formed transvalent tuple as output.
        # ------------------------------------------------------------------

        # Process "float × tuple".
        elif isinstance(p.expr0, float) and isinstance(p.expr1, tuple):
            return (p.expr0 * p.expr1[0], p.expr1[1])

        # Process "tuple × float".
        elif isinstance(p.expr0, tuple) and isinstance(p.expr1, float):
            return (p.expr0[0] * p.expr1, p.expr0[1])

        # Process "positive transvalent × tuple".
        elif (p.expr0 == cfg.transval_sym_pos) and isinstance(p.expr1, tuple):
            if p.expr1[1] == cfg.transval_sym_pos:
                if p.expr1[0] > 0:
                    return (0.0, cfg.transval_sym_pos)
                elif p.expr1[0] == 0:
                    return (1.0, cfg.transval_sym_pos)
                elif p.expr1[0] < 0:
                    return (0.0, 0.0)
            elif p.expr1[1] == cfg.transval_sym_neg:
                if p.expr1[0] > 0:
                    return (0.0, 0.0)
                elif p.expr1[0] == 0:
                    return (1.0, cfg.transval_sym_neg)
                elif p.expr1[0] < 0:
                    return (0.0, cfg.transval_sym_neg)
            elif p.expr1[1] == 0:
                if p.expr1[0] > 0:
                    return (0.0, cfg.transval_sym_pos)
                elif p.expr1[0] == 0:
                    return (1.0, 0.0)
                elif p.expr1[0] < 0:
                    return (0.0, cfg.transval_sym_neg)

        # Process "negative transvalent × tuple".
        elif (p.expr0 == cfg.transval_sym_neg) and isinstance(p.expr1, tuple):
            if p.expr1[1] == cfg.transval_sym_pos:
                if p.expr1[0] > 0:
                    return (0.0, cfg.transval_sym_neg)
                elif p.expr1[0] == 0:
                    return (-1.0, cfg.transval_sym_neg)
                elif p.expr1[0] < 0:
                    return (0.0, 0.0)
            elif p.expr1[1] == cfg.transval_sym_neg:
                if p.expr1[0] > 0:
                    return (0.0, 0.0)
                elif p.expr1[0] == 0:
                    return (-1.0, cfg.transval_sym_pos)
                elif p.expr1[0] < 0:
                    return (0.0, cfg.transval_sym_pos)
            elif p.expr1[1] == 0:
                if p.expr1[0] > 0:
                    return (0.0, cfg.transval_sym_neg)
                elif p.expr1[0] == 0:
                    return (-1.0, 0.0)
                elif p.expr1[0] < 0:
                    return (0.0, cfg.transval_sym_pos)

        # Process "tuple × positive transvalent".
        elif isinstance(p.expr0, tuple) and (p.expr1 == cfg.transval_sym_pos):
            if p.expr0[1] == cfg.transval_sym_pos:
                if p.expr0[0] > 0:
                    return (0.0, cfg.transval_sym_pos)
                elif p.expr0[0] == 0:
                    return (1.0, cfg.transval_sym_pos)
                elif p.expr0[0] < 0:
                    return (0.0, 0.0)
            elif p.expr0[1] == cfg.transval_sym_neg:
                if p.expr0[0] > 0:
                    return (0.0, 0.0)
                elif p.expr0[0] == 0:
                    return (1.0, cfg.transval_sym_neg)
                elif p.expr0[0] < 0:
                    return (0.0, cfg.transval_sym_neg)
            elif p.expr0[1] == 0:
                if p.expr0[0] > 0:
                    return (0.0, cfg.transval_sym_pos)
                elif p.expr0[0] == 0:
                    return (1.0, 0.0)
                elif p.expr0[0] < 0:
                    return (0.0, cfg.transval_sym_neg)

        # Process "tuple × negative transvalent".
        elif isinstance(p.expr0, tuple) and (p.expr1 == cfg.transval_sym_neg):
            if p.expr0[1] == cfg.transval_sym_pos:
                if p.expr0[0] > 0:
                    return (0.0, cfg.transval_sym_neg)
                elif p.expr0[0] == 0:
                    return (-1.0, cfg.transval_sym_neg)
                elif p.expr0[0] < 0:
                    return (0.0, 0.0)
            elif p.expr0[1] == cfg.transval_sym_neg:
                if p.expr0[0] > 0:
                    return (0.0, 0.0)
                elif p.expr0[0] == 0:
                    return (-1.0, cfg.transval_sym_pos)
                elif p.expr0[0] < 0:
                    return (0.0, cfg.transval_sym_pos)
            elif p.expr0[1] == 0:
                if p.expr0[0] > 0:
                    return (0.0, cfg.transval_sym_neg)
                elif p.expr0[0] == 0:
                    return (-1.0, 0.0)
                elif p.expr0[0] < 0:
                    return (0.0, cfg.transval_sym_pos)

        # ------------------------------------------------------------------
        # Process multiplication of two tuples.
        # ------------------------------------------------------------------

        elif isinstance(p.expr0, tuple) and isinstance(p.expr1, tuple):

            # Where expr0[1] == Ƿ and expr1[1] == Ƿ.
            if (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == cfg.transval_sym_pos):
                if (p.expr0[0] > 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (
                        (p.expr0[0] > 0) and (p.expr1[0] == 0) \
                        or (p.expr0[0] == 0) and (p.expr1[0] > 0)
                        ):
                    return (1.0, cfg.transval_sym_pos)
                elif (
                        (p.expr0[0] > 0) and (p.expr1[0] < 0) \
                        or (p.expr0[0] < 0) and (p.expr1[0] > 0)
                        ):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] == 0) and (p.expr1[0] == 0):
                    return (2.0, cfg.transval_sym_pos)
                elif (
                        (p.expr0[0] == 0) and (p.expr1[0] < 0) \
                        or (p.expr0[0] < 0) and (p.expr1[0] == 0) 
                        ):
                    return (1.0, 0.0)
                elif (p.expr0[0] < 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)

            # Where expr0[1] == Ƿ and expr1[1] == -Ƿ.
            elif (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == cfg.transval_sym_neg):
                if (p.expr0[0] > 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] > 0) and (p.expr1[0] == 0):
                    return (1.0, cfg.transval_sym_neg)
                elif (p.expr0[0] == 0) and (p.expr1[0] > 0):
                    return (-1.0, 0.0)
                elif (p.expr0[0] > 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] < 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] == 0) and (p.expr1[0] == 0):
                    return (0.0, cfg.transval_sym_neg)
                elif (p.expr0[0] == 0) and (p.expr1[0] < 0):
                    return (-1.0, cfg.transval_sym_neg)
                elif (p.expr0[0] < 0) and (p.expr1[0] == 0):
                    return (1.0, 0.0)
                elif (p.expr0[0] < 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)

            # Where expr0[1] == -Ƿ and expr1[1] == Ƿ.
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == cfg.transval_sym_pos):
                if (p.expr0[0] > 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] > 0) and (p.expr1[0] == 0):
                    return (-1.0, cfg.transval_sym_neg)
                elif (p.expr0[0] == 0) and (p.expr1[0] > 0):
                    return (1.0, cfg.transval_sym_neg)
                elif (p.expr0[0] > 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] < 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] == 0) and (p.expr1[0] == 0):
                    return (0.0, cfg.transval_sym_neg)
                elif (p.expr0[0] == 0) and (p.expr1[0] < 0):
                    return (1.0, 0.0)
                elif (p.expr0[0] < 0) and (p.expr1[0] == 0):
                    return (-1.0, cfg.transval_sym_neg)
                elif (p.expr0[0] < 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)

            # Where expr0[1] == -Ƿ and expr1[1] == -Ƿ.
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == cfg.transval_sym_neg):
                if (p.expr0[0] > 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (
                        (p.expr0[0] > 0) and (p.expr1[0] == 0) \
                        or (p.expr0[0] == 0) and (p.expr1[0] > 0)
                        ):
                    return (-1.0, 0.0)
                elif (
                        (p.expr0[0] > 0) and (p.expr1[0] < 0) \
                        or (p.expr0[0] < 0) and (p.expr1[0] > 0)
                        ):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] == 0) and (p.expr1[0] == 0):
                    return (-2.0, cfg.transval_sym_pos)
                elif (
                        (p.expr0[0] == 0) and (p.expr1[0] < 0) \
                        or (p.expr0[0] < 0) and (p.expr1[0] == 0) 
                        ):
                    return (-1.0, 0.0)
                elif (p.expr0[0] < 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)

            # Where expr0[1] == Ƿ and expr1[1] == 0.
            elif (p.expr0[1] == cfg.transval_sym_pos) and (p.expr0[1] == 0):
                if (p.expr0[0] > 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] > 0) and (p.expr1[0] == 0):
                    return (1.0, 0.0)
                elif (p.expr0[0] == 0) and (p.expr1[0] > 0):
                    return (0.0, cfg.transval_sym_pos)
                elif (p.expr0[0] > 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] < 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] == 0) and (p.expr1[0] == 0):
                    return (1.0, 0.0)
                elif (p.expr0[0] == 0) and (p.expr1[0] < 0):
                    return (0.0, cfg.transval_sym_neg)
                elif (p.expr0[0] < 0) and (p.expr1[0] == 0):
                    return (1.0, 0.0)
                elif (p.expr0[0] < 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)

            # Where expr0[1] == 0 and expr1[1] == Ƿ.
            elif (p.expr0[1] == 0) and (p.expr0[1] == cfg.transval_sym_pos):
                if (p.expr0[0] > 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] > 0) and (p.expr1[0] == 0):
                    return (0.0, cfg.transval_sym_pos)
                elif (p.expr0[0] == 0) and (p.expr1[0] > 0):
                    return (1.0, 0.0)
                elif (p.expr0[0] > 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] < 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] == 0) and (p.expr1[0] == 0):
                    return (1.0, 0.0)
                elif (p.expr0[0] == 0) and (p.expr1[0] < 0):
                    return (1.0, 0.0)
                elif (p.expr0[0] < 0) and (p.expr1[0] == 0):
                    return (0.0, cfg.transval_sym_neg)
                elif (p.expr0[0] < 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)

            # Where expr0[1] == 0 and expr1[1] == -Ƿ.
            elif (p.expr0[1] == 0) and (p.expr0[1] == cfg.transval_sym_neg):
                if (p.expr0[0] > 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] > 0) and (p.expr1[0] == 0):
                    return (0.0, cfg.transval_sym_neg)
                elif (p.expr0[0] == 0) and (p.expr1[0] > 0):
                    return (-1.0, 0.0)
                elif (p.expr0[0] > 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] < 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] == 0) and (p.expr1[0] == 0):
                    return (-1.0, 0.0)
                elif (p.expr0[0] == 0) and (p.expr1[0] < 0):
                    return (-1.0, 0.0)
                elif (p.expr0[0] < 0) and (p.expr1[0] == 0):
                    return (0.0, cfg.transval_sym_pos)
                elif (p.expr0[0] < 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)

            # Where expr0[1] == -Ƿ and expr1[1] == 0.
            elif (p.expr0[1] == cfg.transval_sym_neg) and (p.expr0[1] == 0):
                if (p.expr0[0] > 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] > 0) and (p.expr1[0] == 0):
                    return (-1.0, 0.0)
                elif (p.expr0[0] == 0) and (p.expr1[0] > 0):
                    return (0.0, cfg.transval_sym_neg)
                elif (p.expr0[0] > 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)
                elif (p.expr0[0] < 0) and (p.expr1[0] > 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_neg)
                elif (p.expr0[0] == 0) and (p.expr1[0] == 0):
                    return (-1.0, 0.0)
                elif (p.expr0[0] == 0) and (p.expr1[0] < 0):
                    return (0.0, cfg.transval_sym_pos)
                elif (p.expr0[0] < 0) and (p.expr1[0] == 0):
                    return (-1.0, 0.0)
                elif (p.expr0[0] < 0) and (p.expr1[0] < 0):
                    return (p.expr0[0] * p.expr1[0], cfg.transval_sym_pos)

            # Where expr0[1] == 0 and expr1[1] == 0.
            elif (p.expr0[1] == 0) and (p.expr0[1] == 0):
                return (p.expr0[0] * p.expr1[0], 0.0)


    """
    @_('term DIVIDE factor')
    def expr(self, p):
        return p.term / p.factor
    """


    @_('factor')
    def term(self, p):
        """
        Defines the processing of a single factor.
        """
        return p.factor


    @_('LPAREN expr RPAREN')
    def factor(self, p):
        """
        Defines the processing of an expression enclosed in parentheses.
        """
        return p.expr


    @_('NUM')
    def factor(self, p):
        """
        Defines the processing of a recognized numerical token.
        """
        return float(p.NUM)


    @_('TRANSVALENT_SYMBOL_INPUT')
    def factor(self, p):
        """
        Defines the processing of a recognized transvalent symbol.
        """
        return cfg.transval_sym_pos


    @_('ID')
    def factor(self, p):
        """
        Checks whether inputted text is an established variable.
        """
        return self.getVar(p.ID)

    def getVar(self, name):
        """
        Assigns the value to a new variable from via user input.
        """
        if name not in self.vars:
            self.vars[name] = float(input(f"Please enter the desired value for {name}: "))
        return self.vars[name]


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Formatter (to convert transvalent tuples or text for display)
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def format_result_for_display(
    result_unformatted
    ):
    """
    Formats calculated transvalent tuples of the type "(1.0, Ƿ)" as
    output in the form of "1.0 + Ƿ", for display. Passes conventional
    text strings (e.g., intro or help text) without alteration.
    """

    # For debugging purposes.
    #print("result_unformatted: ", result_unformatted)
    #print("result_unformatted type: ", type(result_unformatted))


    # If the result is a lone real number...
    if isinstance(result_unformatted, float):
        result_formatted = str(result_unformatted) + " + (" + cfg.transval_sym_pos + " - " + cfg.transval_sym_pos + ")"

    # If the result is Ƿ or -Ƿ by itself...
    elif isinstance(result_unformatted, str):
        if result_unformatted == cfg.transval_sym_pos:
            result_formatted = str(0.0) + " + " + cfg.transval_sym_pos
        elif result_unformatted == cfg.transval_sym_neg:
            result_formatted = str(0.0) + " - " + cfg.transval_sym_pos
        else:
            result_formatted = result_unformatted

    # If the result is a well-formed tuple...
    elif isinstance(result_unformatted, tuple):

        # If the transvalent element == Ƿ.
        if result_unformatted[1] == cfg.transval_sym_pos:
            result_formatted = str(float(result_unformatted[0])) + " + " + cfg.transval_sym_pos

        # If the transvalent element == -Ƿ.
        elif result_unformatted[1] == cfg.transval_sym_neg:
            result_formatted = str(float(result_unformatted[0])) + " - " + cfg.transval_sym_pos

        # If the transvalent element == 0.
        elif result_unformatted[1] == 0:
            result_formatted = str(float(result_unformatted[0])) + " + (" + cfg.transval_sym_pos + " - " + cfg.transval_sym_pos + ")"

        # If result_formatted is a string rather than a tuple 
        # (e.g., in the case of the intro text or help text):
        elif isinstance(result_unformatted, str):
            result_formatted = result_unformatted

    return result_formatted


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Display of pre-prepared text blocks
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def print_intro_text():
    """
    Displays the standard text block used when launching the package.
    """
    print(cfg.intro_text)


def print_help_text():
    """
    Displays a help file when requested by the user.
    """

    print(cfg.help_text)
    return "('Help' contents displayed above. Returning to command prompt.)"


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Overall logic for executing the module
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def handler(signum, frame):
    """
    Allows the user the option of cleanly exiting the program when 
    input of "Ctrl+C" has been detected.
    """

    # Ask for confirmation that the user wishes to exit the program.
    pre_exit_message = "Quit Liniarote? Please press 'y' to exit this program."
    print(pre_exit_message, end="", flush=True)
    user_response = readchar.readchar()

    # Exit if either "Y" or "y" is inputted as the user's response.
    if user_response.lower() == "y":
        print("\n              Thank you for using Liniarote!\n")
        exit(1)
    else:
        print("", end="\r", flush=True)


if __name__ == '__main__':

    # Display the intro text.
    print_intro_text()

    # Create the lexer.
    lexer = LiniaroteLexer()

    # Check for user input of "Ctrl+C".
    signal.signal(signal.SIGINT, handler)

    while True:

        # Display the command prompt that accepts user input.
        text = input("<LINIAROTE:>  ")

        try:
            # For debugging purposes.
            #tokens_for_display = lexer.tokenize(text)
            #for token in tokens_for_display:
            #    print('token type: ', token.type, "; token value: ", token.value)

            # Process the user's input.
            tokens = lexer.tokenize(text)
            parser = LiniaroteParser()
            result = parser.parse(tokens)

        except:
            result = ("A problem occurred during processing. Please try reformulating your input.")

        # Format the calculated output for display and display it
        # on a special "output" line.
        result = format_result_for_display(result)
        print("    output =  " + result)

        # After calculated output has been displayed, wait
        # before providing a new (blank) command prompt to
        # receive new input from the user.
        time.sleep(0.4)

# ••••-••••-••••-••••-••••-••••-••••--••••-••••-••••-••••-••••-••••-••••