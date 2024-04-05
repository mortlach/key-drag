'''
a Klass to do the key dragging
'''
from itertools import product, chain, combinations
import src_py.cryption_methods_of_2_variables as cry
import src_py.gematria as gem


class KeyDrag:

    def __init__(self):
        pass

    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        s = list(iterable)
        return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))

    def drag_key(self, ct, key1, key2, wli, interrupters, transpositions, c_and_k_directions, c_and_k_rotations,
                 decrypt_functions, discard_errors=True):
        '''

        :param ct: list ct int 0,28 normla gematri arune index
        :param key: list int 0 to 28
        :param wli: word-length-index info [[a0,b0],[a1,b1],[a2,b2],[a3,b3],[a4,b4]...]
                    a's are index in word b's are word length
                    MUST be same length as ct and start with same rune as ct
        :param interrupters: list of interrupters, int 0,28 and/or None
        :param transpositions: list of lists of strings defining all transpositions [[]]
        :param c_and_k_directions: atbash normal choices
        :param c_and_k_rotations: 0 to 28
        :param decrypt_functions: function pointers
        :param discard_errors:
        :return:
        '''
        pts_with_opts = []
        # loop from start of ct to end (TODO no wrap around)
        for counter in range(len(ct) - len(key1)):
            # pass all options to each ct the key can be applied to
            # next_pt_withopts are lists of [[pt1,opts1],[pt2,opts2],[pt3,opts3],[pt4,opts4] ... ]

            if counter == 0:
                offset = 0
            else:
                offset = ct[counter-1]

            next_pt_withopts = self.apply_key_from_options(ct[counter:counter + len(key1)],
                                                           key1,
                                                           key2,
                                                           offset,
                                                           interrupters,
                                                           transpositions,
                                                           c_and_k_directions,
                                                           c_and_k_rotations,
                                                           decrypt_functions,
                                                           discard_errors)

            pts_with_opts.append(next_pt_withopts)
        # get the wlis for each item in pts_with_opts
        wlis = [wli[counter:counter + len(key1)] for counter in range(len(ct) - len(key1))]
        # assert len(pts_with_opts) == len(wlis)
        # only keep unique PT (for each index)
        r = {}
        for index, item in enumerate(pts_with_opts):
            for pts, opts in item:
                for p in pts:
                    next_key = tuple([tuple(p), index])
                    r.setdefault(next_key, []).append(opts)
        return [wlis, r]

    def flatten(self, li):
        return sum(([x] if not isinstance(x, list) else self.flatten(x) for x in li), [])

    def wli_2_string(self, data, rune_type=None):
        if rune_type == "rune":
            return ''.join(self.flatten([gem.rune2latincanon(x[0]) if x[1] > 0 else [' ', x[0]] for x in data]))
        return ''.join(self.flatten([x[0] if x[1] > 0 else [' ', x[0]] for x in data]))

    def get_as_runeglish_plaintext(self, this_pt, this_wli):
        '''
            create a string of the PT using wli info to set spaces, and blank '_' chars at start and end phrase
        :param this_pt:
        :param this_wli:
        :return:
        '''
        found_plaintext = self.wli_2_string(
            [[gem.position2latincanon(k_i), c[0], c[1]] for k_i, c in zip(this_pt, this_wli)])
        if this_wli[0][0] > 0:
            found_plaintext = ''.join(["_"] * this_wli[0][0]) + found_plaintext
        if this_wli[-1][0] < (this_wli[-1][1] - 1):
            found_plaintext = found_plaintext + (''.join(["_"] * (this_wli[-1][1] - this_wli[-1][0] - 1)))
        return found_plaintext

    def apply_key_from_options(self, ct, key1, key2, offset, interrupters, transpositions, c_and_k_directions, c_and_k_rotations,
                               decrypt_functions, discard_errors=True):
        # for this ciphertext fragment no point checking interrupters that are not present
        interrupters_cut = [None] + [i for i in interrupters if i in ct]
        options = product(c_and_k_directions, c_and_k_rotations,
                          [cry.get_transposition_indices(len(ct), t) for t in transpositions], interrupters_cut,
                          decrypt_functions, repeat=1)
        pts_with_opts = []
        for o in options:
            pts_from_decryption = self.do_the_decrypt(ct=ct,
                                                      key1=key1,
                                                      key2=key2,
                                                      offset = offset,
                                                      ct_dir=o[0][0],
                                                      k_dir=o[0][1],
                                                      c_rot=o[1][0],
                                                      k_rot=o[1][1],
                                                      trans=o[2],
                                                      inter=o[3],
                                                      decrypt_func=o[4], discard_errors=discard_errors)
            pts_with_opts.append([pts_from_decryption, o])
        return pts_with_opts

    def get_gematria_rotation(self, data, shift, direction=''):
        '''
        add a shift or atbash then shift
        :param data:
        :param shift:
        :param direction:
        :return:
        '''
        if direction == 'atbash':
            return [(28 - d + shift) % 29 for d in data]
        return [(d + shift) % 29 for d in data]

    def zero_shift(self, a):
        '''
            shift entire list so first int element is zero
        :param a: [2,3,4,2,3]
        :return:
        '''
        offset = [x for x in a if type(x) == int]
        if len(offset) > 0:
            return [(x - offset[0]) % 29 if type(x) == int else x for x in a]
        return a

    def do_the_decrypt(self, ct, key1, key2 , offset, ct_dir, c_rot, k_dir, k_rot, inter, trans, decrypt_func, discard_errors=True):
        '''
            create PT from these options, apply all options, decrypt, return complete pt
        :param ct:
        :param key:
        :param ct_dir:
        :param ct_rot:
        :param k_dir:
        :param k_rot:
        :param trans:
        :param inter:
        :param decryption_func:
        :return:
        '''
        # each possible interrupter
        ct_int_pos = [i for i, p in enumerate(ct) if p == inter]
        # all subsets of ct_int_pos
        int_positions = list(self.powerset(ct_int_pos))
        # ASSUME we always have checked no interrupters, so do not repeat when interrupters are present
        if len(int_positions) > 1:
            int_positions.remove(())
        pts = []
        for this_int_pos in int_positions:
            # get the interrupters
            ct_interrupter = [c for i, c in enumerate(ct) if i not in this_int_pos]
            # make sure transpose index are not too great
            transc = [i for i in trans if i < len(ct_interrupter)]
            # apply transpose
            ct_transposed = [ct_interrupter[i] for i in transc]
            # rotate
            ct_rot = self.get_gematria_rotation(ct_transposed, c_rot, ct_dir)
            key1_rot = self.get_gematria_rotation(key1, k_rot, k_dir)[len(this_int_pos):]

            if key2 == "ctminus1":
                key2_rot = [offset] + ct_rot[:-1]
            # decrypt, this creates a list of (potentially) multiple PTs
            l1 = len(ct_rot)
            l2 = len(key1_rot)
            l3 = len(key2_rot)
            # what offset to use ? could get complex with interrupters ....


            temp_p = [list(p) for p in decrypt_func(ct_rot, key1_rot, key2_rot)]
            # discard 'e'
            if discard_errors:
                # temp_p2 = [np.asarray(p, dtype= np.int64) for p in temp_p if "e" not in p]
                temp_p2 = [p for p in temp_p if "e" not in p]
            if temp_p2:
                # untranspose
                pts_untransposed = [[p[i] for i in transc] for p in temp_p]
                #
                # re-insert interrupters AS -1
                pts_untransposed = [cry.zero_shift(p) for p in pts_untransposed]
                for ipos in this_int_pos:
                    for pts_item in pts_untransposed:
                        pts_item.insert(ipos, -1)
                pts.extend(pts_untransposed)
        return pts
