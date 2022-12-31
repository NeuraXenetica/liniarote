# LINIAROTE: A programming language for transvalent mathematics

The Liniarote package is a Python implementation of a command-line interface
for the Liniarote programming language, an open-source programming language 
developed specifically to facilitate operations in transvalent mathematics.

The software is developed by Matthew E. Gladden (with support from Cognitive Firewall LLC and NeuraXenetica LLC) and is made available for use under GNU General Public License Version 3. Please see https://www.gnu.org/licenses/gpl-3.0.html.

___
## AN OVERVIEW OF TRANSVALENT MATHEMATICS

The distinguishing characteristic of transvalent mathematics is that division 
by zero is permitted and generates results calculated according to certain 
clearly defined principles.

The symbol “Ƿ” is used to represent that (transvalent) number which when 
multiplied by 0 yields a result of 1. An equivalent way of defining Ƿ is to 
state that it is the quotient generated when 1 is divided by 0.

Informally, one can think of the number Ƿ as a special type of “infinity” 
that possesses such transcendent power that when 0 is multiplied by it, Ƿ is 
capable of “lifting” zero out of nothingness to give their product a positive 
value (i.e., 1). Similarly, the symbol “-Ƿ” is used to represent that 
(transvalent) number which when multiplied by 0 yields a result of -1; 
alternatively, -Ƿ can be defined as the quotient generated when -1 is divided 
by 0.

The number Ƿ is described as “imperishable,” because there is no real number 
that one can multiply it by in order to yield 0. (Similarly, there is no real 
number by which -Ƿ can be multiplied to yield 0.)

Intuitively, it is easy to suppose that attempts at dividing by zero must 
necessarily yield a result that is “undefined,” “meaningless,” or “absurd” 
and that calculations that attempt to divide by zero are inherently 
“erroneous.” From a theoretical perspective, though, the definitions that 
“Ƿ = 1 ÷ 0” and “Ƿ × 0 = 1” are no more intrinsically absurd than (for 
example) the definitions that “i = √(-1)” and “i² = -1”, which are 
foundations of the imaginary and complex number systems – and which have 
would facilitate countless theoretical and practical advances in diverse 
scientific and technological spheres. The establishment of systems like that 
found in transvalent mathematics simply required clear formulations of the 
meaning of “dividing by zero” and rules for interpreting the results that are
generated. Frameworks with similarities to transvalent mathematics (e.g., 
in granting some formal meaning to division by zero) that have been developed 
in the last 200 years include those of the Riemann sphere (which extends the 
complex plane by adding a point at infinity) and the projectively extended 
real line.

___
## KEY AXIOMS OF TRANSVALENT MATHEMATICS

Axioms of identity and grouping:

`Ƿ = 0 + Ƿ`
`-Ƿ = 0 - Ƿ`
`n = n + (Ƿ - Ƿ), where n is any real number`

Axioms of non-associativity:

(Ƿ + Ƿ) - Ƿ = 0
(Ƿ + (Ƿ - Ƿ) = Ƿ

Axioms of addition and subtraction:

Ƿ + Ƿ = Ƿ
-Ƿ - Ƿ = -Ƿ
Ƿ - Ƿ = 0
-Ƿ + Ƿ = 0

Axioms of multiplication and division:

Ƿ × 0 = 1
-Ƿ × 0 = -1

Ƿ × n = Ƿ, where n is any positive real number
Ƿ × n = -Ƿ, where n is any negative real number
-Ƿ × n = -Ƿ, where n is any positive real number
-Ƿ × n = Ƿ, where n is any negative real number
Ƿ × n ≠ 0, where n is any real number
-Ƿ × n ≠ 0, where n is any real number

n / 0 = (n – 1) + Ƿ, where n is any positive real number
n / 0 = (n + 1) - Ƿ, where n is any negative real number

Ƿ × Ƿ = Ƿ
-Ƿ × Ƿ = -Ƿ
-Ƿ × -Ƿ = Ƿ

Ƿ ÷ 0 = Ƿ
-Ƿ ÷ 0 = -Ƿ
Ƿ ÷ Ƿ = 1
-Ƿ ÷ Ƿ = -1

___
## SAMPLE CALCULATIONS


Ƿ   --->   0 + Ƿ
-Ƿ   --->   0 - Ƿ
4.72   --->   4.72 + (Ƿ - Ƿ)

Ƿ - 9.31   --->   -9.31 + Ƿ
Ƿ + Ƿ + Ƿ   --->   0 + Ƿ
Ƿ + Ƿ – Ƿ   --->   0 + Ƿ
Ƿ - Ƿ – Ƿ   --->   0 - Ƿ
Ƿ - Ƿ + Ƿ - Ƿ   --->   0 + (Ƿ - Ƿ)
Ƿ + Ƿ + 51.2 + Ƿ   --->   51.2 + Ƿ

Ƿ × 0   --->   1 + (Ƿ - Ƿ)
-Ƿ × 0   --->   -1 + (Ƿ - Ƿ)
Ƿ × 5.2   --->   0 + Ƿ
Ƿ × -3.7   --->   0 - Ƿ
-Ƿ × 7.4   --->   0 - Ƿ
-Ƿ × -8.9   --->   0 + Ƿ
1 / 0   --->   0 + Ƿ
-1 / 0   --->   0 - Ƿ
3.4 / 0   --->   2.4 + Ƿ
-5.8 / 0   --->   -4.8 - Ƿ
5.3 ÷ 0   --->   4.3 + Ƿ
-17.2 ÷ 0   --->   -16.2 - Ƿ

In the case of an equation like “5.3 ÷ 0”, the transvalent number Ƿ does the 
“impossible” work of uplifting 0 from 0 to 1: the (much easier) remainder of 
the work is then performed by Ƿ’s “assistants,” in the form of real numbers 
that increase the value from 1 to that of the number that was divided by 0. 
In that case, the relevant real number is 4.3, which increases 1 to a 
targeted sum of 5.3.

___
## INPUT FORMAT

On the Liniarote command line, the symbol “Ƿ” (Unicode: U+01F7; UTF-8: C7 B7) 
can be inputted by typing the lowercase letter “w”, which will be 
automatically converted into “Ƿ” during processing of the input. (Similarly, 
“-w” will be converted into “-Ƿ”.)

The order of entry of the real and transvalent components of a number is 
without significance. Thus, both “3 + w” and “w + 3” will, when inputted, be 
converted into “3 + Ƿ”, while “-5 + w” and “-w – 5” and will be converted 
into “-5 – Ƿ”.

Inputted constants recognized by Liniarote include “e” and “pi”.

Division is not yet implemented. The operators currently available for use 
are: + - * ( )

___
## REQUIREMENTS

Please see the “requirements.txt” file for a list of other Python packages 
whose installation is a prerequisite for the proper functioning of Liniarote.

___
## INSPIRATION AND ACKNOWLEDGMENTS

Within the world of the “Utopian Confederation” RPG series, the foundational 
text in the field of transvalent mathematics as such was published by a team 
of Utopian mathematicians in 1911. In honor of their work, the Liniarote 
programming language was named after one of the 54 cities of the ancient 
Utopian Commonwealth, as described in ThomasMore’s “Utopia” (1516). Liniarote 
was created and is maintained by Matthew E. Gladden.

Liniarote code and documentation ©2022-23 Cognitive Firewall LLC

