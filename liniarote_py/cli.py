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


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import standard modules.
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import time
import math
import signal


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import third-party modules.
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

import readchar
from sly import Lexer, Parser


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Import other modules from the Liniarote package.
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

try:
    from . import config as cfg
except:
    import config as cfg


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define the lexer and parser.
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

class LiniaroteLexer(Lexer):
    """
    Liniarote's core lexer, for recognizing inputted characters as tokens.
    """

    # The following are the tokens to be recognized by the lexer.
    tokens = {
        PLUS,
        MINUS,
        TIMES,
        DIVIDE,
        LPAREN,
        RPAREN,
        NUM,
        ID,
        TRANSVALENT_SYMBOL_POSITIVE_INPUT,
        TRANSVALENT_SYMBOL_POWER_PLUS_TWO_POSITIVE_INPUT,
        TRANSVALENT_SYMBOL_POWER_PLUS_THREE_POSITIVE_INPUT,
        TRANSVALENT_SYMBOL_POWER_PLUS_FOUR_POSITIVE_INPUT,
        TRANSVALENT_SYMBOL_POWER_MINUS_TWO_POSITIVE_INPUT,
        TRANSVALENT_SYMBOL_POWER_MINUS_THREE_POSITIVE_INPUT,
        REAL_NUMBER_POSITIVE_SYMBOL_INPUT,
        REAL_NUMBER_SYMBOL_INPUT,
        NULL_SYMBOL_INPUT,
        UNIMPLEMENTED_SYMBOL_INPUT,
        HELP,
        PI_CONSTANT,
        E_CONSTANT,
        }

    # The following types of input will be ignored by the lexer.
    ignore = ' \t\r\n'

    # These character strings will be recognized as tokens.
    PLUS = r'\+'
    MINUS = r'-'
    TIMES = r'\*'
    DIVIDE = r'/'
    LPAREN = r'\('
    RPAREN = r'\)'
    NUM = r"-?[0-9]+(\.[0-9]*)?"
    ID = r"[a-zA-Z_Ƿ⁻²³⁴Æℝ∅][a-zA-Z0-9_Ƿ⁻²³⁴Æℝ∅]*"
    ID['w'] = TRANSVALENT_SYMBOL_POSITIVE_INPUT
    ID['W'] = TRANSVALENT_SYMBOL_POSITIVE_INPUT
    ID[cfg.tv_sym_pos] = TRANSVALENT_SYMBOL_POSITIVE_INPUT
    ID[cfg.tv_sym_pwr_p2_pos] = TRANSVALENT_SYMBOL_POWER_PLUS_TWO_POSITIVE_INPUT
    ID[cfg.tv_sym_pwr_p3_pos] = TRANSVALENT_SYMBOL_POWER_PLUS_THREE_POSITIVE_INPUT
    ID[cfg.tv_sym_pwr_p4_pos] = TRANSVALENT_SYMBOL_POWER_PLUS_FOUR_POSITIVE_INPUT
    ID[cfg.tv_sym_pwr_m2_pos] = TRANSVALENT_SYMBOL_POWER_MINUS_TWO_POSITIVE_INPUT
    ID[cfg.tv_sym_pwr_m3_pos] = TRANSVALENT_SYMBOL_POWER_MINUS_THREE_POSITIVE_INPUT
    ID[cfg.real_num_sym_pos] = REAL_NUMBER_POSITIVE_SYMBOL_INPUT
    ID[cfg.real_num_sym] = REAL_NUMBER_SYMBOL_INPUT
    ID[cfg.null_sym] = NULL_SYMBOL_INPUT
    ID[cfg.unimplemented_sym] = UNIMPLEMENTED_SYMBOL_INPUT
    ID['help'] = HELP
    ID['?'] = HELP
    ID['pi'] = PI_CONSTANT
    ID['e'] = E_CONSTANT


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
        ('left', TIMES, DIVIDE),
        ('right', UMINUS),
        )


    # ------------------------------------------------------------------
    # Define internal methods and functions.
    # ------------------------------------------------------------------
    def __init__(self):
        """
        The constructor method for the class object.
        """


    @_('HELP')
    def expr(self, p):
        """
        Displays help text when the HELP token is recognized.
        """
        return print_help_text()


    @_('PI_CONSTANT')
    def expr(self, p):
        """
        Returns the value of pi when the PI_CONSTANT token is recognized.
        """
        return math.pi


    @_('E_CONSTANT')
    def expr(self, p):
        """
        Returns the value of e when the E_CONSTANT token is recognized.
        """
        return math.e


    def error(self, p):
        """
        Displays an error message if poorly formulated input is detected
        (e.g., "3++w" or "5//w").
        """
        print(cfg.output_spacer \
            + "A poorly formulated input statement has been detected.")
        print(cfg.output_spacer \
            + "A (possibly misguided) attempt will be made to interpret it.")


    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        """
        Gives precedence to the processing of a unary minus sign
        (over the subtraction operation) and returns the correct
        value after the unary minus operation has been applied.
        """

        if p.expr == cfg.tv_sym_pos:
            return cfg.tv_sym_neg
        elif p.expr == cfg.tv_sym_neg:
            return cfg.tv_sym_pos

        elif p.expr == cfg.tv_sym_pwr_p2_pos:
            return cfg.tv_sym_pwr_p2_neg
        elif p.expr == cfg.tv_sym_pwr_p2_neg:
            return cfg.tv_sym_pwr_p2_pos

        elif p.expr == cfg.tv_sym_pwr_p3_pos:
            return cfg.tv_sym_pwr_p3_neg
        elif p.expr == cfg.tv_sym_pwr_p3_neg:
            return cfg.tv_sym_pwr_p3_pos

        elif p.expr == cfg.tv_sym_pwr_p4_pos:
            return cfg.tv_sym_pwr_p4_neg
        elif p.expr == cfg.tv_sym_pwr_p4_neg:
            return cfg.tv_sym_pwr_p4_pos

        elif p.expr == cfg.tv_sym_pwr_m2_pos:
            return cfg.tv_sym_pwr_m2_neg
        elif p.expr == cfg.tv_sym_pwr_m2_neg:
            return cfg.tv_sym_pwr_m2_pos

        elif p.expr == cfg.tv_sym_pwr_m3_pos:
            return cfg.tv_sym_pwr_m3_neg
        elif p.expr == cfg.tv_sym_pwr_m3_neg:
            return cfg.tv_sym_pwr_m3_pos

        elif p.expr == cfg.real_num_sym_pos:
            return cfg.real_num_sym_neg
        elif p.expr == cfg.real_num_sym_neg:
            return cfg.real_num_sym_pos

        elif p.expr == cfg.real_num_sym:
            return cfg.real_num_sym

        elif p.expr == cfg.null_sym:
            return cfg.null_sym

        elif p.expr == cfg.unimplemented_sym:
            return cfg.unimplemented_sym

        # If nothing above applies...
        return -p.expr


    @_('expr MINUS expr')
    def expr(self, p):
        """
        Specifies how the subtraction operation is evaluated
        within the context of transvalent mathematics.
        """

        if cfg.debugging_mode is True:
            print("Beginning subtraction of: ", str(p.expr0), "and", str(p.expr1))
            print("   ... of types: ", str(type(p.expr0)), "and", str(type(p.expr1)))

        # Assign the argument expressions to variables, to simplify
        # operations involving them.
        u = p.expr0
        v = p.expr1

        # If both u *and* v are lone elements, then they can be processed
        # directly as specified further below. Similarly, if both u *and* v 
        # are already well-formed tuples, they can be processed as specified
        # further below. However, if one of u or v is a lone element and the
        # other is a tuple, the lone element should be converted to a tuple
        # here, so that they can be processed below as two tuples.
        #
        # Note that technically, this only checks whether they are tuples;
        # to be more rigorous and eliminate errors, it should check whether
        # they are *well-formed* transvalent tuples.
        if isinstance(u, tuple) and (not isinstance(v, tuple)):
            v = convert_lone_element_to_tuple(v)
        elif (not isinstance(u, tuple)) and isinstance(v, tuple):
            u = convert_lone_element_to_tuple(u)

        if cfg.debugging_mode is True:
            print("Continuing with subtraction of: ", str(u), "and", str(v))


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
        # ● Process the subtraction of lone elements (e.g., a transvalent 
        # ● symbol *or* float with another such variable), generating a
        # ● well-formed transvalent tuple as output.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

        # If either of the terms is the Unimplemented symbol, return
        # a result indicating that the operation cannot be processed.
        if (u == cfg.unimplemented_sym) | (v == cfg.unimplemented_sym):
            return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "float - (something)".
        # ------------------------------------------------------------------

        # Process "float - float".
        if isinstance(u, float) and isinstance(v, float):
            return (u - v, cfg.null_sym)

        # Process "float - Ƿ".
        elif isinstance(u, float) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_neg)

        # Process "float - -Ƿ".
        elif isinstance(u, float) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pos)

        # Process "float - Ƿ²".
        elif isinstance(u, float) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "float - -Ƿ²".
        elif isinstance(u, float) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "float - ∅".
        elif isinstance(u, float)  and (v == cfg.null_sym):
            return (u, cfg.null_sym)

        # Process "float - Æ".
        elif isinstance(u, float) and (v == cfg.real_num_sym_pos):
            if u == 0:
                return (cfg.real_num_sym_neg, cfg.null_sym)
            else:
                return cfg.unimplemented_sym

        # Process "float - -Æ".
        elif isinstance(u, float) and (v == cfg.real_num_sym_neg):
            if u == 0:
                return (cfg.real_num_sym_pos, cfg.null_sym)
            else:
                return cfg.unimplemented_sym

        # Process "float - ℝ".
        elif isinstance(u, float) and (v == cfg.real_num_sym):
            return (cfg.real_num_sym, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "Ƿ - (something)".
        # ------------------------------------------------------------------

        # Process "Ƿ - float".
        elif (u == cfg.tv_sym_pos) and isinstance(v, float):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ - Ƿ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.null_sym)

        # Process "Ƿ - -Ƿ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ - Ƿ²".
        elif (u == cfg.tv_sym_pos) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "Ƿ - -Ƿ²".
        elif (u == cfg.tv_sym_pos) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ - ∅".
        elif (u == cfg.tv_sym_pos) and (v == cfg.null_sym):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ - Æ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.real_num_sym_pos):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ - -Æ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.real_num_sym_neg):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ - ℝ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.real_num_sym):
            return (0.0, cfg.tv_sym_pos)


        # ------------------------------------------------------------------
        # Process "-Ƿ - (something)".
        # ------------------------------------------------------------------

        # Process "-Ƿ - float".
        elif (u == cfg.tv_sym_neg) and isinstance(v, float):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ - Ƿ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ - -Ƿ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.null_sym)

        # Process "-Ƿ - Ƿ²".
        elif (u == cfg.tv_sym_neg) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ - -Ƿ²".
        elif (u == cfg.tv_sym_neg) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "-Ƿ - ∅".
        elif (u == cfg.tv_sym_neg) and (v == cfg.null_sym):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ - Æ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.real_num_sym_pos):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ - -Æ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.real_num_sym_neg):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ - ℝ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.real_num_sym):
            return (0.0, cfg.tv_sym_neg)


        # ------------------------------------------------------------------
        # Process "Ƿ² - (something)".
        # ------------------------------------------------------------------

        # Process "Ƿ² - float".
        elif (u == cfg.tv_sym_pwr_p2_pos) and isinstance(v, float):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² - Ƿ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² - -Ƿ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² - Ƿ²".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.null_sym)

        # Process "Ƿ² - -Ƿ²".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

       # Process "Ƿ² - ∅".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.null_sym):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² - Æ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.real_num_sym_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² - -Æ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.real_num_sym_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² - ℝ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.real_num_sym):
            return (0.0, cfg.tv_sym_pwr_p2_pos)


        # ------------------------------------------------------------------
        # Process "-Ƿ² - (something)".
        # ------------------------------------------------------------------

        # Process "-Ƿ² - float".
        elif (u == cfg.tv_sym_pwr_p2_neg) and isinstance(v, float):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² - Ƿ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² - -Ƿ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² - Ƿ²".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² - -Ƿ²".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.null_sym)

        # Process "-Ƿ² - ∅".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.null_sym):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² - Æ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.real_num_sym_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² - -Æ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.real_num_sym_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² - ℝ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.real_num_sym):
            return (0.0, cfg.tv_sym_pwr_p2_neg)


        # ------------------------------------------------------------------
        # Process "∅ - (something)".
        # ------------------------------------------------------------------

        # Process "∅ - float".
        elif (u == cfg.null_sym) and isinstance(v, float):
            return (-v, cfg.null_sym)

        # Process "∅ - Ƿ".
        elif (u == cfg.null_sym) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_neg)

        # Process "∅ - -Ƿ".
        elif (u == cfg.null_sym) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pos)

        # Process "∅ - Ƿ²".
        elif (u == cfg.null_sym) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "∅ - -Ƿ²".
        elif (u == cfg.null_sym) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "∅ - ∅".
        elif (u == cfg.null_sym) and (v == cfg.null_sym):
            return (0.0, cfg.null_sym)

        # Process "∅ - Æ".
        elif (u == cfg.null_sym) and (v == cfg.real_num_sym_pos):
            return (cfg.real_num_sym_neg, cfg.null_sym)

        # Process "∅ - -Æ".
        elif (u == cfg.null_sym) and (v == cfg.real_num_sym_neg):
            return (cfg.real_num_sym_pos, cfg.null_sym)

        # Process "∅ - ℝ".
        elif (u == cfg.null_sym) and (v == cfg.real_num_sym):
            return (cfg.real_num_sym, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "Æ - (something)".
        # ------------------------------------------------------------------

        # Process "Æ - float".
        elif (u == cfg.real_num_sym_pos) and isinstance(v, float):
            if v == 0:
                return (cfg.real_num_sym_pos, cfg.null_sym)
            else:
                return cfg.unimplemented_sym

        # Process "Æ - Ƿ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_neg)

        # Process "Æ - -Ƿ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pos)

        # Process "Æ - Ƿ²".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "Æ - -Ƿ²".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Æ - ∅".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.null_sym):
            return (cfg.real_num_sym_pos, cfg.null_sym)

        # Process "Æ - Æ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.real_num_sym_pos):
            return cfg.unimplemented_sym

        # Process "Æ - -Æ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.real_num_sym_neg):
            return (cfg.real_num_sym_pos, cfg.null_sym)

        # Process "Æ - ℝ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.real_num_sym):
            return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "-Æ - (something)".
        # ------------------------------------------------------------------

        # Process "-Æ - float".
        elif (u == cfg.real_num_sym_neg) and isinstance(v, float):
            if v == 0:
                return (cfg.real_num_sym_neg, cfg.null_sym)
            else:
                return cfg.unimplemented_sym

        # Process "-Æ - Ƿ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Æ - -Ƿ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pos)

        # Process "-Æ - Ƿ²".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Æ - -Ƿ²".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "-Æ - ∅".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.null_sym):
            return (cfg.real_num_sym_neg, cfg.null_sym)

        # Process "-Æ - Æ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.real_num_sym_pos):
            return (cfg.real_num_sym_neg, cfg.null_sym)

        # Process "-Æ - -Æ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.real_num_sym_neg):
            return cfg.unimplemented_sym

        # Process "-Æ - ℝ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.real_num_sym):
            return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "ℝ - (something)".
        # ------------------------------------------------------------------

        # Process "ℝ - float".
        elif (u == cfg.real_num_sym) and isinstance(v, float):
            return (cfg.real_num_sym, cfg.null_sym)

        # Process "ℝ - Ƿ".
        elif (u == cfg.real_num_sym) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_neg)

        # Process "ℝ - -Ƿ".
        elif (u == cfg.real_num_sym) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pos)

        # Process "ℝ - Ƿ²".
        elif (u == cfg.real_num_sym) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "ℝ - -Ƿ²".
        elif (u == cfg.real_num_sym) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "ℝ - ∅".
        elif (u == cfg.real_num_sym) and (v == cfg.null_sym):
            return (cfg.real_num_sym, cfg.null_sym)

        # Process "ℝ - Æ".
        elif (u == cfg.real_num_sym) and (v == cfg.real_num_sym_pos):
            return cfg.unimplemented_sym

        # Process "ℝ - -Æ".
        elif (u == cfg.real_num_sym) and (v == cfg.real_num_sym_neg):
            return cfg.unimplemented_sym

        # Process "ℝ - ℝ".
        elif (u == cfg.real_num_sym) and (v == cfg.real_num_sym):
            return cfg.unimplemented_sym


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
        # ● Process the subtraction of two well-formed tuples.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

        # This subtracts two well-formed tuples by separately subtracting 
        # their real elements and their transvalent elements, using the rules 
        # defined above for the subtraction of lone elements.

        elif isinstance(u, tuple) and isinstance(v, tuple):

            if cfg.debugging_mode is True:
                print("Beginning subtraction of two tuples.")

            # This subtracts one transvalent tuple from another; i.e., 
            # it calculates the value of: (a, b) - (c, d), where:
            a = u[0]
            b = u[1]
            c = v[0]
            d = v[1]

            # If any of the tuples' elements is the "Unimplemented" symbol, 
            # return a result indicating that the operation cannot be 
            # processed.
            if (a == cfg.unimplemented_sym) \
                    | (b == cfg.unimplemented_sym) \
                    | (c == cfg.unimplemented_sym) \
                    | (d == cfg.unimplemented_sym):
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the difference of a and c as the difference of 
            # two lone elements.
            # ------------------------------------------------------------------

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(
                "(" + str(a) + " - " + str(c) + ")"
                )

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            diff_of_a_and_c = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("difference of real elements: ", diff_of_a_and_c)

            # ------------------------------------------------------------------
            # Determine the difference of b and d as the difference of 
            # two lone elements.
            # ------------------------------------------------------------------

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(
                "(" + str(b) + " - " + str(d) + ")"
                )

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            diff_of_b_and_d = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("difference of transvalent elements: ", diff_of_b_and_d)

            # ------------------------------------------------------------------
            # Determine the sum of (a-c) and (b-d) as the sum of 
            # two lone elements.
            # ------------------------------------------------------------------

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(
                "(" + str(diff_of_a_and_c[0]) + " + " + str(diff_of_b_and_d[1]) + ")"
                )

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            sum_of_a_minus_c_and_b_minus_d = \
                parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("difference of tuples: ", sum_of_a_minus_c_and_b_minus_d)

            return sum_of_a_minus_c_and_b_minus_d


        # If none of the steps above have been able to successfully
        # handle the subtraction operation, return the Unimplemented symbol.
        else:
            return cfg.unimplemented_sym


    @_('expr PLUS expr')
    def expr(self, p):
        """
        Specifies how the addition operation is evaluated
        within the context of transvalent mathematics.
        """

        if cfg.debugging_mode is True:
            print("Beginning addition of: ", str(p.expr0), "and", str(p.expr1))
            print("   ... of types: ", str(type(p.expr0)), "and", str(type(p.expr1)))

        # Assign the argument expressions to variables, to simplify
        # operations involving them.
        u = p.expr0
        v = p.expr1

        # If both u *and* v are lone elements, then they can be processed
        # directly as specified further below. Similarly, if both u *and* v 
        # are already well-formed tuples, they can be processed as specified
        # further below. However, if one of u or v is a lone element and the
        # other is a tuple, the lone element should be converted to a tuple
        # here, so that they can be processed below as two tuples.
        #
        # Note that technically, this only checks whether they are tuples;
        # to be more rigorous and eliminate errors, it should check whether
        # they are *well-formed* transvalent tuples.
        if isinstance(u, tuple) and (not isinstance(v, tuple)):
            v = convert_lone_element_to_tuple(v)
        elif (not isinstance(u, tuple)) and isinstance(v, tuple):
            u = convert_lone_element_to_tuple(u)

        if cfg.debugging_mode is True:
            print("Continuing with addition of: ", str(u), "and", str(v))


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
        # ● Process the addition of lone elements (e.g., a transvalent 
        # ● symbol *or* float with another such variable), generating a
        # ● well-formed transvalent tuple as output.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

        # If either u or v is the Unimplemented symbol, return the
        # Unimplemented symbol as the operation's result.
        if (u == cfg.unimplemented_sym) | (u == cfg.unimplemented_sym):
            return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "float + (something)".
        # ------------------------------------------------------------------

        # Process "float + float".
        if isinstance(u, float) and isinstance(v, float):
            return (u + v, cfg.null_sym)

        # Process "float + Ƿ".
        elif isinstance(u, float) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pos)

        # Process "float + -Ƿ".
        elif isinstance(u, float) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_neg)

        # Process "float + Ƿ²".
        elif isinstance(u, float) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "float + -Ƿ²".
        elif isinstance(u, float) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "float + ∅".
        elif isinstance(u, float)  and (v == cfg.null_sym):
            return (u, cfg.null_sym)

        # Process "float + Æ".
        elif isinstance(u, float) and (v == cfg.real_num_sym_pos):
            if u == 0:
                return (cfg.real_num_sym_pos, cfg.null_sym)
            else:
                return cfg.unimplemented_sym

        # Process "float + -Æ".
        elif isinstance(u, float) and (v == cfg.real_num_sym_neg):
            if u == 0:
                return (cfg.real_num_sym_neg, cfg.null_sym)
            else:
                return cfg.unimplemented_sym

        # Process "float + ℝ".
        elif isinstance(u, float) and (v == cfg.real_num_sym):
            if u == 0:
                return (cfg.real_num_sym, cfg.null_sym)
            else:
                return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "Ƿ + (something)".
        # ------------------------------------------------------------------

        # Process "Ƿ + float".
        elif (u == cfg.tv_sym_pos) and isinstance(v, float):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ + Ƿ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ + -Ƿ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.null_sym)

        # Process "Ƿ + Ƿ²".
        elif (u == cfg.tv_sym_pos) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ + -Ƿ²".
        elif (u == cfg.tv_sym_pos) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "Ƿ + ∅".
        elif (u == cfg.tv_sym_pos) and (v == cfg.null_sym):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ + Æ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.real_num_sym_pos):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ + -Æ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.real_num_sym_neg):
            return (0.0, cfg.tv_sym_pos)

        # Process "Ƿ + ℝ".
        elif (u == cfg.tv_sym_pos) and (v == cfg.real_num_sym):
            return (0.0, cfg.tv_sym_pos)


        # ------------------------------------------------------------------
        # Process "-Ƿ + (something)".
        # ------------------------------------------------------------------

        # Process "-Ƿ + float".
        elif (u == cfg.tv_sym_neg) and isinstance(v, float):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ + Ƿ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.null_sym)

        # Process "-Ƿ + -Ƿ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ + Ƿ²".
        elif (u == cfg.tv_sym_neg) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "-Ƿ + -Ƿ²".
        elif (u == cfg.tv_sym_neg) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ + ∅".
        elif (u == cfg.tv_sym_neg) and (v == cfg.null_sym):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ + Æ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.real_num_sym_pos):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ + -Æ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.real_num_sym_neg):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Ƿ + ℝ".
        elif (u == cfg.tv_sym_neg) and (v == cfg.real_num_sym):
            return (0.0, cfg.tv_sym_neg)


        # ------------------------------------------------------------------
        # Process "Ƿ² + (something)".
        # ------------------------------------------------------------------

        # Process "Ƿ² + float".
        elif (u == cfg.tv_sym_pwr_p2_pos) and isinstance(v, float):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² + Ƿ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² + -Ƿ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² + Ƿ²".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² + -Ƿ²".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.null_sym)

        # Process "Ƿ² + ∅".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.null_sym):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² + Æ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.real_num_sym_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² + -Æ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.real_num_sym_neg):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Ƿ² + ℝ".
        elif (u == cfg.tv_sym_pwr_p2_pos) and (v == cfg.real_num_sym):
            return (0.0, cfg.tv_sym_pwr_p2_pos)


        # ------------------------------------------------------------------
        # Process "-Ƿ² + (something)".
        # ------------------------------------------------------------------

        # Process "-Ƿ² + float".
        elif (u == cfg.tv_sym_pwr_p2_neg) and isinstance(v, float):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² + Ƿ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² + -Ƿ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² + Ƿ²".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.null_sym)

        # Process "-Ƿ² + -Ƿ²".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² + ∅".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.null_sym):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² + Æ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.real_num_sym_pos):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² + -Æ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.real_num_sym_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Ƿ² + ℝ".
        elif (u == cfg.tv_sym_pwr_p2_neg) and (v == cfg.real_num_sym):
            return (0.0, cfg.tv_sym_pwr_p2_neg)


        # ------------------------------------------------------------------
        # Process "∅ + (something)".
        # ------------------------------------------------------------------

        # Process "∅ + float".
        elif (u == cfg.null_sym) and isinstance(v, float):
            return (v, cfg.null_sym)

        # Process "∅ + Ƿ".
        elif (u == cfg.null_sym) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pos)

        # Process "∅ + -Ƿ".
        elif (u == cfg.null_sym) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_neg)

        # Process "∅ + Ƿ²".
        elif (u == cfg.null_sym) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "∅ + -Ƿ²".
        elif (u == cfg.null_sym) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "∅ + ∅".
        elif (u == cfg.null_sym) and (v == cfg.null_sym):
            return (0.0, cfg.null_sym)

        # Process "∅ + Æ".
        elif (u == cfg.null_sym) and (v == cfg.real_num_sym_pos):
            return (cfg.real_num_sym_pos, cfg.null_sym)

        # Process "∅ + -Æ".
        elif (u == cfg.null_sym) and (v == cfg.real_num_sym_neg):
            return (cfg.real_num_sym_neg, cfg.null_sym)

        # Process "∅ + ℝ".
        elif (u == cfg.null_sym) and (v == cfg.real_num_sym):
            return (cfg.real_num_sym, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "Æ + (something)".
        # ------------------------------------------------------------------

        # Process "Æ + float".
        elif (u == cfg.real_num_sym_pos) and isinstance(v, float):
            if v == 0:
                return (cfg.real_num_sym_pos, cfg.null_sym)
            else:
                return cfg.unimplemented_sym

        # Process "Æ + Ƿ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pos)

        # Process "Æ + -Ƿ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_neg)

        # Process "Æ + Ƿ²".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "Æ + -Ƿ²".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "Æ + ∅".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.null_sym):
            return (cfg.real_num_sym_pos, cfg.null_sym)

        # Process "Æ + Æ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.real_num_sym_pos):
            return (cfg.real_num_sym_pos, cfg.null_sym)

        # Process "Æ + -Æ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.real_num_sym_neg):
            return cfg.unimplemented_sym

        # Process "Æ + ℝ".
        elif (u == cfg.real_num_sym_pos) and (v == cfg.real_num_sym):
            return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "-Æ + (something)".
        # ------------------------------------------------------------------

        # Process "-Æ + float".
        elif (u == cfg.real_num_sym_neg) and isinstance(v, float):
            if v == 0:
                return (cfg.real_num_sym_neg, cfg.null_sym)
            else:
                return cfg.unimplemented_sym

        # Process "-Æ + Ƿ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pos)

        # Process "-Æ + -Ƿ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_neg)

        # Process "-Æ + Ƿ²".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "-Æ + -Ƿ²".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "-Æ + ∅".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.null_sym):
            return (cfg.real_num_sym_neg, cfg.null_sym)

        # Process "-Æ + Æ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.real_num_sym_pos):
            return cfg.unimplemented_sym

        # Process "-Æ + -Æ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.real_num_sym_neg):
            return (cfg.real_num_sym_neg, cfg.null_sym)

        # Process "-Æ + ℝ".
        elif (u == cfg.real_num_sym_neg) and (v == cfg.real_num_sym):
            return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "ℝ + (something)".
        # ------------------------------------------------------------------

        # Process "ℝ + float".
        elif (u == cfg.real_num_sym) and isinstance(v, float):
            if v == 0:
                return (0.0, cfg.real_num_sym)
            else:
                return cfg.unimplemented_sym

        # Process "ℝ + Ƿ".
        elif (u == cfg.real_num_sym) and (v == cfg.tv_sym_pos):
            return (0.0, cfg.tv_sym_pos)

        # Process "ℝ + -Ƿ".
        elif (u == cfg.real_num_sym) and (v == cfg.tv_sym_neg):
            return (0.0, cfg.tv_sym_neg)

        # Process "ℝ + Ƿ²".
        elif (u == cfg.real_num_sym) and (v == cfg.tv_sym_pwr_p2_pos):
            return (0.0, cfg.tv_sym_pwr_p2_pos)

        # Process "ℝ + -Ƿ²".
        elif (u == cfg.real_num_sym) and (v == cfg.tv_sym_pwr_p2_neg):
            return (0.0, cfg.tv_sym_pwr_p2_neg)

        # Process "ℝ + ∅".
        elif (u == cfg.real_num_sym) and (v == cfg.null_sym):
            return (cfg.real_num_sym, cfg.null_sym)

        # Process "ℝ + Æ".
        elif (u == cfg.real_num_sym) and (v == cfg.real_num_sym_pos):
            return cfg.unimplemented_sym

        # Process "ℝ + -Æ".
        elif (u == cfg.real_num_sym) and (v == cfg.real_num_sym_neg):
            return cfg.unimplemented_sym

        # Process "ℝ + ℝ".
        elif (u == cfg.real_num_sym) and (v == cfg.real_num_sym):
            return cfg.unimplemented_sym


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
        # ● Process the addition of two well-formed tuples.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

        # This adds two well-formed tuples by separately adding their real
        # elements and their transvalent elements, using the rules defined
        # above for the addition of lone elements.

        elif isinstance(u, tuple) and isinstance(v, tuple):

            if cfg.debugging_mode is True:
                print("Beginning addition of two tuples.")

            # The steps below will add one transvalent tuple to another; 
            # i.e., it calculates the value of: (a, b) + (c, d), where:
            a = u[0]
            b = u[1]
            c = v[0]
            d = v[1]

            # If any of the tuples' elements is the Unimplemented symbol, 
            # return a result indicating that the operation cannot be 
            # processed.
            if (a == cfg.unimplemented_sym) \
                    | (b == cfg.unimplemented_sym) \
                    | (c == cfg.unimplemented_sym) \
                    | (d == cfg.unimplemented_sym):
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the sum of a and c as the sum of two lone elements.
            # ------------------------------------------------------------------

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(
                "(" + str(a) + " + " + str(c) + ")"
                )

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            sum_of_a_and_c = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("sum of real elements: ", sum_of_a_and_c)

            # ------------------------------------------------------------------
            # Determine the sum of b and d as the sum of two lone elements.
            # ------------------------------------------------------------------

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(
                "(" + str(b) + " + " + str(d) + ")"
                )

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            sum_of_b_and_d = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("sum of transvalent elements: ", sum_of_b_and_d)

            if sum_of_b_and_d == cfg.unimplemented_sym:
                return cfg.unimplemented_sym

            # ------------------------------------------------------------------
            # Determine the sum of (a+c) and (b+d) as the sum of 
            # two lone elements.
            # ------------------------------------------------------------------

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(
                "(" + str(sum_of_a_and_c[0]) + " + " + str(sum_of_b_and_d[1]) + ")"
                )

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            sum_of_a_and_c_and_b_and_d = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("sum of tuples: ", sum_of_a_and_c_and_b_and_d)

            return sum_of_a_and_c_and_b_and_d


        # If none of the steps above have been able to successfully
        # handle the addition operation, return the Unimplemented symbol.
        else:
            return cfg.unimplemented_sym


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

        if cfg.debugging_mode is True:
            print("Beginning multiplication of: ",
                str(p.expr0), "and", str(p.expr1)
                )
            print("   ... of types: ",
                str(type(p.expr0)), "and", str(type(p.expr1))
                )

        # Assign the argument expressions to variables, to simplify
        # operations involving them.
        u = p.expr0
        v = p.expr1

        # If both u *and* v are lone elements, then they can be processed
        # directly as specified further below. Similarly, if both u *and* v 
        # are already well-formed tuples, they can be processed as specified
        # further below. However, if one of u or v is a lone element and the
        # other is a tuple, the lone element should be converted to a tuple
        # here, so that they can be processed below as two tuples.
        #
        # Note that technically, this only checks whether they are tuples;
        # to be more rigorous and eliminate errors, it should check whether
        # they are *well-formed* transvalent tuples.
        if isinstance(u, tuple) and (not isinstance(v, tuple)):
            v = convert_lone_element_to_tuple(v)
        elif (not isinstance(u, tuple)) and isinstance(v, tuple):
            u = convert_lone_element_to_tuple(u)

        if cfg.debugging_mode is True:
            print("Continuing with multiplication of: ",
                str(u), "and", str(v)
                )


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
        # ● Process the multiplication of lone elements (e.g., a transvalent
        # ● symbol *or* float with another such variable), generating a
        # ● well-formed transvalent tuple as output.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

        # If either of the terms is the "Unimplemented" symbol, return
        # a result indicating that the operation cannot be processed.
        if (u == cfg.unimplemented_sym) | (v == cfg.unimplemented_sym):
            return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "positive float × (something)".
        # ------------------------------------------------------------------
        if isinstance(u, float) and (u > 0):

            # Process "positive float × positive float".
            # Process "positive float × negative float".
            # Process "positive float × 0".
            if isinstance(v, float):
                return (u*v, cfg.null_sym)

            # Process "positive float × Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_pos)

            # Process "positive float × -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_neg)

            # Process "positive float × Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "positive float × -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "positive float × ∅".
            elif v == cfg.null_sym:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "negative float × (something)".
        # ------------------------------------------------------------------
        elif isinstance(u, float) and (u < 0):

            # Process "negative float × positive float".
            # Process "negative float × negative float".
            # Process "negative float × 0".
            if isinstance(v, float):
                return (u*v, cfg.null_sym)

            # Process "negative float × Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_neg)

            # Process "negative float × -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_pos)

            # Process "negative float × Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "negative float × -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "negative float × ∅".
            elif v == cfg.null_sym:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "0 × (something)".
        # ------------------------------------------------------------------
        elif u == 0:

            # Process "0 × positive float".
            # Process "0 × negative float".
            # Process "0 × 0".
            if isinstance(v, float):
                return (0.0, cfg.null_sym)

            # Process "0 × Ƿ".
            elif v == cfg.tv_sym_pos:
                return (cfg.real_num_sym_pos, cfg.null_sym)

            # Process "0 × -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (cfg.real_num_sym_neg, cfg.null_sym)

            # Process "0 × Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pos)

            # Process "0 × -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_neg)

            # Process "0 × ∅".
            elif v == cfg.null_sym:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "Ƿ × (something)".
        # ------------------------------------------------------------------
        elif u == cfg.tv_sym_pos:

            # Process "Ƿ × positive float".
            if isinstance(v, float) and (v > 0):
                return (0.0, cfg.tv_sym_pos)

            # Process "Ƿ × negative float".
            elif isinstance(v, float) and (v < 0):
                return (0.0, cfg.tv_sym_neg)

            # Process "Ƿ × 0".
            elif v == 0:
                return (cfg.real_num_sym_pos, cfg.null_sym)

            # Process "Ƿ × Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "Ƿ × -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "Ƿ × Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_p3_pos)

            # Process "Ƿ × -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_p3_neg)

            # Process "Ƿ × ∅".
            elif v == cfg.null_sym:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "-Ƿ × (something)".
        # ------------------------------------------------------------------
        elif u == cfg.tv_sym_neg:

            # Process "-Ƿ × positive float".
            if isinstance(v, float) and (v > 0):
                return (0.0, cfg.tv_sym_neg)

            # Process "-Ƿ × negative float".
            elif isinstance(v, float) and (v < 0):
                return (0.0, cfg.tv_sym_pos)

            # Process "-Ƿ × 0".
            elif v == 0:
                return (cfg.real_num_sym_neg, cfg.null_sym)

            # Process "-Ƿ × Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "-Ƿ × -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "-Ƿ × Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_p3_neg)

            # Process "-Ƿ × -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_p3_pos)

            # Process "-Ƿ × ∅".
            elif v == cfg.null_sym:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "Ƿ² × (something)".
        # ------------------------------------------------------------------
        elif u == cfg.tv_sym_pwr_p2_pos:

            # Process "Ƿ² × positive float".
            if isinstance(v, float) and (v > 0):
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "Ƿ² × negative float".
            elif isinstance(v, float) and (v < 0):
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "Ƿ² × 0".
            elif v == 0:
                return (0.0, cfg.tv_sym_pos)

            # Process "Ƿ² × Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_pwr_p3_pos)

            # Process "Ƿ² × -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_pwr_p3_neg)

            # Process "Ƿ² × Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_p4_pos)

            # Process "Ƿ² × -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_p4_neg)

            # Process "Ƿ² × ∅".
            elif v == cfg.null_sym:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "-Ƿ² × (something)".
        # ------------------------------------------------------------------
        elif u == cfg.tv_sym_pwr_p2_neg:

            # Process "-Ƿ² × positive float".
            if isinstance(v, float) and (v > 0):
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "-Ƿ² × negative float".
            elif isinstance(v, float) and (v < 0):
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "-Ƿ² × 0".
            elif v == 0:
                return (0.0, cfg.tv_sym_neg)

            # Process "-Ƿ² × Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_pwr_p3_neg)

            # Process "-Ƿ² × -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_pwr_p3_pos)

            # Process "-Ƿ² × Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_p4_neg)

            # Process "-Ƿ² × -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_p4_pos)

            # Process "-Ƿ² × ∅".
            elif v == cfg.null_sym:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "∅ × (something)".
        # ------------------------------------------------------------------
        elif u == cfg.null_sym:
            # Process "∅ × positive float".
            # Process "∅ × negative float".
            # Process "∅ × 0".
            # Process "∅ × Ƿ".
            # Process "∅ × -Ƿ".
            # Process "∅ × Ƿ²".
            # Process "∅ × -Ƿ²".
            # Process "∅ × ∅".
            return (0.0, cfg.null_sym)


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
        # ● Process the multiplication of two well-formed tuples.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

        # This multiplies two well-formed tuples by using the rules
        # defined above for the multiplication of lone elements (and the
        # rules for addition of tuples and lone elements).

        # Multiplication of two tuples is calculated in the following manner:
        # (a, b) × (c, d) = (a × c) + (a × d) + (b × c) + (b × d)

        elif isinstance(u, tuple) and isinstance(v, tuple):

            # This multiplies one well-formed tuple by another; i.e., it 
            # calculates the value of: (a, b) × (c, d), where:
            a = u[0]
            b = u[1]
            c = v[0]
            d = v[1]

            # If any of the tuples' elements is the "Unimplemented" symbol, 
            # return a result indicating that the operation cannot be 
            # processed.
            if (a == cfg.unimplemented_sym) \
                    | (b == cfg.unimplemented_sym) \
                    | (c == cfg.unimplemented_sym) \
                    | (d == cfg.unimplemented_sym):
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the product of "(a × c)".
            # ------------------------------------------------------------------

            # Create a new "input" string to be lexed and parsed
            # that requests the product of a × c.
            input_string = "(" + str(a) + " * " + str(c) + ")"
            if cfg.debugging_mode is True:
                print("input_string: ", input_string)
            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(input_string)

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            result_subordinate = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("parsed result: ", result_subordinate)

            a_times_c = result_subordinate
            if cfg.debugging_mode is True:
                print("a_times_c: ", a_times_c)

            if a_times_c == cfg.unimplemented_sym:
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the product of "(a × d)".
            # ------------------------------------------------------------------

            # Create a new "input" string to be lexed and parsed
            # that requests the product of a × d.
            input_string = "(" + str(a) + " * " + str(d) + ")"
            if cfg.debugging_mode is True:
                print("input_string: ", input_string)
            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(input_string)

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            result_subordinate = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("parsed result: ", result_subordinate)

            a_times_d = result_subordinate
            if cfg.debugging_mode is True:
                print("a_times_d: ", a_times_d)

            if a_times_d == cfg.unimplemented_sym:
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the product of "(b × c)".
            # ------------------------------------------------------------------

            input_string = "(" + str(b) + " * " + str(c) + ")"
            if cfg.debugging_mode is True:
                print("input_string: ", input_string)
            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(input_string)

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            result_subordinate = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("parsed result: ", result_subordinate)

            b_times_c = result_subordinate
            if cfg.debugging_mode is True:
                print("b_times_c: ", b_times_c)

            if b_times_c == cfg.unimplemented_sym:
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the product of "(b × d)".
            # ------------------------------------------------------------------

            input_string = "(" + str(b) + " * " + str(d) + ")"
            if cfg.debugging_mode is True:
                print("input_string: ", input_string)
            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(input_string)

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            result_subordinate = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("parsed result: ", result_subordinate)

            b_times_d = result_subordinate
            if cfg.debugging_mode is True:
                print("b_times_d: ", b_times_d)

            if b_times_d == cfg.unimplemented_sym:
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the sum of "a_times_c + a_times_d".
            # ------------------------------------------------------------------

            input_string = "(" \
                + str(a_times_c[0]) + " + " \
                + str(a_times_c[1]) + " + " \
                + str(a_times_d[0]) + " + " \
                + str(a_times_d[1]) \
                + ")"
            if cfg.debugging_mode is True:
                print("a_times_c + a_times_d input_string: ", input_string)

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(input_string)

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            result_subordinate = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("a_times_c_plus_a_times_d parsed result: ",
                    result_subordinate
                    )

            a_times_c_plus_a_times_d = result_subordinate

            if a_times_c_plus_a_times_d == cfg.unimplemented_sym:
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the sum of "a_times_c_plus_a_times_d + b_times_c".
            # ------------------------------------------------------------------

            input_string = "(" \
                + str(a_times_c_plus_a_times_d[0]) + " + " \
                + str(a_times_c_plus_a_times_d[1]) + " + " \
                + str(b_times_c[0]) + " + " \
                + str(b_times_c[1]) \
                + ")"
            if cfg.debugging_mode is True:
                print("input_string: ", input_string)

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(input_string)

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            result_subordinate = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print("a_times_c_plus_a_times_d_plus_b_times_c parsed result: ",
                    result_subordinate
                    )

            a_times_c_plus_a_times_d_plus_b_times_c = result_subordinate

            if a_times_c_plus_a_times_d_plus_b_times_c == cfg.unimplemented_sym:
                return cfg.unimplemented_sym


            # ------------------------------------------------------------------
            # Determine the sum of 
            # "a_times_c_plus_a_times_d_plus_b_times_c + b_times_d".
            # ------------------------------------------------------------------

            input_string = "(" \
                + str(a_times_c_plus_a_times_d_plus_b_times_c[0]) + " + " \
                + str(a_times_c_plus_a_times_d_plus_b_times_c[1]) + " + " \
                + str(b_times_d[0]) + " + " \
                + str(b_times_d[1]) \
                + ")"
            if cfg.debugging_mode is True:
                print("input_string: ", input_string)

            lexer_subordinate = LiniaroteLexer()
            tokens_subordinate = lexer_subordinate.tokenize(input_string)

            # It's necessary to create a new parser.
            parser_subordinate = LiniaroteParser()

            result_subordinate = parser_subordinate.parse(tokens_subordinate)
            if cfg.debugging_mode is True:
                print(
                    "a_times_c_plus_a_times_d_plus_b_times_c_plus_b_times_d parsed result: ",
                    result_subordinate
                    )

            a_times_c_plus_a_times_d_plus_b_times_c_plus_b_times_d = result_subordinate

            if a_times_c_plus_a_times_d_plus_b_times_c_plus_b_times_d == cfg.unimplemented_sym:
                return cfg.unimplemented_sym
            else:
                return a_times_c_plus_a_times_d_plus_b_times_c_plus_b_times_d


        # If none of the steps above have been able to successfully
        # handle the multiplication operation, return the Unimplemented 
        # symbol.
        else:
            return cfg.unimplemented_sym


    @_('expr DIVIDE expr')
    def expr(self, p):
        """
        Specifies how the division operation is evaluated
        within the context of transvalent mathematics.
        """

        if cfg.debugging_mode is True:
            print("Beginning division of: ", str(p.expr0), "and", str(p.expr1))
            print("   ... of types: ", 
                str(type(p.expr0)), "and", str(type(p.expr1))
                )

        # Assign the argument expressions to variables, to simplify
        # operations involving them.
        u = p.expr0
        v = p.expr1

        # If both u *and* v are lone elements, then they can be processed
        # directly as specified further below. Similarly, if both u *and* v 
        # are already well-formed tuples, they can be processed as specified
        # further below. However, if one of u or v is a lone element and the
        # other is a tuple, the lone element should be converted to a tuple
        # here, so that they can be processed below as two tuples.
        #
        # Note that technically, this only checks whether they are tuples;
        # to be more rigorous and eliminate errors, it should check whether
        # they are *well-formed* transvalent tuples.
        if isinstance(u, tuple) and (not isinstance(v, tuple)):
            v = convert_lone_element_to_tuple(v)
        elif (not isinstance(u, tuple)) and isinstance(v, tuple):
            u = convert_lone_element_to_tuple(u)

        if cfg.debugging_mode is True:
            print("Continuing with division of: ", str(u), "and", str(v))


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
        # ● Process the division of lone elements (e.g., a transvalent 
        # ● symbol *or* float with another such variable), generating a
        # ● well-formed transvalent tuple as output.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

        # If either of the terms is the Unimplemented symbol, return
        # a result indicating that the operation cannot be processed.
        if (u == cfg.unimplemented_sym) | (v == cfg.unimplemented_sym):
            return cfg.unimplemented_sym


        # ------------------------------------------------------------------
        # Process "positive float ÷ (something)".
        # ------------------------------------------------------------------
        if isinstance(u, float) and (u > 0):

            # Process "positive float ÷ positive float".
            # Process "positive float ÷ negative float".
            if isinstance(v, float) and (v != 0):
                return (u/v, cfg.null_sym)

            # Process "positive float ÷ 0".
            elif isinstance(v, float) and (v == 0):
                return (0.0, cfg.tv_sym_pos)

            # Process "positive float ÷ Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.null_sym)

            # Process "positive float ÷ -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.null_sym)

            # Process "positive float ÷ Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_m2_pos)

            # Process "positive float ÷ -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_m2_neg)


        # ------------------------------------------------------------------
        # Process "negative float ÷ (something)".
        # ------------------------------------------------------------------
        elif isinstance(u, float) and (u < 0):

            # Process "negative float ÷ positive float".
            # Process "negative float ÷ negative float".
            if isinstance(v, float) and (v != 0):
                return (u/v, cfg.null_sym)

            # Process "negative float ÷ 0".
            elif isinstance(v, float) and (v == 0):
                return (0.0, cfg.tv_sym_neg)

            # Process "negative float ÷ Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.null_sym)

            # Process "negative float ÷ -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.null_sym)

            # Process "negative float ÷ Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_m2_neg)

            # Process "negative float ÷ -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_m2_pos)


        # ------------------------------------------------------------------
        # Process "0 ÷ (something)".
        # ------------------------------------------------------------------
        elif u == 0:

            # Process "0 ÷ positive float".
            # Process "0 ÷ negative float".
            if isinstance(v, float) and (v != 0):
                return (0.0, cfg.null_sym)

            # Process "0 ÷ 0".
            elif isinstance(v, float) and (v == 0):
                return (cfg.real_num_sym, cfg.null_sym)

            # Process "0 ÷ Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_pwr_m2_pos)

            # Process "0 ÷ -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_pwr_m2_neg)

            # Process "0 ÷ Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.tv_sym_pwr_m3_pos)

            # Process "0 ÷ -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.tv_sym_pwr_m3_neg)


        # ------------------------------------------------------------------
        # Process "Ƿ ÷ (something)".
        # ------------------------------------------------------------------
        elif u == cfg.tv_sym_pos:

            # Process "Ƿ ÷ positive float".
            if isinstance(v, float) and (v > 0):
                return (0.0, cfg.tv_sym_pos)

            # Process "Ƿ ÷ negative float".
            elif isinstance(v, float) and (v < 0):
                return (0.0, cfg.tv_sym_neg)

            # Process "Ƿ ÷ 0".
            elif v == 0:
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "Ƿ ÷ Ƿ".
            elif v == cfg.tv_sym_pos:
                return (cfg.real_num_sym_pos, cfg.null_sym)

            # Process "Ƿ ÷ -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (cfg.real_num_sym_neg, cfg.null_sym)

            # Process "Ƿ ÷ Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.null_sym)

            # Process "Ƿ ÷ -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "-Ƿ ÷ (something)".
        # ------------------------------------------------------------------
        elif u == cfg.tv_sym_neg:

            # Process "-Ƿ ÷ positive float".
            if isinstance(v, float) and (v > 0):
                return (0.0, cfg.tv_sym_neg)

            # Process "-Ƿ ÷ negative float".
            elif isinstance(v, float) and (v < 0):
                return (0.0, cfg.tv_sym_pos)

            # Process "-Ƿ ÷ 0".
            elif v == 0:
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "-Ƿ ÷ Ƿ".
            elif v == cfg.tv_sym_pos:
                return (cfg.real_num_sym_neg, cfg.null_sym)

            # Process "-Ƿ ÷ -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (cfg.real_num_sym_pos, cfg.null_sym)

            # Process "-Ƿ ÷ Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (0.0, cfg.null_sym)

            # Process "-Ƿ ÷ -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (0.0, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "Ƿ² ÷ (something)".
        # ------------------------------------------------------------------
        elif u == cfg.tv_sym_pwr_p2_pos:

            # Process "Ƿ² ÷ positive float".
            if isinstance(v, float) and (v > 0):
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "Ƿ² ÷ negative float".
            elif isinstance(v, float) and (v < 0):
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "Ƿ² ÷ 0".
            elif v == 0:
                return (0.0, cfg.tv_sym_pwr_p3_pos)

            # Process "Ƿ² ÷ Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_pos)

            # Process "Ƿ² ÷ -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_neg)

            # Process "Ƿ² ÷ Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (cfg.real_num_sym_pos, cfg.null_sym)

            # Process "Ƿ² ÷ -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (cfg.real_num_sym_neg, cfg.null_sym)


        # ------------------------------------------------------------------
        # Process "-Ƿ² ÷ (something)".
        # ------------------------------------------------------------------
        elif u == cfg.tv_sym_pwr_p2_neg:

            # Process "-Ƿ² ÷ positive float".
            if isinstance(v, float) and (v > 0):
                return (0.0, cfg.tv_sym_pwr_p2_neg)

            # Process "-Ƿ² ÷ negative float".
            elif isinstance(v, float) and (v < 0):
                return (0.0, cfg.tv_sym_pwr_p2_pos)

            # Process "-Ƿ² ÷ 0".
            elif v == 0:
                return (0.0, cfg.tv_sym_pwr_p3_neg)

            # Process "-Ƿ² ÷ Ƿ".
            elif v == cfg.tv_sym_pos:
                return (0.0, cfg.tv_sym_neg)

            # Process "-Ƿ² ÷ -Ƿ".
            elif v == cfg.tv_sym_neg:
                return (0.0, cfg.tv_sym_pos)

            # Process "-Ƿ² ÷ Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_pos:
                return (cfg.real_num_sym_neg, cfg.null_sym)

            # Process "-Ƿ² ÷ -Ƿ²".
            elif v == cfg.tv_sym_pwr_p2_neg:
                return (cfg.real_num_sym_pos, cfg.null_sym)


        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●
        # ● Process the division of two well-formed tuples.
        # ●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●●

        elif isinstance(u, tuple) and isinstance(v, tuple):

            # This divides one well-formed tuple by another; i.e., it 
            # calculates the value of: (a, b) ÷ (c, d), where:
            a = u[0]
            b = u[1]
            c = v[0]
            d = v[1]

            # If any of the tuples' elements is the Unimplemented symbol, 
            # return a result indicating that the operation cannot be 
            # processed.
            if (a == cfg.unimplemented_sym) \
                    | (b == cfg.unimplemented_sym) \
                    | (c == cfg.unimplemented_sym) \
                    | (d == cfg.unimplemented_sym):
                return cfg.unimplemented_sym


            # NOTE! At the moment, some of the if statements below don't check
            # the values of a or c. But I haven't yet confirmed that the 
            # formulas will be true for ALL possible values of a and c.

            if (b == cfg.tv_sym_pos) and (d == cfg.tv_sym_pos):
                return (cfg.real_num_sym_pos, cfg.null_sym)

            elif (b == cfg.tv_sym_pos) and (d == cfg.tv_sym_neg):
                return (cfg.real_num_sym_neg, cfg.null_sym)

            elif (b == cfg.tv_sym_neg) and (d == cfg.tv_sym_pos):
                return (cfg.real_num_sym_neg, cfg.null_sym)

            elif (b == cfg.tv_sym_neg) and (d == cfg.tv_sym_neg):
                return (cfg.real_num_sym_pos, cfg.null_sym)

            elif (b == cfg.tv_sym_pos) and (d == cfg.null_sym):
                if isinstance(c, float) and (c > 0):
                    return (0.0, cfg.tv_sym_pos)
                elif isinstance(c, float) and (c < 0):
                    return (0.0, cfg.tv_sym_neg)
                elif c == 0:
                    return cfg.unimplemented_sym

            elif (b == cfg.tv_sym_neg) and (d == cfg.null_sym):
                if isinstance(c, float) and (c > 0):
                    return (0.0, cfg.tv_sym_neg)
                elif isinstance(c, float) and (c < 0):
                    return (0.0, cfg.tv_sym_pos)
                elif c == 0:
                    return cfg.unimplemented_sym

            elif (b == cfg.null_sym) and (d == cfg.tv_sym_pos):
                if a == 0:
                    return cfg.unimplemented_sym
                else:
                    return (0.0, cfg.null_sym)

            elif (b == cfg.null_sym) and (d == cfg.tv_sym_neg):
                if a == 0:
                    return cfg.unimplemented_sym
                else:
                    return (0.0, cfg.null_sym)

            elif (b == cfg.null_sym) and (d == cfg.null_sym):

                # Handle the subcase when:
                #    a is a positive real number and
                #    c is a positive real number.
                if ( isinstance(a, float) and (a > 0) ) \
                        and ( isinstance(c, float) and (c > 0) ):
                    return (a/c, cfg.null_sym)

                # Handle the subcase when:
                #    a is a positive real number and
                #    c is zero.
                elif ( isinstance(a, float) and (a > 0) ) \
                        and (c == 0):
                    return cfg.unimplemented_sym

                # Handle the subcase when:
                #    a is a positive real number and
                #    c is a negative real number.
                elif ( isinstance(a, float) and (a > 0) ) \
                        and ( isinstance(c, float) and (c < 0) ):
                    return (a/c, cfg.null_sym)

                # Handle the subcase when:
                #    a is zero and
                #    c is a positive real number.
                if (a == 0)  \
                        and ( isinstance(c, float) and (c > 0) ):
                    return cfg.unimplemented_sym

                # Handle the subcase when:
                #    a is zero and
                #    c is zero.
                if (a == 0) and (c == 0):
                    return cfg.unimplemented_sym

                # Handle the subcase when:
                #    a is zero and
                #    c is a negative real number.
                if (a == 0)  \
                        and ( isinstance(c, float) and (c < 0) ):
                    return cfg.unimplemented_sym

                # Handle the subcase when:
                #    a is a negative real number and
                #    c is a positive real number.
                elif ( isinstance(a, float) and (a < 0) ) \
                        and ( isinstance(c, float) and (c > 0) ):
                    return (a/c, cfg.null_sym)

                # Handle the subcase when:
                #    a is a negative real number and
                #    c is zero.
                elif ( isinstance(a, float) and (a < 0) ) \
                        and (c == 0):
                    return cfg.unimplemented_sym

                # Handle the subcase when:
                #    a is a negative real number and
                #    c is a negative real number.
                elif ( isinstance(a, float) and (a < 0) ) \
                        and ( isinstance(c, float) and (c < 0) ):
                    return (a/c, cfg.null_sym)


        # If none of the steps above have been able to successfully
        # handle the multiplication operation, return the Unimplemented 
        # symbol.
        else:
            return cfg.unimplemented_sym


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


    # ------------------------------------------------------------------
    # Define the recognition of transvalent symbols and other special
    # symbols.
    # ------------------------------------------------------------------

    @_('TRANSVALENT_SYMBOL_POSITIVE_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “Ƿ” string.
        """
        return cfg.tv_sym_pos


    @_('TRANSVALENT_SYMBOL_POWER_PLUS_TWO_POSITIVE_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “Ƿ²” string.
        """
        return cfg.tv_sym_pwr_p2_pos


    @_('TRANSVALENT_SYMBOL_POWER_PLUS_THREE_POSITIVE_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “Ƿ³” string.
        """
        return cfg.tv_sym_pwr_p3_pos


    @_('TRANSVALENT_SYMBOL_POWER_PLUS_FOUR_POSITIVE_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “Ƿ⁴” string.
        """
        return cfg.tv_sym_pwr_p4_pos


    @_('TRANSVALENT_SYMBOL_POWER_MINUS_TWO_POSITIVE_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “Ƿ⁻²” string.
        """
        return cfg.tv_sym_pwr_m2_pos


    @_('TRANSVALENT_SYMBOL_POWER_MINUS_THREE_POSITIVE_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “Ƿ⁻³” string.
        """
        return cfg.tv_sym_pwr_m3_pos


    @_('REAL_NUMBER_POSITIVE_SYMBOL_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “Æ” string.
        """
        return cfg.real_num_sym_pos


    @_('REAL_NUMBER_SYMBOL_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “ℝ” string.
        """
        return cfg.real_num_sym


    @_('NULL_SYMBOL_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “∅” string.
        """
        return cfg.null_sym


    @_('UNIMPLEMENTED_SYMBOL_INPUT')
    def factor(self, p):
        """
        Defines the processing of the “U” string.
        """
        return cfg.unimplemented_sym


    # ------------------------------------------------------------------
    # Handle the input of user-defined constants.
    # ------------------------------------------------------------------

    @_('ID')
    def factor(self, p):
        """
        Checks whether inputted text is an established variable.
        """
        return self.get_value_of_constant(p.ID)


    def get_value_of_constant(self, name):
        """
        Assigns the value to a new variable from via user input.
        """
        if name not in cfg.recognized_constants:
            cfg.recognized_constants[name] = \
                float(input(f"Please enter the desired value for {name}: "))
        return cfg.recognized_constants[name]


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define the formatter (to convert transvalent tuples or text for 
# █ display).
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def convert_lone_element_to_tuple(
    lone_element_u,
    ):
    """
    Converts a lone element (e.g., a float or "Ƿ") into a well-formed
    transvalent tuple upon which mathematical operations can be
    performed.
    """

    if isinstance(lone_element_u, float):
        return (lone_element_u, cfg.null_sym)

    elif lone_element_u == cfg.tv_sym_pos:
        return (0.0, cfg.tv_sym_pos)
    elif lone_element_u == cfg.tv_sym_neg:
        return (0.0, cfg.tv_sym_neg)

    elif lone_element_u == cfg.tv_sym_pwr_p2_pos:
        return (0.0, cfg.tv_sym_pwr_p2_pos)
    elif lone_element_u == cfg.tv_sym_pwr_p2_neg:
        return (0.0, cfg.tv_sym_pwr_p2_neg)

    elif lone_element_u == cfg.tv_sym_pwr_p3_pos:
        return (0.0, cfg.tv_sym_pwr_p3_pos)
    elif lone_element_u == cfg.tv_sym_pwr_p3_neg:
        return (0.0, cfg.tv_sym_pwr_p3_neg)

    elif lone_element_u == cfg.tv_sym_pwr_p4_pos:
        return (0.0, cfg.tv_sym_pwr_p4_pos)
    elif lone_element_u == cfg.tv_sym_pwr_p4_neg:
        return (0.0, cfg.tv_sym_pwr_p4_neg)

    elif lone_element_u == cfg.tv_sym_pwr_m2_pos:
        return (0.0, cfg.tv_sym_pwr_m2_pos)
    elif lone_element_u == cfg.tv_sym_pwr_m2_neg:
        return (0.0, cfg.tv_sym_pwr_m2_neg)

    elif lone_element_u == cfg.tv_sym_pwr_m3_pos:
        return (0.0, cfg.tv_sym_pwr_m3_pos)
    elif lone_element_u == cfg.tv_sym_pwr_m3_neg:
        return (0.0, cfg.tv_sym_pwr_m3_neg)

    elif lone_element_u == cfg.real_num_sym_pos:
        return (cfg.real_num_sym_pos, cfg.null_sym)
    elif lone_element_u == cfg.real_num_sym_neg:
        return (cfg.real_num_sym_neg, cfg.null_sym)

    elif lone_element_u == cfg.real_num_sym:
        return (cfg.real_num_sym, cfg.null_sym)

    elif lone_element_u == cfg.null_sym:
        return (0.0, cfg.null_sym)

    elif lone_element_u == cfg.unimplemented_sym:
        return cfg.unimplemented_sym


def format_result_for_display(
    result_unformatted
    ):
    """
    Formats calculated transvalent tuples of the type "(0.0, Ƿ)" as
    output in the form of "Ƿ", for display. Passes conventional
    text strings (e.g., intro or help text) without alteration.
    """

    if cfg.debugging_mode is True:
        print("result_unformatted: ", result_unformatted)
        print("result_unformatted type: ", type(result_unformatted))


    # ------------------------------------------------------------------
    # Format various types of unformatted results.
    # ------------------------------------------------------------------

    # If the result is a lone real number...
    if isinstance(result_unformatted, float):
        result_formatted = str(result_unformatted)

    # If the result couldn't be calculated...
    elif result_unformatted == cfg.unimplemented_sym:
        result_formatted = \
            "The requested calculation involves operations or\n" \
            + cfg.output_spacer \
            + "values not yet implemented in the Liniarote CLI."

    # If the result is a string (e.g., a lone transvalent symbol or
    # a string with the intro or help text)...
    elif isinstance(result_unformatted, str):
        result_formatted = result_unformatted

    # If the result is a well-formed tuple...
    elif isinstance(result_unformatted, tuple):

        # If the first (real) value is a string (e.g., "Æ", "-Æ", or "ℝ"),
        # display it if the second (transvalent) value is the Null
        # transvalent symbol.
        if isinstance(result_unformatted[0], str):
            if result_unformatted[1] == cfg.null_sym:
                result_formatted = result_unformatted[0]

        # If the first (real) value is 0, display the second (transvalent) 
        # value, as long as its not the Null transvalent symbol. If the 
        # second value is the Null transvalent symbol, display 0.
        if result_unformatted[0] == 0:
            if result_unformatted[1] != cfg.null_sym:
                result_formatted = result_unformatted[1]
            else:
                result_formatted = str(0.0)

        # If the first (real) value is not 0 and the second value is the Null
        # transvalent symbol, display the first (real) value.
        elif (isinstance(result_unformatted[0], float) and result_unformatted[0] !=0) \
                and (result_unformatted[1] == cfg.null_sym):
            result_formatted = str(result_unformatted[0])

    # For any other (unanticipated) cases:
    else:
        result_formatted = result_unformatted

    return result_formatted


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define functions for displaying pre-prepared text blocks.
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def print_intro_text():
    """
    Displays the standard introductory text block used when launching the CLI.
    """
    print(cfg.intro_text)


def print_help_text():
    """
    Displays a detailed help file when requested by the user.
    """

    print(cfg.help_text)
    return "('Help' contents displayed above. Returning to command prompt.)"


# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■
# █ Define the overall logic for executing the module.
# ■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■■

def handler(signum, frame):
    """
    Allows the user the option of cleanly exiting the program when 
    input of "Ctrl+C" has been detected.
    """

    # Ask for confirmation that the user wishes to exit the program.
    pre_exit_message = \
        "Quit Liniarote? Please press 'y' to exit this program."
    print(pre_exit_message, end="", flush=True)
    user_response = readchar.readchar()

    # Exit if either "Y" or "y" is inputted as the user's response.
    if user_response.lower() == "y":
        print("\n" + cfg.output_spacer + "Thank you for using Liniarote!\n")
        exit(1)
    else:
        print("", end="\r", flush=True)


if __name__ == '__main__':

    # A general error message will be printed if (e.g.)
    # the intro text cannot be displayed.
    try:

        # Display the intro text.
        print_intro_text()

        # Create the main lexer.
        lexer = LiniaroteLexer()

        # Check for user input of "Ctrl+C".
        signal.signal(signal.SIGINT, handler)

        while True:

            # Display the command prompt that accepts user input.
            text = input("<LINIAROTE:>  ")

            #try:
            if cfg.debugging_mode is True:
                tokens_for_display = lexer.tokenize(text)
                for token in tokens_for_display:
                    print('token type: ', token.type, "; token value: ", token.value)

            # Process the user's input.
            tokens = lexer.tokenize(text)
            parser = LiniaroteParser()
            result = parser.parse(tokens)

            # Format the calculated output for display and display it
            # on a special "output" line.
            result = format_result_for_display(result)
            print("    output =  " + result)

            #except:
            #    result = ("A problem occurred during processing. Please try reformulating your input.")
            #    print("    output =  " + result)

            # After calculated output has been displayed, wait
            # before providing a new (blank) command prompt to
            # receive new input from the user.
            time.sleep(0.4)

    except:
        print("A problem has occurred with the Liniarote CLI. We apologize!")


# ••••-••••-••••-••••-••••-••••-••••--••••-••••-••••-••••-••••-••••-••••