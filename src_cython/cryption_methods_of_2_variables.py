'''
cryption methods for simple arithmetic functions
explicit is better than implicit ;)
this is about as simple as it need be
used in other files to encrypt / decrypt user data
follow patterns when adding your own function
'''

from itertools import product


def get_transposition_indices(text_len, transposition_key):
    '''
    define possible transpositions here, 2 obvious ones to start,
    but they can be basically arbitrary
    :param text_len: runes
    :param transposition_key: which transposition to use, must be defined in body
    :return:
    '''
    if transposition_key == 'L2R':
        transposition = list(range(text_len))
    elif transposition_key == 'R2L':
        transposition = list(range(text_len))
        transposition.reverse()
    else:
        print(f'Warning transposition_key {transposition_key} not found, using default order')
        transposition = list(range(text_len))
    return transposition


def get_gematria_rotation(data, shift, direction=''):
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


def get_all_gematria_rotations(data):
    '''
    if you know, you know
    :param data:
    :return:
    '''
    r = []
    for direction in ['normal', 'atbash']:
        for shift in range(29):
            r.append(get_gematria_rotation(data, shift, direction))
    return r


def zero_shift(a):
    '''
        shift entire list so first int element is zero
    :param a: [2,3,4,2,3]
    :return:
    '''
    offset = [x for x in a if type(x) == int]
    if len(offset) > 0:
        return [(x - offset[0]) % 29 if type(x) == int else x for x in a]


#     return a


''' encrypt arithmetic '''


def encrypt_p_plus_k(pt, key):
    if type(pt) == list:
        return [(p + k) % 29 for p, k in zip(pt, key)]
    return (pt + key) % 29


def encrypt_p_minus_k(pt, key):
    if type(pt) == list:
        return [(p - k) % 29 for p, k in zip(pt, key)]
    return (pt - key) % 29


def encrypt_k_minus_p(pt, key):
    if type(pt) == list:
        return [(k - p) % 29 for p, k in zip(pt, key)]
    return (key - pt) % 29


def encrypt_p_multiply_k(pt, key):
    if type(pt) == list:
        return [(p * k) % 29 for p, k in zip(pt, key)]
    return (pt * key) % 29


def encrypt_k_divide_p(pt, key, errorrune=''):
    '''
        if you define an error rune that will be used in case no solution. Otherwise original PT char will be used
    '''
    if errorrune == '':
        if type(pt) == list:
            return [(k * pow(p, -1, 29)) % 29 if p > 0 else p for p, k in zip(pt, key)]
        if pt > 0:
            return (key * pow(pt, -1, 29)) % 29
        else:
            return pt
    else:
        if type(pt) == list:
            return [(k * pow(p, -1, 29)) % 29 if p > errorrune else p for p, k in zip(pt, key)]
        if pt > 0:
            return (key * pow(pt, -1, 29)) % 29
        else:
            return errorrune


def encrypt_p_divide_k(pt, key, errorrune=''):
    '''
        if you define an error rune that will be used in case no solution. Otherwise original PT char will be used
    '''
    if errorrune == '':
        if type(pt) == list:
            return [(p * pow(k, -1, 29)) % 29 if k > 0 else p for p, k in zip(pt, key)]
        if key > 0:
            return (pt * pow(key, -1, 29)) % 29
        else:
            return pt
    else:
        if type(pt) == list:
            return [(p * pow(k, -1, 29)) % 29 if k > 0 else "e" for p, k in zip(pt, key)]
        if key > 0:
            return (pt * pow(key, -1, 29)) % 29
        else:
            return errorrune


def encrypt_p_xor_k(pt, key):
    if type(pt) == list:
        return [(p ^ k) % 29 for p, k in zip(pt, key)]
    return (pt ^ key) % 29


def encrypt_k_xor_p(pt, key):
    if type(pt) == list:
        return [(k ^ p) % 29 for p, k in zip(pt, key)]
    return (key ^ pt) % 29


##
## decryption methods, first use ct and key to generate pt
##
def get_decrypt_to_p_data(encryption_function_of_p_and_k):
    '''
    returns map of (c,k)->p for encryption_function_of_p_and_k, e.g. p+k=c
    '''
    raw_data = [(p, k1, encryption_function_of_p_and_k(p, k1)) for p, k1 in list(product(list(range(29)), repeat=2))]
    r = {}
    p, k, c = 0, 1, 2
    for data in raw_data:
        next_key = tuple([data[c], data[k]])
        if next_key in r:
            r[next_key].append(data[p])
        else:
            r[next_key] = [data[p]]
    return r


