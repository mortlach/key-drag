import time
import random
import numpy as np
import src_cython.generate_test as gt
import src_cython.gematria as gem
import src_cython.cryption_methods_of_2_variables as cry
import src_cython.key_drag as key_drag
import src_cython.ngram_model as ngmod
import src_cython.word_model as wmod
import src_cython.numerical_methods as nm
from operator import itemgetter

tload1 = time.time()
lm1 = ngmod.NGramModel(True, False)
lm2 = wmod.WordModel(True)


def apply_key(decrypt_data, outputfile):
    # set up key-dragger
    kd = key_drag.KeyDrag()
    # what to do with errors? for now, exclude them (could treat as a form of interrupter, etc.)
    discard_errors = True
    [wlis, r] = kd.drag_key(ct=decrypt_data['c_index'], key=decrypt_data['key_guess'],
                            wli=decrypt_data['wli'], interrupters=decrypt_data['interrupters'],
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
        this_pt_allrot = nm.get_all_gematria_rotations_C(list(this_pt))
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
                            datatosave = [decrypt_data['key_guess'], this_pt_as_string, this_i, result1, sum(result1), opts_for_this_pt]
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
]

import key_list
decrypt_data['key_guesses'] = key_list.key_list

decrypt_data["dec_function"] = [#cry.decrypt_p_xor_k_to_p,
                                #cry.decrypt_k_xor_p_to_p,
                                cry.decrypt_p_plus_k_to_p
                                #cry.decrypt_p_minus_k_to_p,
                                #cry.decrypt_k_minus_p_to_p,
                                #cry.decrypt_p_multiply_k_to_p,
                                #cry.decrypt_p_divide_k_to_p,
                                #cry.decrypt_k_divide_p_to_p
                                ]
decrypt_data['interrupters'] = [None, 0, 5, 6, 7, 8, 11, 12, 13, 14, 17, 19, 20, 21, 22, 23, 25, 26, 27, 28]
decrypt_data['transpositions'] = ['L2R', 'R2L']


ahits = []
with open('./test_5455.txt', 'w') as f:
    for key_guess in decrypt_data["key_guesses"]:
        decrypt_data['key_guess'] = key_guess
        for method in decrypt_data["dec_function"]:
            print(f'STARTING METHOD {method}')
            apply_key_start = time.time()
            decrypt_data['decrypt_functions'] = [method]
            #print(cry.get_gematria_options_for_method(decrypt_data["decrypt_functions"][0]))
            decrypt_data['c_and_k_directions'], decrypt_data['c_and_k_rotations'] = cry.get_gematria_options_for_method(
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

