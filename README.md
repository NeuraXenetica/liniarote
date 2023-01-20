# LINIAROTE: The programming language for transvalent mathematics

The Liniarote package is a Python implementation of a command-line interface for the Liniarote programming language, an open-source language developed to facilitate operations in transvalent mathematics.

The software is developed by Matthew E. Gladden (with support from Cognitive Firewall LLC and NeuraXenetica LLC) and is made available for use under GNU General Public License Version 3. Please see https://www.gnu.org/licenses/gpl-3.0.html.

___
## AN OVERVIEW OF TRANSVALENT MATHEMATICS

The distinguishing characteristic of transvalent mathematics is that division by zero is permitted and generates results calculated according to certain clearly defined principles.

The symbol “Ƿ” is used to represent that (transvalent) number which when multiplied by 0 can equal any positive real number. An equivalent way of defining Ƿ is to state that it is the quotient generated when any positive real number is divided by 0. Informally, one can think of the number Ƿ as a special type of “infinity” that possesses such transcendent power that when 0 is multiplied by it, Ƿ is capable of “lifting” zero out of nothingness to give their product a positive real value. Similarly, the symbol “-Ƿ” is used to represent that (transvalent) number which when multiplied by 0 yields a result that can take the value of any of negative real number; alternatively, -Ƿ can be defined as the quotient generated when any real number is divided by 0. (Meanwhile, 0 divided by 0 yields a result that can take the form of any real number.) Within transvalent mathematics, the number Ƿ is described as “imperishable,” because there is no real number that one can multiply it by in order to yield 0. (Similarly, there is no real number by which -Ƿ can be multiplied to yield 0.)

Also important in transvalent mathematics is the symbol “Æ”, which represents a number whose current value is able to take the form of any positive real number, with “-Æ” representing a number whose current value is able to take the form of any negative real number. Similarly, “ℝ” is used here not to represent the set of all real numbers but to represents a number whose current value is able to take the form of any particular real number.

Intuitively, it is easy to suppose that attempts at dividing by zero must necessarily yield a result that is “undefined,” “meaningless,” or “absurd” and that calculations that attempt to divide by zero are inherently “erroneous.” From a theoretical perspective, though, statements like “Ƿ = 3 ÷ 0” and “Ƿ × 0 = 5” are no more intrinsically absurd than (for example) the definitions that “i = √(-1)” and “i² = -1”, which are foundations of the imaginary and complex number systems – and which have facilitated countless theoretical and practical advances in diverse scientific and technological spheres. The establishment of systems like that of transvalent mathematics simply require clear formulations of the meaning of “dividing by zero” and rules for interpreting the results that are generated. Frameworks with similarities to transvalent mathematics (e.g., in granting some formal meaning to division by zero) that have been developed in the last 200 years include those of the Riemann sphere (which extends the complex plane by adding a point at infinity) and the projectively extended real line.

While transvalent mathematics is able to define division by zero and handle it in a consistent and predictable manner, it does so at the cost of eliminating certain properties employed in more conventional mathematics (e.g., the properties of associativity and commutativity for certain binary operations). For example, in conventional mathematics, it is the case that (a + b) + c = a + (b + c). However, in transvalent mathematics, (Ƿ + Ƿ) + -Ƿ = (Ƿ) + -Ƿ = 0, while Ƿ + (Ƿ + -Ƿ) = Ƿ + (0) = Ƿ.

___
## SELECTED AXIOMS OF TRANSVALENT MATHEMATICS

Axioms of addition and subtraction:

`Ƿ + n = Ƿ, where n is any real number`\
`-Ƿ + n = -Ƿ, where n is any real number`\
`Ƿ - Æ = Ƿ`\
`Ƿ + Æ = Ƿ`\
`Ƿ² + n = Ƿ², where n is any real number`\
`Ƿ² + Ƿ = Ƿ²`\
`-Ƿ² + Ƿ = -Ƿ²`\
`Ƿ + Ƿ = Ƿ`\
`-Ƿ - Ƿ = -Ƿ`\
`Ƿ - Ƿ = 0`

Axioms of non-associativity:

`(Ƿ + Ƿ) + -Ƿ = (Ƿ) + -Ƿ = 0`\
`Ƿ + (Ƿ + -Ƿ) = Ƿ + (0) = Ƿ`

Axioms of multiplication:

`Ƿ × n = Ƿ, where n is any positive real number`\
`Ƿ × n = -Ƿ, where n is any negative real number`\
`-Ƿ × n = -Ƿ, where n is any positive real number`\
`-Ƿ × n = Ƿ, where n is any negative real number`\
`Ƿ × Ƿ = Ƿ²`\
`Ƿ × -Ƿ = -Ƿ²`\
`Ƿ × 0 = Æ`\
`-Ƿ × 0 = -Æ`

