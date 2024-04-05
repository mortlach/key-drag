'''
TEST - using pure python libs
'''
import time
import random
import src_py.gematria as gem
import src_py.generate_test as gt
import src_py.cryption_methods_of_3_variables as cry3
import src_py.key_drag_3var as key_drag
import src_py.ngram_model as ngmod
import src_py.word_model as wmod
import time
import random
import numpy as np
from operator import itemgetter

tload1 = time.time()
lm1 = ngmod.NGramModel(True, False)
lm2 = wmod.WordModel(True)

def apply_key(decrypt_data, outputfile):
    # set up key-dragger
    kd = key_drag.KeyDrag()
    # what to do with errors? for now, exclude them (could treat as a form of interrupter, etc.)
    discard_errors = True
    [wlis, r] = kd.drag_key(ct=decrypt_data['c_index'],
                            key1=decrypt_data['key1_guess'],
                            key2=decrypt_data['key2_guess'],
                            wli=decrypt_data['wli'],
                            interrupters=decrypt_data['interrupters'],
                            transpositions=decrypt_data['transpositions'],
                            c_and_k_directions=decrypt_data['c_and_k_directions'],
                            c_and_k_rotations=decrypt_data['c_and_k_rotations'],
                            decrypt_functions=decrypt_data['decrypt_functions'],
                            discard_errors=discard_errors)
    hit_data = []
    hit_dict = {}
    total_attempts = 0
    tru_hits = 0
    for pt_key, these_opts in r.items():
        this_pt = pt_key[0]
        this_i = pt_key[1]
        wli_at_this_index = wlis[this_i]
        # interrupter
        interrupters = [topts[3] for topts in these_opts]
        int_pos = [i for i, p in enumerate(this_pt) if p == -1]
        #this_pt_allrot = nm.get_all_gematria_rotations_C(list(this_pt))
        this_pt_allrot = cry3.get_all_gematria_rotations(list(this_pt))
        # interrupters are never changed, so add back in
        for opts_counter, interrupt in enumerate(interrupters):
            opts_for_this_pt = these_opts[opts_counter]
            for part in int_pos:
                for a in this_pt_allrot:
                    a[part] = interrupt
            for rot_pt in this_pt_allrot:
                total_attempts += 1
                # two language test  tests, first on ngrams
                lm_threshold = -3
                result1 = False
                if all(lm1.are_w3w4_loaded()):
                    result1 = lm1.get_distance_from_mean_w3w4(rot_pt, wli_at_this_index)
                elif lm1.are_w3w4_loaded()[0]:
                    result1 = lm1.get_distance_from_mean_w3(rot_pt, wli_at_this_index)
                elif lm1.are_w3w4_loaded()[1]:
                    result1 = lm1.get_distance_from_mean_w4(rot_pt, wli_at_this_index)
                else:
                    input("ERROR CANT SCORE")

                result1 = lm1.get_distance_from_mean_w3(rot_pt, wli_at_this_index)
                all_neg = all([x > lm_threshold for x in result1])
                if all_neg:
                    # 2nd tets on word
                    result2 = lm2.find_min_HD(rot_pt, wli_at_this_index)
                    max_hd = 1
                    if result2 <= max_hd:
                        # a hit
                        this_pt_as_string = kd.get_as_runeglish_plaintext(this_pt=rot_pt, this_wli=wli_at_this_index)
                        if this_pt_as_string not in hit_dict:
                            datatosave = [decrypt_data['key1_guess'], this_pt_as_string, this_i, result1, sum(result1), opts_for_this_pt]
                            if datatosave not in hit_data:
                                hit_data.append(datatosave)
                                print(f'hit {datatosave}')
                                outputfile.write(f'{datatosave}\n')
                                outputfile.flush()
                            if this_pt_as_string not in hit_dict:
                                hit_dict[this_pt_as_string] = [datatosave]
                            else:
                                hit_dict[this_pt_as_string].append(datatosave)

    return sorted(hit_data, key=itemgetter(4), reverse=True), total_attempts, tru_hits, hit_dict


