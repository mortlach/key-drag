'''
Start of cryption methods for 3 vars
explicit is better than implicit ;)
this is about as simple as it need be
used in other files to encrypt / decrypt user data
follow patterns when adding your own function
'''
from itertools import product


def encrypt_p_multiply_k1_add_k2(pt, key1, key2):
    if type(pt) == list:
        return [(p * k1 + k2) % 29 for p, k1, k2 in zip(pt, key1, key2)]
    return (pt * key1 + key2) % 29

# for testing, encrypt_p_multiply_k1_add_k2, it's useful to have a function that does not depend on key2
def encrypt_p_i_multiply_k_i_add_cMinus1(pt, key1, offset):
    ct = [-1] * len(pt)
    ct[0] = pt[0] * key1[0] + offset
    for i in range(1,len(pt)):
        ct[i] = pt[i] * key1[i] + ct[i-1]
    return [x % 29 for x in ct]

def get_decrypt_to_p_data(encryption_function_of_p_and_k):
    '''
    returns map of (c,k)->p for encryption_function_of_p_and_k, e.g. p+k=c
    '''
    raw_data = [(p, k1, k2, encryption_function_of_p_and_k(p, k1, k2)) for p, k1, k2, in list(product(list(range(29)), repeat=3))]
    r = {}
    p, k1, k2, c = 0, 1, 2, 3
    for data in raw_data:
        next_key = tuple([data[c], data[k1], data[k2]])
        if next_key in r:
            r[next_key].append(data[p])
        else:
            r[next_key] = [data[p]]
    return r


__decrypt_p_multiply_k1_add_k2_to_p_data = get_decrypt_to_p_data(encrypt_p_multiply_k1_add_k2)
# for k,v in __decrypt_p_multiply_k1_add_k2_to_p_data.items():
#     print(f'{k} = {v}')
''' pass lists of ciphertext and key to bespoke decryption functions NO ERROR CHECKING '''
def decrypt_p_plus_k_to_p(ct, key1, key2):
    # test = []
    # for c, k1, k2 in zip(ct, key1, key2):
    #     aaa = __decrypt_p_multiply_k1_add_k2_to_p_data.get(tuple([c, k1, k2]), ["e"])
    #     test.append(aaa)
    return [v for v in product(
        *[__decrypt_p_multiply_k1_add_k2_to_p_data.get(tuple([c, k1, k2]), ["e"]) for c, k1, k2 in
          zip(ct, key1, key2)])]


def get_gematria_options_for_method(df):
    if df == decrypt_p_plus_k_to_p:
        #return [list(product(["normal", 'atbash'], repeat=2)), list(product(range(29), repeat=2))]
        return [[["normal", 'normal']], list(product(range(29), range(29), repeat=1))]


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

''' must be same order for both lists '''
all_encrypt_methods_of_3_variables = [encrypt_p_multiply_k1_add_k2]
''' must be same order with above list '''
all_encrypt_plaintext_methods_of_3_variables = [encrypt_p_i_multiply_k_i_add_cMinus1]
''' must be same order with above list '''
all_decrypt_to_p_methods_of_3_variables = [decrypt_p_plus_k_to_p]


''' used to automatically pick correct opposite function '''
encrypt_to_decrypt = {e: d for e, d in zip(all_encrypt_methods_of_3_variables,
                                           all_decrypt_to_p_methods_of_3_variables)}
decrypt_to_encrypt = {d: e for e, d in zip(all_encrypt_methods_of_3_variables,
                                           all_decrypt_to_p_methods_of_3_variables)}

''' used to automatically pick correct encryption function if using defined plaintext  '''
encrypt_to_encrypt_plaintext = {e: d for e, d in zip(all_encrypt_methods_of_3_variables,
                                           all_encrypt_plaintext_methods_of_3_variables)}





