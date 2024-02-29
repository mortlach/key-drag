'''
generate sa "random" test encryption to try adn solve
all data save inm dict

'''
import time
import random
import src_cython.gematria as gem
import src_cython.cryption_methods_of_2_variables as cry

# list of test words to generate a key
test_key_words = [[1, 3, 10, 5, 18], [3, 2, 18, 4, 15], [24, 0, 16, 18, 4], [24, 6, 24, 10, 9], [24, 9, 26, 2, 21],
                  [24, 15, 5, 18, 23], [24, 17, 3, 1, 16], [24, 19, 24, 15, 15], [4, 10, 6, 8, 16], [4, 28, 15, 3, 9],
                  [5, 3, 1, 20, 23], [5, 24, 1, 15, 18], [5, 8, 24, 21, 18], [6, 18, 16, 16, 21], [7, 3, 4, 23, 15],
                  [7, 24, 4, 9, 21], [7, 8, 10, 5, 8], [7, 10, 2, 10, 9], [8, 1, 19, 24, 9], [9, 18, 1, 18, 4],
                  [13, 24, 1, 15, 18], [15, 8, 24, 13, 18], [15, 16, 1, 23, 26], [15, 16, 4, 3, 21],
                  [17, 18, 20, 3, 21],
                  [18, 1, 18, 4, 26], [18, 10, 2, 18, 4], [20, 24, 16, 18, 4], [20, 10, 1, 18, 15], [23, 3, 6, 19, 24],
                  [0, 3, 20, 20, 3, 7], [2, 3, 1, 6, 8, 16], [2, 4, 3, 1, 6, 8], [3, 17, 16, 24, 10, 9],
                  [24, 4, 4, 10, 1, 18], [4, 24, 10, 15, 18, 23], [4, 28, 20, 10, 16, 26], [5, 24, 20, 20, 18, 23],
                  [7, 10, 15, 8, 18, 15], [7, 10, 15, 23, 3, 19], [7, 10, 23, 15, 3, 19], [8, 24, 15, 8, 18, 15],
                  [10, 9, 15, 10, 23, 18], [10, 9, 15, 16, 24, 4], [10, 19, 13, 3, 15, 18], [13, 4, 10, 19, 18, 15],
                  [15, 24, 5, 4, 18, 23], [15, 8, 3, 1, 20, 23], [16, 3, 7, 24, 4, 23], [17, 18, 5, 3, 19, 18],
                  [18, 4, 4, 3, 4, 15], [18, 9, 3, 1, 6, 8], [18, 14, 5, 18, 13, 16], [18, 14, 10, 15, 16, 15],
                  [18, 19, 18, 4, 6, 18], [19, 3, 19, 18, 9, 16], [19, 24, 15, 16, 18, 4], [19, 18, 4, 18, 20, 26],
                  [20, 18, 15, 15, 3, 9], [0, 1, 9, 5, 16, 27, 9], [0, 3, 20, 20, 3, 7, 21], [0, 10, 9, 24, 20, 20, 26],
                  [3, 1, 16, 15, 10, 23, 18], [4, 18, 13, 20, 10, 18, 23], [5, 3, 9, 15, 1, 19, 18],
                  [5, 3, 9, 15, 1, 19, 21], [5, 3, 19, 19, 24, 9, 23], [5, 7, 18, 15, 16, 27, 9],
                  [7, 18, 20, 5, 3, 19, 18], [9, 1, 19, 17, 18, 4,
                                              15], [11, 3, 1, 4, 9, 18, 26], [13, 24, 4, 24, 17, 20, 18], [13, 4,
                                                                                                           3, 6, 4, 24,
                                                                                                           19],
                  [13, 10, 20, 6, 4, 10, 19], [15, 1, 0, 0, 18, 4,
                                               21], [15, 1, 4, 0, 24, 5, 18], [15, 13, 18, 5, 10, 18, 15], [15, 16,
                                                                                                            1, 23, 18,
                                                                                                            9, 16],
                  [15, 16, 3, 13, 13, 18, 23], [15, 16, 24, 4, 16, 18, 23], [16, 1, 9, 9, 18, 20, 21],
                  [16, 3, 16, 10, 18, 9, 16],
                  [16, 4, 24, 10, 20, 18, 23],
                  [17, 18, 5, 24, 1, 15, 18], [17, 18, 20, 10, 18, 1, 18], [18, 14, 13, 20, 24, 10, 9],
                  [19, 18, 15, 15, 24, 6, 18],
                  [23, 18, 5, 10, 23, 18, 23], [23, 18, 15, 16, 4, 3, 26], [26, 3, 1, 4, 15, 18, 20, 0],
                  [24, 9, 15, 7, 18, 4, 18, 23], [24, 16, 16, 24, 5, 8, 18, 23], [4, 28, 20, 10, 16, 10, 18, 15],
                  [5, 3, 9, 0, 1, 15, 18, 23],
                  [10, 9, 8, 24, 17, 10, 16, 21], [10, 20, 20, 1, 15, 27, 9, 15],
                  [13, 4, 18, 13, 24, 4, 18, 23], [13, 4, 18, 15, 18, 4, 1, 18], [13,
                                                                                  4, 18, 15, 18, 4, 1, 21],
                  [15, 16, 1, 23, 18, 9, 16, 15], [15, 16, 4,
                                                   1, 6, 6, 20, 18], [17, 18, 8, 24, 1, 27, 4, 15], [23, 10, 1, 10, 9,
                                                                                                     10, 16, 26],
                  [23, 10, 15, 5, 3, 1, 18, 4], [23, 18, 5, 18, 13, 16,
                                                 27, 9], [3, 1, 4, 15, 18, 20, 1, 18, 15], [24, 4, 17, 10, 16, 4, 24,
                                                                                            4, 26],
                  [24, 23, 8, 18, 4, 18, 9, 5, 18], [5, 3, 9, 16, 24, 10, 9,
                                                     18, 23], [5, 9, 3, 7, 20, 18, 23, 6, 18], [5, 18, 4, 16, 24, 10, 9,
                                                                                                16, 26],
                  [9, 18, 5, 18, 15, 15, 24, 4, 26], [10, 4, 4, 10, 16, 24,
                                                      16, 18, 23], [10, 9, 9, 3, 5, 18, 9, 5, 18], [13, 4, 3, 0, 18, 15,
                                                                                                    15, 3, 4],
                  [13, 4, 24, 5, 16, 10, 5, 18, 15], [13, 4, 10, 19, 24, 20,
                                                      10, 16, 26], [18, 9, 5, 4, 26, 13, 16, 18, 23],
                  [18, 14, 13, 20, 24,
                   10, 9, 18, 23], [1, 20, 16, 10, 19, 24, 16, 18, 20, 26], [5, 3, 9,
                                                                             15, 1, 19, 13, 16, 27, 9],
                  [10, 9, 15, 16, 4, 1, 5, 16, 27, 9], [13,
                                                        10, 20, 6, 4, 10, 19, 24, 6, 18],
                  [18, 14, 13, 18, 4, 10, 18, 9, 5, 18], [1, 9, 4, 28, 15, 3, 9, 24, 17, 20, 18],
                  [13, 4, 18, 15, 18, 4, 1, 24, 16, 27, 9],
                  [18, 9, 20, 10, 6, 8, 16, 18, 9, 18, 23], [5, 3, 9, 15, 5, 27, 1, 15, 9, 18, 15, 15],
                  [10, 9, 16, 18, 20, 20, 10, 6, 18, 9, 5, 18], [5, 10, 4, 5, 1, 19, 0, 18, 4, 18, 9, 5, 18],
                  [5, 10, 4, 5, 1, 19, 0, 18, 4, 18, 9, 5, 18, 15]]