decrypt_data = {}
decrypt_data['c_runes_string'] = "ᚪ ᛗᛝᛞᛡᚦᛉᛁᛗ ᛡᛞᛈᛝᚢᚹᚪᛗ ᛏᚪᛝ ᛝᚦᛡᚹᛋᚻ ᛁᚳ ᚫᛈᚫᚷᚩ ᛗᛁᚪ ᛖᚩ ᛏᚹᚩ ᚠᚣᚢᛏᛂ ᚦᛂᛠᛖᚳᚾᛠ ᚳᛠᛖ \
                                    ᚱᚩᚢᛉ ᛞᚹᚻᛒᛝᚠᚪᚳᛂᚢ ᚩᛂᛡᛠᛁᛚᚷᚻ ᛒᚢᛂ ᛉᚪᚳᚹᛡ ᛗᚩᛈᚣᛞᛡᛚᛈ ᛇᛁᚦᚱ ᚣᚷᛗ ᛉᛟᚷᛋ ᛗᛈᛂᛟᛞ ᛟᛏᛡᛟ \
                                    ᛏᛝᛁ ᛗᛝᚣᚪᚫ ᛝ ᚱᚣᛂ ᚾᛚᚢᛉᛒ ᚻᛈᛂᚩᛠ ᚷᚫᚹ ᛉᛋᛞᚳ ᚢᛏ ᛟᚻᛇᚾᛈᛏ ᛠᚣᛒᚢᚷ ᚷᚪᛇ ᚾᚷᚩᛖᛚᛗᛒᚦ \
                                    ᚣᛡᛟᛇᚣ ᛗᚳᛟᚦ ᛖᛚᚱᛇᛈᚱᛞᚣ ᛉᛞ ᛝᚣᛈ ᛋᛖᛉᚹ ᚳᚷᚠᛞᚱᛖ ᛞᛖᚹᚩᛇᛟ ᚻᚩᛟ ᛒᛋ ᚻᛠᚪᚳᛁᛗᛉᛂᛗᛖ ᛗᛚ \
                                    ᚷᚩᛏᚦᛉᛖᛠᚱᚷᚣᛝ ᚫᛗᛁᚹ ᛋᛒ ᛉᛗ ᛋᛇᚷᛞᚦᚫ ᚠᛡᚪᛒᚳᚢ ᚹᚱ ᛒᛠᚠᛉᛁᛗᚢᚳᛈᚻᛝᛚᛇ ᛗᛋᛞᛡᛈᚠ ᛒᚻᛇᚳ ᛇᛖ \
                                    ᛠᛖᛁᚷᛉᚷᛋ ᛖᛋᛇᚦᚦᛖᛋ ᚦᛟ ᚳᛠᛁᛗᚳᛉ ᛞᛂᚢ ᛒᛖᛁ"
decrypt_data["c_runewords"] = decrypt_data['c_runes_string'].split()
decrypt_data['c_index'] = [gem.rune2position(x) for x in list(decrypt_data['c_runes_string']) if x != ' ']
# this odditiy is used to check if we get a valid plaintext
decrypt_data['c_index_str'] = ''.join(str(i) for i in decrypt_data['c_index'])
decrypt_data['c_latin'] = [gem.rune2latincanon(x) for x in list(decrypt_data['c_runes_string']) if x != ' ']
decrypt_data['c_runes'] = [x for x in list(decrypt_data['c_runes_string']) if x != ' ']
decrypt_data['wli'] = []
[[decrypt_data['wli'].append([i, len(word)]) for i, x in enumerate(word)] for word in
 decrypt_data['c_runewords']]

