'''
Class that scores plaintext
Log probability of ngrams with/without information about character's word length and index in word
'''
from ast import literal_eval
import time
import csv


class NGramModel:
    '''

    '''

    ''' class to score plaintext - runes are all defined in terms of index in gematria '''
    __w3_loaded = False
    __w4_loaded = False

    # raw transition matrix data stored in these dictionaries.
    # keys are up to runes
    ''' keys are tuple([r1 index in word, r1 word length, r1, r2, r3]) output is log prob '''
    __tm_rwli_3 = {}
    ''' keys are tuple([r1 index in word, r1 word length, r1, r2, r3, r4]) output is log prob'''
    __tm_rwli_4 = {}

    # default minimum score (updated in load_raw_tm_data)
    __tm_rwli_3_min = -25
    __tm_rwli_4_min = -25

    # "expected" score per ngram for "true" runeglish (measured from project runeberg)
    [__w3_mean, __w4_mean] = [-5.26217, -7.75378]

    # standard deviation of "expected" score per ngram for "true runeglish" as the number of ngrams in phrase increases
    __w3_sd = {1: 2.21654, 2: 2.21654, 3: 2.21654, 4: 2.21654, 5: 2.21654, 6: 2.21654, 7: 2.03109, 8: 1.89282,
               9: 1.77089, 10: 1.67998, 11: 1.59448, 12: 1.53094}
    __w4_sd = {1: 3.0063, 2: 3.0063, 3: 3.0063, 4: 3.0063, 5: 3.0063, 6: 3.0063, 7: 2.73505, 8: 2.54176, 9: 2.35905,
               10: 2.23328, 11: 2.10699, 12: 2.02206}

    def __init__(self, load_w3=True, load_w4=False):
        if load_w3:
            self.load_raw_tm_data_w3()
        if load_w4:
            self.load_raw_tm_data_w4()

    def load_raw_tm_data_w3(self):
        if not NGramModel.__w3_loaded:
            t1 = time.time()
            with open('./data/tm_wli_models3p.csv', newline='\n') as csvfile:
                NGramModel.__tm_rwli_3 = {literal_eval(','.join(row[:-1])): float(row[-1]) for row in
                                          csv.reader(csvfile, delimiter=',', quotechar='|')}
                NGramModel.__tm_rwli_3_min = min(NGramModel.__tm_rwli_3.values())
            NGramModel.__w3_loaded = True

    def load_raw_tm_data_w4(self):
        if not NGramModel.__w4_loaded:
            t1 = time.time()
            with open('./data/tm_wli_models4p.csv', newline='\n') as csvfile:
                NGramModel.__tm_rwli_4 = {literal_eval(','.join(row[:-1])): float(row[-1]) for row in
                                          csv.reader(csvfile, delimiter=',', quotechar='|')}
                NGramModel.__tm_rwli_4_min = min(NGramModel.__tm_rwli_4.values())
            NGramModel.__w4_loaded = True

    def __get_w3_0(self, k):
        return NGramModel.__tm_rwli_3.get(tuple([k[0], k[1], 'z']), NGramModel.__tm_rwli_3_min)

    def __get_tm_rwli_3(self, k):
        return NGramModel.__tm_rwli_3.get(k, self.__get_w3_0(k))

    def __get_w4_0(self, k):
        return NGramModel.__tm_rwli_4.get(tuple([k[0], k[1], k[2], 'z']), NGramModel.__tm_rwli_4_min)

    def __get_tm_rwli_4(self, k):
        return NGramModel.__tm_rwli_4.get(k, self.__get_w4_0(k))

    def get_logprob_wlir_data_w3(self, runes, wli, subtract_mean=True):
        return [self.__get_tm_rwli_3(tuple([wli[i][1], wli[i][0], runes[i], runes[i + 1],
                                            runes[
                                                i + 2]])) - NGramModel.__w3_mean if subtract_mean else self.__get_tm_rwli_3(
            tuple([wli[i][1], wli[i][0], runes[i], runes[i + 1], runes[i + 2]])) for i in range(len(runes) - 2)]

    def get_logprob_wlir_data_w4(self, runes, wli, subtract_mean=True):
        return [self.__get_tm_rwli_4(tuple([wli[i][1], wli[i][0], runes[i], runes[i + 1], runes[i + 2],
                                            runes[
                                                i + 3]])) - NGramModel.__w4_mean if subtract_mean else self.__get_tm_rwli_4(
            tuple([wli[i][1], wli[i][0], runes[i], runes[i + 1], runes[i + 2], runes[i + 3]])) for i in
                range(len(runes) - 3)]

    def get_distance_from_mean_w3w4(self, rune, wli):
        [rw3, rw4] = [self.get_logprob_wlir_data_w3(rune, wli, True),
                      self.get_logprob_wlir_data_w4(rune, wli, True)
                      ]
        mean_dif = [
            sum(rw3) / (len(rw3) * NGramModel.__w3_sd.get(len(rw3), NGramModel.__w3_sd[12])),
            sum(rw4) / (len(rw4) * NGramModel.__w4_sd.get(len(rw4), NGramModel.__w4_sd[12])),
        ]
        return mean_dif

    def get_distance_from_mean_w3(self, rune, wli):
        [rw3] = [self.get_logprob_wlir_data_w3(rune, wli, True)]
        mean_dif = [
            sum(rw3) / (len(rw3) * NGramModel.__w3_sd.get(len(rw3), NGramModel.__w3_sd[12])),
        ]
        return mean_dif

    def score_plaintext(self, this_pt, this_wli, lm_threshold=-3, max_hd=1):
        # could add an ngram check for even more discriminating hamming tests
        # result = self.lm.get_distance_from_mean_w3w4(this_pt, this_wli)
        result = self.lm.get_distance_from_mean_w3(this_pt, this_wli)
        all_neg = all([x > lm_threshold for x in result])
        if all_neg:
            if self.dl.find_min_HD(this_pt, this_wli) <= max_hd:
                return [True, result]
        return [False, result]
