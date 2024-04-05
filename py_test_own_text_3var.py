'''
TEST - using pure python libs
'''
import time
import random
import src_py.gematria as gem
import src_py.generate_test as gt
import src_py.cryption_methods_of_3_variables as cry
import src_py.key_drag_3var as key_drag
import src_py.ngram_model as ngmod
import src_py.word_model as wmod



def apply_key(decrypt_data, ans_data):
    # set up key-dragger
    kd = key_drag.KeyDrag()
    # what to do with errors? for now, exclude them (could treat as a form of interrupter, etc.)
    discard_errors = True
    [wlis, r] = kd.drag_key(ct=decrypt_data['c_index'],
                            key1=decrypt_data['key1_guess'],
                            key2=decrypt_data['key2_guess'],
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
        this_pt_allrot = cry.get_all_gematria_rotations(list(this_pt))
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

                all_neg = all([x > lm_threshold for x in result1])

                if all_neg:
                    # 2nd test on word
                    result2 = lm2.find_min_HD(rot_pt, wli_at_this_index)
                    max_hd = 1
                    if result2 <= max_hd:
                        # a hit
                        this_pt_as_string = kd.get_as_runeglish_plaintext(this_pt=rot_pt, this_wli=wli_at_this_index)
                        if this_pt_as_string not in hit_dict:
                            datatosave = [this_pt_as_string, this_i, result1, opts_for_this_pt]
                            hit_dict[this_pt_as_string] = datatosave
                            rot_pt_s = ''.join(str(i) for i in rot_pt)
                            hit_data.append(datatosave)
                            if rot_pt_s in ans_data:
                                # print(f'TRU HIT {this_pt_as_string}, {this_i}, {result1} {opts_for_this_pt}')
                                tru_hits += 1
    return hit_data, total_attempts, tru_hits


if __name__ == "__main__":
    tload1 = time.time()
    lm1 = ngmod.NGramModel(True, False)
    lm2 = wmod.WordModel(True)
    failed_count = 0
    success_count = 0
    signal_to_noise = []
    counter = 0

    while success_count < 100:
        counter += 1
        print(f'\n***** ATTEMPT {counter} ****** ')
        ## setup a test encryption using current methods / assumptions nad options ##
        pt_test = "Welcome welcome pilgrim to the great journey toward the end of all things"
        [test_data, decrypt_data] = gt.get_test_encryption_3V(pt_test)
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
        print(
            f'{success_count}/ {counter} This iteration found {tru_hits} / {len(hits)}  / {total_attempts} Attempts {apply_key_end - apply_key_start} secs ')
    for item in signal_to_noise:
        print(item)
    print("FINISHED")


    from cProfile import Profile
    from pstats import SortKey, Stats

    # with Profile() as profile:
    #     while success_count < 100:
    #         counter += 1
    #         print(f'\n***** ATTEMPT {counter} ****** ')
    #         ## setup a test encryption using current methods / assumptions nad options ##
    #         pt_test = "Welcome welcome pilgrim to the great journey toward the end of all things"
    #         [test_data, decrypt_data] = gt.get_test_encryption(pt_test)
    #         for k, v in test_data.items():
    #             print(f'{k} = {v}')
    #         apply_key_start = time.time()
    #         hits, total_attempts, tru_hits = apply_key(decrypt_data, test_data['p_index_str'])
    #         signal_to_noise.append([tru_hits, len(hits), total_attempts])
    #         if tru_hits > 0:
    #             success_count += 1
    #         apply_key_end = time.time()
    #         for item in hits:
    #             print(item)
    #         print(
    #             f'{success_count}/ {counter} This iteration found {tru_hits} / {len(hits)}  / {total_attempts} Attempts {apply_key_end - apply_key_start} secs ')
    #     for item in signal_to_noise:
    #         print(item)
    # (
    #     Stats(profile)
    #     .strip_dirs()
    #     .sort_stats(SortKey.CUMULATIVE)
    #     #    '''    CALLS  CUMULATIVE,    FILENAME,    LINE,    NAME,    NFL ,    PCALLS ''''
    #     .print_stats()
    # )