decrypt_data['key_guesses'] = [
    [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71],
    [1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597],
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144, 233, 377, 610, 987, 1597],
    [3301, 3299, 3271, 3257, 3229, 3191, 3119, 3001, 2819, 2579, 2131, 1459, 457],
    [24, 9, 18, 5, 18, 15, 15, 24, 4, 26], [24, 5, 3, 9, 15, 5, 27, 1, 15, 9, 18, 15, 15],
    [2, 18, 17, 18, 8, 24, 1, 27, 4, 15], [2, 18, 23, 18, 5, 18, 13, 16, 27, 9],
    [2, 18, 5, 10, 4, 5, 1, 19, 0, 18, 4, 18, 9, 5, 18], [3, 0, 23, 10, 1, 10, 9, 10, 16, 26],
    [3, 0, 5, 3, 9, 15, 1, 19, 13, 16, 27, 9], [8, 18, 24, 9, 15, 7, 18, 4, 18, 23],
    [2, 10, 15, 7, 18, 20, 5, 3, 19, 18], [2, 10, 15, 13, 10, 20, 6, 4, 10, 19, 24, 6, 18],
    [3, 7, 9, 5, 10, 4, 5, 1, 19, 0, 18, 4, 18, 9, 5, 18, 15], [24, 4, 18, 7, 18, 20, 5, 3, 19, 18],
    [24, 9, 23, 15, 1, 0, 0, 18, 4, 21], [24, 20, 20, 15, 16, 4, 1, 6, 6, 20, 18],
    [19, 24, 9, 23, 18, 5, 10, 23, 18, 23], [0, 3, 1, 4, 1, 9, 4, 28, 15, 3, 9, 24, 17, 20, 18],
    [26, 3, 1, 4, 15, 13, 18, 5, 10, 18, 15], [26, 3, 1, 4, 10, 20, 20, 1, 15, 27, 9, 15],
    [26, 3, 1, 4, 5, 18, 4, 16, 24, 10, 9, 16, 26], [26, 3, 1, 4, 10, 9, 9, 3, 5, 18, 9, 5, 18],
    [2, 4, 18, 18, 17, 18, 8, 24, 1, 27, 4, 15], [3, 9, 20, 26, 2, 4, 3, 1, 6, 8],
    [6, 4, 28, 16, 11, 3, 1, 4, 9, 18, 26], [7, 3, 4, 2, 5, 3, 9, 15, 1, 19, 21],
    [7, 3, 4, 2, 13, 4, 18, 15, 18, 4, 1, 21], [7, 10, 20, 20, 24, 4, 4, 10, 1, 18], [8, 24, 1, 18, 18, 9, 3, 1, 6, 8],
    [8, 18, 4, 18, 5, 3, 9, 0, 1, 15, 18, 23], [16, 4, 1, 2, 10, 19, 13, 3, 15, 18],
    [17, 3, 3, 5, 18, 14, 5, 18, 13, 16], [19, 1, 5, 8, 17, 18, 5, 24, 1, 15, 18],
    [19, 3, 4, 18, 0, 10, 9, 24, 20, 20, 26], [1, 3, 10, 5, 18, 10, 9, 15, 10, 23, 18],
    [4, 10, 6, 8, 16, 24, 17, 3, 1, 16], [7, 8, 10, 5, 8, 5, 24, 1, 15, 18], [7, 10, 2, 10, 9, 18, 10, 2, 18, 4],
    [9, 18, 1, 18, 4, 17, 18, 5, 3, 19, 18], [15, 8, 24, 13, 18, 3, 1, 4, 15, 18, 20, 1, 18, 15],
    [15, 16, 4, 3, 21, 18, 9, 3, 1, 6, 8], [0, 3, 20, 20, 3, 7, 26, 3, 1, 4], [0, 3, 20, 20, 3, 7, 4, 28, 15, 3, 9],
    [0, 3, 20, 20, 3, 7, 23, 3, 6, 19, 24], [2, 3, 1, 6, 8, 16, 15, 3, 19, 18], [3, 17, 16, 24, 10, 9, 7, 8, 24, 16],
    [4, 28, 20, 10, 16, 26, 1, 20, 16, 10, 19, 24, 16, 18, 20, 26], [7, 10, 15, 23, 3, 19, 24, 19, 24, 15, 15],
    [10, 9, 15, 10, 23, 18, 26, 3, 1, 4, 15, 18, 20, 0], [15, 24, 5, 4, 18, 23, 15, 3, 19, 18],
    [19, 24, 15, 16, 18, 4, 24, 6, 24, 10, 9], [19, 24, 15, 16, 18, 4, 4, 18, 13, 20, 10, 18, 23],
    [19, 24, 15, 16, 18, 4, 18, 14, 13, 20, 24, 10, 9, 18, 23], [19, 18, 4, 18, 20, 26, 7, 8, 24, 16],
    [3, 1, 16, 15, 10, 23, 18, 20, 10, 5, 18], [5, 3, 9, 15, 1, 19, 18, 16, 3, 3],
    [7, 18, 20, 5, 3, 19, 18, 13, 10, 20, 6, 4, 10, 19], [9, 1, 19, 17, 18, 4, 15, 0, 3, 4],
    [13, 24, 4, 24, 17, 20, 18, 20, 10, 5, 18], [13, 4, 3, 6, 4, 24, 19, 4, 28, 20, 10, 16, 26],
    [15, 16, 1, 23, 18, 9, 16, 24, 9, 23], [15, 16, 24, 4, 16, 18, 23, 17, 1, 16],
    [16, 3, 16, 10, 18, 9, 16, 0, 1, 9, 5, 16, 27, 9], [17, 18, 20, 10, 18, 1, 18, 9, 3, 2, 21],
    [18, 14, 13, 20, 24, 10, 9, 7, 8, 24, 16], [19, 18, 15, 15, 24, 6, 18, 5, 3, 9, 16, 24, 10, 9, 18, 23],
    [23, 18, 15, 16, 4, 3, 26, 24, 20, 20], [26, 3, 1, 4, 15, 18, 20, 0, 26, 3, 1],
    [26, 3, 1, 4, 15, 18, 20, 0, 28, 5, 8], [24, 16, 16, 24, 5, 8, 18, 23, 16, 3],
    [4, 28, 20, 10, 16, 10, 18, 15, 11, 3, 1, 4, 9, 18, 26], [10, 9, 8, 24, 17, 10, 16, 21, 24, 9],
    [13, 4, 18, 13, 24, 4, 18, 23, 16, 3], [13, 4, 18, 15, 18, 4, 1, 18, 2, 21, 15],
    [15, 16, 1, 23, 18, 9, 16, 15, 7, 18, 4, 18], [23, 10, 1, 10, 9, 10, 16, 26, 2, 18],
    [23, 10, 1, 10, 9, 10, 16, 26, 15, 3, 19, 18], [23, 10, 1, 10, 9, 10, 16, 26, 7, 10, 2, 10, 9],
    [23, 10, 15, 5, 3, 1, 18, 4, 24, 9], [23, 10, 15, 5, 3, 1, 18, 4, 16, 4, 1, 2],
    [23, 18, 5, 18, 13, 16, 27, 9, 7, 18], [24, 4, 17, 10, 16, 4, 24, 4, 26, 17, 3, 23, 26],
    [24, 23, 8, 18, 4, 18, 9, 5, 18, 7, 18], [24, 23, 8, 18, 4, 18, 9, 5, 18, 2, 24, 16],
    [5, 9, 3, 7, 20, 18, 23, 6, 18, 0, 10, 9, 23], [10, 4, 4, 10, 16, 24, 16, 18, 23, 10],
    [13, 4, 3, 0, 18, 15, 15, 3, 4, 2, 24, 16], [13, 4, 3, 0, 18, 15, 15, 3, 4, 4, 18, 13, 20, 10, 18, 23],
    [13, 4, 10, 19, 24, 20, 10, 16, 26, 24, 9, 23], [18, 9, 5, 4, 26, 13, 16, 18, 23, 5, 9, 3, 7],
    [5, 3, 9, 15, 1, 19, 13, 16, 27, 9, 7, 18], [10, 9, 15, 16, 4, 1, 5, 16, 27, 9, 23, 3],
    [10, 9, 15, 16, 4, 1, 5, 16, 27, 9, 5, 3, 19, 19, 24, 9, 23],
    [10, 9, 15, 16, 4, 1, 5, 16, 27, 9, 5, 7, 18, 15, 16, 27, 9],
    [10, 9, 15, 16, 4, 1, 5, 16, 27, 9, 13, 4, 3, 6, 4, 24, 19], [18, 14, 13, 18, 4, 10, 18, 9, 5, 18, 26, 3, 1, 4],
    [13, 4, 18, 15, 18, 4, 1, 24, 16, 27, 9, 7, 18], [13, 4, 18, 15, 18, 4, 1, 24, 16, 27, 9, 24, 9, 23],
    [18, 9, 20, 10, 6, 8, 16, 18, 9, 18, 23, 24, 9], [10, 9, 16, 18, 20, 20, 10, 6, 18, 9, 5, 18, 10, 15],
    [5, 10, 4, 5, 1, 19, 0, 18, 4, 18, 9, 5, 18, 13, 4, 24, 5, 16, 10, 5, 18, 15]

]

