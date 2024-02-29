# key-drag
## _Automate applying keys to the Liber Primus_

Methods to apply a key to cipher text and look for viable plaintext. 
Currently decryption functions of two variables are supported (e.g. ciphertext = plaintext + key, ciphertext = plaintext * key ).

 - pure python version (src_py) (mostly for demonstration as it is slow)
 - cython version  using compiled binaries generated with cython. (src_cython) 


## Installation 

For cython version you may need to install cython and numpy. To compile binaries a c/c++ compiler is required. 
The cython binaries can be compiled by running, from src_cython directory, something like:
"python setup.py build_ext --inplace"


## Example Scripts / Tests  

 - solve_solved_pages.py Reproduce solutions to the 3 solved sections that require a key  
 - py_test_own_text.py and cy_test_own_text.py Generate a "random" ciphertext and then try and solve it. These should _never_ fail. If they do you may have found a bug.  
 - solve_5455 An example script applying the prime sequence key, with all options to 54/55.jpg of LP 

## Main Files & Classes

- gematria Simple gematria class for converting between runes and index etc. 
- ngram_model Language model based on https://github.com/mortlach/runeglish-language-model-transition-probabilty-matrices (Python and Cython version). Used to Score plaintext results. 
- word_model. Language Model based on pre-defined word-lists. (taken from a version of this https://github.com/mortlach/Liber-Primus-Crib-Assist Used to calculate Hamming distance of plaintext results
- setup.py compilation instructions for cython 
- numerical_methods.pyx numerical functions 
- key_drag applies keys with _all_ combinations of options to each possible ciphertext 
- cryption_methods_of_2_variables ALl encryption / decryption methods are given here. These methods can easily be extended by adding your own, either by defining your own functions or lookup tables  

## Development

I'm mostly confident on accuracy so the main development plan is to improve speed and general status of the code.
Main next planned extension is to include functions af 3 variables, (e.g. ciphertext[i] = plaintext[i] * key[i] + ciphertext[i-1] 
Want to contribute? Great! Meet  me at the cicadasolvers discord.  

## HELP

cicadasolvers discord.  