Axioms of division:

`n ÷ 0 = Ƿ, where n is any positive real number`\
`n ÷ 0 = -Ƿ, where n is any negative real number`\
`0 ÷ 0 = ℝ`\
`Ƿ ÷ 0 = Ƿ²`\
`-Ƿ ÷ 0 = -Ƿ²`\
`Ƿ ÷ n = Ƿ, where n is any positive real number`\
`Ƿ ÷ n = -Ƿ, where n is any negative real number`\
`-Ƿ ÷ n = -Ƿ, where n is any positive real number`\
`-Ƿ ÷ n = Ƿ, where n is any negative real number`\
`n ÷ Ƿ = 0, where n is any non-zero real number`\
`n ÷ -Ƿ = 0, where n is any non-zero real number`\
`0 ÷ Ƿ = Ƿ⁻²`\
`0 ÷ -Ƿ = -Ƿ⁻²`\
`Ƿ ÷ Ƿ = Æ`\
`-Ƿ ÷ Ƿ = -Æ`\
`-Ƿ ÷ -Ƿ = Æ`\
`Ƿ ÷ -Ƿ = -Æ`\
`Ƿ ÷ Ƿ² = 0`\
`Ƿ ÷ -Ƿ² = 0`\
`Ƿ² ÷ 0 = Ƿ³`\
`Ƿ² ÷ Ƿ = Ƿ`\
`Ƿ² ÷ n = Ƿ², where n is any positive real number`\
`Ƿ² ÷ n = -Ƿ², where n is any negative real number`\
`Ƿ² ÷ Ƿ² = Æ`

___
## PACKAGE EXECUTION AND INPUT FORMAT

The manner of activating the Liniarote command-line interface will depend on one's operating system and Python installation. In Windows, for example, one may be able to run the command-line interface module (cli.py) by typing the following lines at the PowerShell prompt or Visual Studio Code terminal prompt from within the appropriate folder:

`python -m pip install liniarote`\
`python -m liniarote.cli`

On the Liniarote command line, the symbol “Ƿ” (Unicode: U+01F7; UTF-8: C7 B7) can be inputted by typing the lowercase letter “w”, which will be automatically converted into “Ƿ” during processing of the input. (Similarly, “-w” will be converted into “-Ƿ”.) Built-in constants recognized by Liniarote include “e” and “pi”. The operators currently available for use are:

`+ - * / ( )`

It’s possible to assign a value to a user-created alphabetical constant (beyond “pi” and “e”) for use in multiple calculations. This can be done by typing the constant’s name at the command prompt; Liniarote will then ask for the constant’s value to be inputted. For example:

`<LINIAROTE:>  m`\
`Please enter the desired value for m: 5.7`

At the moment, the CLI is capable of processing only simple requested calculations, inputted in a form like:

`<LINIAROTE:>  37/54`\
`<LINIAROTE:>  3+w*4`\
`<LINIAROTE:>  (14.3 + w)*(3.1 + w)`\
`<LINIAROTE:>  (3-w)*(5-w)`\
`<LINIAROTE:>  (9.2 + w) / (41.7 + w)`\
`<LINIAROTE:>  w / 5.3 / w`\
`<LINIAROTE:>  12.5*w*w`\
`<LINIAROTE:>  (3+w) - (w-5) + (2-w) - (12+w)`\
`<LINIAROTE:>  (w*4.5) - (w-25) - (w/32) + (pi+w)`\
`<LINIAROTE:>  pi*w`\
`<LINIAROTE:>  (e+w)/(pi+1)`\
`<LINIAROTE:>  w+8*C`\

An error message will be generated if an inputted calculations requires the use of operations or values not currently implemented in the Liniarote CLI.

___
## REQUIREMENTS

Please see the “requirements.txt” file for a list of other Python packages whose installation is a prerequisite for the proper functioning of Liniarote.

___
## INSPIRATION AND ACKNOWLEDGMENTS

Within the world of the “Utopian Confederation” RPG series, the foundational text in the field of transvalent mathematics as such was published by a team of Utopian mathematicians in 1911. In honor of their work, the Liniarote programming language was named after one of the 54 cities of the ancient Utopian Commonwealth, as described in Thomas More’s “Utopia” (1516). The Liniarote programming language was created by Matthew E. Gladden, who also developed and maintains the Liniarote CLI.

Liniarote code and documentation ©2022-2023 Cognitive Firewall LLC
