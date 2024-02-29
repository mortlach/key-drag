# cython: infer_types=True
import cython
import numpy as np
cimport numpy as cnp
cnp.import_array()

DTYPE = np.int64
ctypedef cnp.int64_t DTYPE_t


cpdef  hamming_distance_pos_C(dict_words,  r, w, int max_hd = 1):
    #dict_words = DictionaryLookUp.__all_words_index[ w[0][1]  - 1 ]
    #int min_hd = 15
    cdef int hd = 0
    cdef int min_hd = 15
    for word in dict_words:
        hd = 0
        for i in  range(len(r)):
            if word[ w[i][0] ] != r[i]:
                hd += 1
            if hd > max_hd:
                break
        if hd == 0:
            return 0
        if hd < min_hd:
            min_hd = hd
    return min_hd

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def  hamming_distance_pos_Cnp(cnp.ndarray[DTYPE_t, ndim=2] dict_words, cnp.ndarray[DTYPE_t, ndim=1] r, w, int max_hd = 1):
    cdef int hd = 0
    cdef int min_hd = 15
    for word in dict_words:
        hd = 0
        for i,j in zip(r,w):
            if word[ j[0] ] != i:
                hd += 1
            if hd > max_hd:
                break
        if hd == 0:
            return 0
        if hd < min_hd:
            min_hd = hd
    return min_hd


##cpdef int hamming_distance_pos_C(list[list[int]] dict_words, list[int] runes, list[list[int]] wli, int max_hd = 1):
##    '''
##        calc hamming distance <= max_hd
##    :param dict_words: are reference words, word data
##    :param word_data: output of create_word_data
##    :param max_hd: max hamming distance tolerated (otherwise quit)
##    :return: hamming distance <= max_hd
##    '''
##    cdef int hd = 0
##    cdef int min_hd = 15 # arbitrary initial value larger than any min hamming distance we might expect
##    for word in dict_words:
##        for i, r in zip(wli, runes):
##            if word[i[0]] != r:
##                hd += 1
##            if hd > max_hd:
##                break
##        if hd == 0:
##            return 0
##        if hd < min_hd:
##            min_hd = hd
##    return min_hd

cpdef list[int] get_gematria_rotation_C(list[int] data, int shift, str direction=''):
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

cpdef list[list[int]] get_all_gematria_rotations_C(list[int] data):
    '''
    if you know, you know
    :param data:
    :return:
    '''
    cdef list r = []
    for direction in ['normal','atbash']:
        for shift in range(29):
            r.append(get_gematria_rotation_C(data,shift,direction))
    return r

@cython.boundscheck(False) # turn off bounds-checking for entire function
@cython.wraparound(False)  # turn off negative index wrapping for entire function
def zero_shift1_C(cnp.ndarray[DTYPE_t, ndim=1] a):
    return (a-a[0]) % 29

cpdef list zero_shift(list a):
    offset = [x for x in a if type(x) == int]
    if len(offset) > 0:
        return [ (x-offset[0]) % 29 if type(x) == int else x for x in a]
    return a