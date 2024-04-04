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
    if type(pt) == list:
        for i in range(2,len(pt)):
            ct[i] = pt[i] * key1[i] + ct[i-1]
    return ct

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



__decrypt_p_xor_k_to_p_data = get_decrypt_to_p_data(encrypt_p_multiply_k1_add_k2)
__decrypt_p_multiply_k1_add_k2_to_p_data = get_decrypt_to_p_data(encrypt_p_multiply_k1_add_k2)

''' pass lists of ciphertext and key to bespoke decryption functions NO ERROR CHECKING '''


def decrypt_p_plus_k_to_p(ct, key1, key2):
    return [v for v in product(
        *[__decrypt_p_multiply_k1_add_k2_to_p_data.get(tuple([c, k1, k2]), ["e"]) for c, k1, k2 in
          zip(ct, key1, key2)])]