def get_keywords_by_min_length(min_length):
    return [x for x in test_key_words if len(x) >= min_length]


def get_keywords_by_length(length):
    return [x for x in test_key_words if len(x) == length]


def get_random_keyword(min_len, max_len):
    return random.choice([x for x in test_key_words if (len(x) >= min_len) and (len(x) <= max_len)])


def get_test_encryption(pt_rune_string):
    ''' generates a test encryption data saved to test_data '''
    test_data = {}
    test_data['p_latin_string'] = pt_rune_string
    test_data['p_runes_string'] = gem.translate_to_gematria(test_data['p_latin_string'])
    test_data['p_runewords_string'] = test_data['p_runes_string'].split()
    test_data['p_index'] = [gem.rune2position(x) for x in list(test_data['p_runes_string']) if x != ' ']
    # this odditiy is used to check if we get a valid plaintext
    test_data['p_index_str'] = ''.join(str(i) for i in test_data['p_index'])
    test_data['p_latin'] = [gem.rune2latincanon(x) for x in list(test_data['p_runes_string']) if x != ' ']
    test_data['p_runes'] = [x for x in list(test_data['p_runes_string']) if x != ' ']
    test_data['wli'] = []
    [[test_data['wli'].append([i, len(word)]) for i, x in enumerate(word)] for word in
     test_data['p_runewords_string']]

    # set cipher options
    possible_interrupters = [None, 0, 5, 6, 7, 8, 11, 12, 13, 14, 17, 19, 20, 21, 22, 23, 25, 26, 27, 28]
    u = set.intersection(set(possible_interrupters), set(test_data['p_index']))
    # Encryption Options
    test_data["interrupter"] = random.choice(list(u) + [None])
    test_data["interrupter_latin"] = gem.position2latincanon(test_data["interrupter"])
    test_data["k_gematria_shift"] = random.choice(range(29))
    test_data["p_gematria_shift"] = random.choice(range(29))
    test_data["enc_function"] = random.choice([cry.encrypt_p_plus_k,
                                               cry.encrypt_p_minus_k,
                                               cry.encrypt_k_minus_p,
                                               cry.encrypt_p_multiply_k,
                                               cry.encrypt_p_divide_k,
                                               cry.encrypt_k_divide_p,
                                               cry.encrypt_k_xor_p,
                                               cry.encrypt_p_xor_k
                                               ])
    test_data["p_gematria_direction"] = random.choice(['normal', 'atbash'])
    test_data["k_gematria_direction"] = random.choice(['normal', 'atbash'])
    test_data["transposition"] = random.choice(['L2R', 'R2L'])
    # test_data["enc_function"] = cry.encrypt_p_plus_k
    # test_data["p_gematria_direction"] = 'normal'
    # test_data["k_gematria_direction"] = 'normal'
    # test_data["transposition"] = 'L2R'
    # test_data["k_gematria_shift"] = 0
    # test_data["p_gematria_shift"] = 0

    #
    # ENCRYPTION
    #
    # first remove interrupters
    test_data['interrupter_index'] = [i for i, p in enumerate(test_data['p_index']) if p == test_data['interrupter']]
    test_data['interrupted_p_index'] = [p for i, p in enumerate(test_data['p_index']) if
                                        i not in test_data['interrupter_index']]
    #
    # NEXT  apply transposition to plaintext
    test_data['transposition_indices'] = cry.get_transposition_indices(len(test_data['interrupted_p_index']),
                                                                       test_data['transposition'])
    test_data['transposed_interrupted_p_index'] = [test_data['interrupted_p_index'][i] for i in
                                                   test_data['transposition_indices']]
    #
    # Get key parameters
    test_data['k_raw'] = random.choices(range(29), k=len(test_data['transposed_interrupted_p_index']))

    # a word a sa key
    test_data['key_word'] = get_random_keyword(10, 14)
    # the prim esequenc eas key
    test_data['key_word'] = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]

    test_data['key_word_start_index'] = random.choice(
        range(0, len(test_data['k_raw']) - len(test_data['key_word']) - 1))
    # test_data['key_word_start_index'] = 0
    for i, p in enumerate(test_data['key_word']):
        test_data['k_raw'][test_data['key_word_start_index'] + i] = test_data['key_word'][i]
    #
    # rotate the plaintext / key
    test_data['p_to_encrypt'] = cry.get_gematria_rotation(test_data['transposed_interrupted_p_index'],
                                                          test_data['p_gematria_shift'],
                                                          test_data['p_gematria_direction'])
    test_data['k_to_encrypt'] = cry.get_gematria_rotation(test_data['k_raw'], test_data['k_gematria_shift'],
                                                          test_data['k_gematria_direction'])
    #
    # apply encryption function
    test_data['c_raw'] = test_data['enc_function'](test_data['p_to_encrypt'], test_data['k_to_encrypt'])
    #
    # un-transpose
    test_data['c_raw_untranspose'] = [test_data['c_raw'][i] for i in test_data['transposition_indices']]
    #
    # re-insert interrupters
    test_data['c_raw_untranspose_add_interrupters'] = list(test_data['c_raw_untranspose'])
    for i in test_data['interrupter_index']:
        test_data['c_raw_untranspose_add_interrupters'].insert(i, test_data['interrupter'])
    #
    # final cipher text lists
    test_data['c_index'] = test_data['c_raw_untranspose_add_interrupters']
    test_data['c_latin'] = [gem.position2latincanon(x) for x in test_data['c_index']]
    test_data['c_rune'] = [gem.position2rune(x) for x in test_data['c_index']]

    assert len(test_data['c_rune']) == len(test_data['p_index'])

    # Decryption Attempts, need Cipher Text With word length info  and Key_guesses
    decrypt_data = {}
    decrypt_data['decrypt_functions'] = [cry.encrypt_to_decrypt[test_data['enc_function']]]
    decrypt_data['c_and_k_directions'], decrypt_data['c_and_k_rotations'] = cry.get_gematria_options_for_method(
        decrypt_data["decrypt_functions"][0])
    decrypt_data['interrupters'] = list({None, test_data['interrupter']})
    decrypt_data['transpositions'] = [test_data['transposition']]
    # decrypt_data['c_and_k_directions'] = [["normal", 'atbash'], ["normal", 'normal']]
    decrypt_data['c_index'] = test_data['c_index']
    decrypt_data['wli'] = test_data['wli']
    decrypt_data['key_guess'] = test_data['key_word']
    return [test_data, decrypt_data]