import key_list
decrypt_data['key_guesses'] = key_list.key_list

decrypt_data["dec_function"] = [#cry.decrypt_p_xor_k_to_p,
                                #cry.decrypt_k_xor_p_to_p,
                                cry3.decrypt_p_multiply_k1_add_k2_to_p
                                #cry.decrypt_p_minus_k_to_p,
                                #cry.decrypt_k_minus_p_to_p,
                                #cry.decrypt_p_multiply_k_to_p,
                                #cry.decrypt_p_divide_k_to_p,
                                #cry.decrypt_k_divide_p_to_p
                                ]
decrypt_data['interrupters'] = [None]#, 0, 5, 6, 7, 8, 11, 12, 13, 14, 17, 19, 20, 21, 22, 23, 25, 26, 27, 28]
decrypt_data['transpositions'] = ['L2R', 'R2L']


ahits = []
with open('./test_5455.txt', 'w') as f:
    for key_guess in decrypt_data["key_guesses"]:
        print(f'STARTING {key_guess}')
        decrypt_data['key1_guess'] = key_guess
        decrypt_data['key2_guess'] = "ctminus1"
        for method in decrypt_data["dec_function"]:
            print(f'STARTING METHOD {method}')
            apply_key_start = time.time()
            decrypt_data['decrypt_functions'] = [method]
            #print(cry.get_gematria_options_for_method(decrypt_data["decrypt_functions"][0]))
            decrypt_data['c_and_k_directions'], decrypt_data['c_and_k_rotations'] = cry3.get_gematria_options_for_method(
                decrypt_data["decrypt_functions"][0])
            hits, total_attempts, tru_hits, hit_dict = apply_key(decrypt_data, f)
            ahits.extend(hits)
            print(
                f'This iteration found {tru_hits} / {len(hits)}  / {total_attempts} Attempts {time.time() - apply_key_start} secs ')
            with open('./sorted_test_5455.txt', 'w') as f2:
                for hit in hits:
                    f2.write(f'{hit}\n')
                    f2.flush()

unique_hits= []
for i in ahits:
    if i in unique_hits:
        pass
    else:
        unique_hits.append(i)


with open('allsorted_test_5455_LPkeys.txt', 'w') as f2:
    for hit in sorted(unique_hits, key=itemgetter(4), reverse=True):
        f2.write(f'{hit}\n')
        f2.flush()