''' raw data dicts for decryption maps  '''
print('''Generating decryption maps''')
__decrypt_p_plus_k_to_p_data = get_decrypt_to_p_data(encrypt_p_plus_k)
__decrypt_p_minus_k_to_p_data = get_decrypt_to_p_data(encrypt_p_minus_k)
__decrypt_k_minus_p_to_p_data = get_decrypt_to_p_data(encrypt_k_minus_p)
__decrypt_p_multiply_k_to_p_data = get_decrypt_to_p_data(encrypt_p_multiply_k)
__decrypt_p_divide_k_to_p_data = get_decrypt_to_p_data(encrypt_p_divide_k)
__decrypt_k_divide_p_to_p_data = get_decrypt_to_p_data(encrypt_k_divide_p)
__decrypt_k_xor_p_to_p_data = get_decrypt_to_p_data(encrypt_k_xor_p)
__decrypt_p_xor_k_to_p_data = get_decrypt_to_p_data(encrypt_p_xor_k)

''' pass lists of ciphertext and key to bespoke decryption functions NO ERROR CHECKING '''


def decrypt_p_plus_k_to_p(ct, key):
    return [v for v in product(*[__decrypt_p_plus_k_to_p_data.get(tuple([c, k]), ["e"]) for c, k in zip(ct, key)])]


def decrypt_p_minus_k_to_p(ct, key):
    return [v for v in product(*[__decrypt_p_minus_k_to_p_data.get(tuple([c, k]), ["e"]) for c, k in zip(ct, key)])]


def decrypt_k_minus_p_to_p(ct, key):
    return [v for v in product(*[__decrypt_k_minus_p_to_p_data.get(tuple([c, k]), ["e"]) for c, k in zip(ct, key)])]


def decrypt_p_multiply_k_to_p(ct, key):
    return [v for v in product(*[__decrypt_p_multiply_k_to_p_data.get(tuple([c, k]), ["e"]) for c, k in zip(ct, key)])]


def decrypt_p_divide_k_to_p(ct, key):
    return [v for v in product(*[__decrypt_p_divide_k_to_p_data.get(tuple([c, k]), ["e"]) for c, k in zip(ct, key)])]


def decrypt_k_divide_p_to_p(ct, key):
    return [v for v in product(*[__decrypt_k_divide_p_to_p_data.get(tuple([c, k]), ["e"]) for c, k in zip(ct, key)])]


def decrypt_k_xor_p_to_p(ct, key):
    return [v for v in product(*[__decrypt_k_xor_p_to_p_data.get(tuple([c, k]), ["e"]) for c, k in zip(ct, key)])]


def decrypt_p_xor_k_to_p(ct, key):
    return [v for v in product(*[__decrypt_p_xor_k_to_p_data.get(tuple([c, k]), ["e"]) for c, k in zip(ct, key)])]


''' 
    for each method we only need consider certain objects 
    (assuming we check all rotations of any generated plaintext) 
'''
def get_gematria_options_for_method(df):
    if df == decrypt_p_xor_k_to_p:
        return [list(product(["normal", 'atbash'], repeat=2)), list(product(range(29), range(29), repeat=1))]
    if df == decrypt_k_xor_p_to_p:
        return [list(product(["normal", 'atbash'], repeat=2)), list(product(range(29), range(29), repeat=1))]
    if df == decrypt_p_plus_k_to_p:
        return [[["normal", 'atbash'], ["normal", 'normal']], [[0, 0]]]
    if df == decrypt_p_minus_k_to_p:
        return [[["normal", 'atbash'], ["normal", 'normal']], [[0, 0]]]
    if df == decrypt_k_minus_p_to_p:
        return [[["normal", 'atbash'], ["normal", 'normal']], [[0, 0]]]
    if df == decrypt_p_multiply_k_to_p:
        return [[["normal", 'normal']], list(product(range(29), range(29), repeat=1))]
    if df == decrypt_p_divide_k_to_p:
        return [list(product(["normal", 'atbash'], repeat=2)), list(product(range(29), range(29), repeat=1))]
    if df == decrypt_k_divide_p_to_p:
        return [list(product(["normal", 'atbash'], repeat=2)), list(product(range(29), range(29), repeat=1))]


''' must be same order for both lists '''
all_encrypt_methods_of_2_variables = [
    encrypt_p_xor_k,
    encrypt_k_xor_p,
    encrypt_p_plus_k,
    encrypt_p_minus_k,
    encrypt_k_minus_p,
    encrypt_p_multiply_k,
    encrypt_p_divide_k,
    encrypt_k_divide_p
]
''' must be same order with above list '''
all_decrypt_to_p_methods_of_2_variables = [
    decrypt_p_xor_k_to_p,
    decrypt_k_xor_p_to_p,
    decrypt_p_plus_k_to_p,
    decrypt_p_minus_k_to_p,
    decrypt_k_minus_p_to_p,
    decrypt_p_multiply_k_to_p,
    decrypt_p_divide_k_to_p,
    decrypt_k_divide_p_to_p
]
''' used to automatically pick correct opposite function '''
encrypt_to_decrypt = {e: d for e, d in zip(all_encrypt_methods_of_2_variables,
                                           all_decrypt_to_p_methods_of_2_variables)}
decrypt_to_encrypt = {d: e for e, d in zip(all_encrypt_methods_of_2_variables,
                                           all_decrypt_to_p_methods_of_2_variables)}
