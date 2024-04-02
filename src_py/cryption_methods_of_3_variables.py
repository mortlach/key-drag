def encrypt_p_multiply_k1_add_k2(pt, key1, key2):
    if type(pt) == list:
        return [(p * k1 + k2) % 29 for p, k1, k2 in zip(pt, key1, key2)]
    return (pt * key1 + key2) % 29