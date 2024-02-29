'''
TEST using the cython version of
'''
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

''' loop through applying keys and testing output  '''
def apply_key(decrypt_data, ans_data):
    # set up key-dragger
    kd = key_drag.KeyDrag()
    # what to do with errors? for now, exclude them (could treat as a form of interrupter, etc.)
    discard_errors = True
    # drag key over all options
    [wlis, r] = kd.drag_key(ct=decrypt_data['c_index'], key=decrypt_data['key_guess'],
                                           wli=decrypt_data['wli'], interrupters=decrypt_data['interrupters'],
                                           transpositions=decrypt_data['transpositions'],
                                           c_and_k_directions=decrypt_data['c_and_k_directions'],
                                           c_and_k_rotations=decrypt_data['c_and_k_rotations'],
                                           decrypt_functions=decrypt_data['decrypt_functions'],
                                           discard_errors=discard_errors)

    # plaintext analysis
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
        # interrupter position
        int_pos = [i for i, p in enumerate(this_pt) if p == -1]
        # all rotations for this PT
        this_pt_allrot = nm.get_all_gematria_rotations_C(list(this_pt))

        for opts_counter, interrupt in enumerate(interrupters):
            # options for this PT
            opts_for_this_pt = these_opts[opts_counter]
            # meh - manually re-insert interrupter after all gematria rotations
            for part in int_pos:
                for a in this_pt_allrot:
                    a[part] = interrupt
            # test all PT
            for rot_pt in this_pt_allrot:
                total_attempts += 1
                # two language test  tests, first on ngrams (just using w3-gram sfro now
                lm_threshold = -3
                result1 = lm1.get_distance_from_mean_w3(rot_pt, wli_at_this_index)
                all_neg = all([x > lm_threshold for x in result1])
                if all_neg:
                    # 2nd test on words
                    result2 = lm2.find_min_HD(rot_pt, wli_at_this_index)
                    max_hd = 1
                    if result2 <= max_hd:
                        # a hit keep data and write some message
                        this_pt_as_string = kd.get_as_runeglish_plaintext(this_pt=rot_pt, this_wli=wli_at_this_index)
                        if this_pt_as_string not in hit_dict:
                            datatosave = [this_pt_as_string, this_i, result1, sum(result1), opts_for_this_pt]
                            hit_dict[this_pt_as_string] = datatosave
                            rot_pt_s = ''.join(str(i) for i in rot_pt)
                            hit_data.append(datatosave)
                            if rot_pt_s in ans_data:
                                tru_hits += 1
    return sorted(hit_data, key=itemgetter(3), reverse=True), total_attempts, tru_hits



if __name__ == "__main__":
    tload1 = time.time()
    lm1 = ngmod.NGramModel(True, False)
    lm2 = wmod.WordModel(True)
    failed_count = 0
    success_count = 0
    signal_to_noise = []
    counter = 0
    from cProfile import Profile
    from pstats import SortKey, Stats

    with Profile() as profile:
        while success_count < 10:
            counter += 1
            print(f'\n***** ATTEMPT {counter} ****** ')
            ## setup a test encryption using current methods / assumptions nad options ##
            pt_test = "Welcome welcome pilgrim to the great journey toward the end of all things"
            [test_data, decrypt_data] = gt.get_test_encryption(pt_test)
            for k, v in test_data.items():
                print(f'{k} = {v}')
            apply_key_start = time.time()
            hits, total_attempts, tru_hits = apply_key(decrypt_data, test_data['p_index_str'])
            signal_to_noise.append([tru_hits, len(hits), total_attempts])
            if tru_hits > 0:
                success_count += 1
            apply_key_end = time.time()
            for item in hits:
                print(item)
            print(f'{success_count}/ {counter} This iteration found {tru_hits} / {len(hits)}  / {total_attempts} Attempts {apply_key_end-apply_key_start} secs ')
        for item in signal_to_noise:
            print(item)
    (
        Stats(profile)
        .strip_dirs()
        .sort_stats(SortKey.CUMULATIVE)
    #    '''    CALLS  CUMULATIVE,    FILENAME,    LINE,    NAME,    NFL ,    PCALLS ''''
        .print_stats()
    )
    print(f'{success_count} / {counter} ')
