import csv
import src_cython.gematria as gem
import time
import src_cython.numerical_methods as nm
import numpy as np


class WordModel:
    '''
    A dictionary of "approved" runeglish words with lengths 1 to 14 runes.
    Data is imported from csv files that are the same as used in the "LP Crib Assist" app. https://github.com/mortlach/Liber-Primus-Crib-Assist
    Having a good list of words will reduce noise
    ATM the wordlists are still being cut, continuing that process will improve accuracy and general speed
    The main purpose of this class is to compute a "hamming distance"
    Having a smaller list of approved words will increase speed
    '''
    # After loading, contains all words as rune strings
    __all_words_runes = None
    # After loading, contains all words as lists of rune-index
    __all_words_index = None
    __all_words_index_np = None

    def __init__(self, should_init_data = False):
        if should_init_data:
            self.init_data()

    def readcsvtodict(self, fp):
        '''
        read csv formatted like: a,30285331759,1,ᚪ,97
        :param fp: file path
        :return: dictionary of data
        '''
        with open(fp, mode='r',encoding='utf-8') as file:
            return  { r[3] : [r[0], int(r[1]), int(r[4])] for r in csv.reader(file) if int(r[2]) == 1 }

    def init_data(self):
        '''
        data is imported from csv files that are the same as used in the "LP Crib Assist" app.
        rune-strings are converted to rune-index lists
        '''
        print(f'DL load word lists', end=" ")
        ts = time.time()
        WordModel.__all_words = [self.readcsvtodict('./data/1_grams/raw1grams_01.csv'),
                                 self.readcsvtodict('./data/1_grams/raw1grams_02.csv'), self.readcsvtodict('./data/1_grams/raw1grams_03.csv'),
                                 self.readcsvtodict('./data/1_grams/raw1grams_04.csv'), self.readcsvtodict('./data/1_grams/raw1grams_05.csv'),
                                 self.readcsvtodict('./data/1_grams/raw1grams_06.csv'), self.readcsvtodict('./data/1_grams/raw1grams_07.csv'),
                                 self.readcsvtodict('./data/1_grams/raw1grams_08.csv'), self.readcsvtodict('./data/1_grams/raw1grams_09.csv'),
                                 self.readcsvtodict('./data/1_grams/raw1grams_10.csv'), self.readcsvtodict('./data/1_grams/raw1grams_11.csv'),
                                 self.readcsvtodict('./data/1_grams/raw1grams_12.csv'), self.readcsvtodict('./data/1_grams/raw1grams_13.csv'),
                                 self.readcsvtodict('./data/1_grams/raw1grams_14.csv')]
        WordModel.__all_words_index = [[[gem.rune2position(c) for c in word] for word in wl] for wl in WordModel.__all_words]

        WordModel.__all_words_index_np = [np.array(x,dtype=np.int64) for x in  WordModel.__all_words_index]

        print(WordModel.__all_words_index[0][0])
        print(f' took {time.time() - ts} secs', end="\n")

    def create_word_data(self, runes_index, wli_data):
        '''
        Splits rune and wli data by word so they can be looked up in individual wordlists
        :param runes_index: e.g. [7, 18, 20, 5, 3, 19, 18, 7]
        :param wli_data: e.g. [[0, 3], [1, 3], [2, 3], [0, 2], [1, 2], [0, 7], [1, 7], [3, 7]]
        :return: [[7, 18, 20, 5, 3, 19, 18], [7]], [[[0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7]], [[0, 7]]]
        '''
        return_runes, return_wli = [], []
        nextrunes, nextwli = [], []
        for rune, wli in zip(runes_index, wli_data):
            if wli[0] == 0:
                if nextrunes:
                    return_runes.append(nextrunes)
                    return_wli.append(nextwli)
                nextwli, nextrunes = [wli], [rune]
            else:
                nextwli.append(wli)
                nextrunes.append(rune)

        if nextrunes:
            return_runes.append(nextrunes)
            return_wli.append(nextwli)

        return return_runes, return_wli

    def create_word_dataOLD(self, runes_index, wli_data):
        '''
            splits rune and wli data by word so they can be looked up in individual wordlists to we find hamming distance
            each item of return list is passed with wordlist to hamming_funciton
        :param runes_index: e.g.[7, 18, 20, 5, 3, 19, 18, 7]
        :param wli_data: e.g. [[0, 3], [1, 3], [2, 3], [0, 2], [1, 2], [0, 7], [1, 7], [3, 7]]
        :return: will give   [[7, 18, 20, 5, 3, 19, 18], [7]] , [[[0, 7], [1, 7], [2, 7], [3, 7], [4, 7], [5, 7], [6, 7]], [[0, 7]]]
        '''
        nextrunes = []
        nextwli = []
        return_wli = []
        return_runes = []
        for i in range(len(runes_index)):
            if wli_data[i][0] == 0:
                if nextrunes:  # Check if nextrunes is not empty before appending to word_data
                    return_runes.append(nextrunes)
                    return_wli.append(nextwli)
                nextwli = [wli_data[i]]
                nextrunes = [runes_index[i]]
            else:
                nextwli.append(wli_data[i])
                nextrunes.append(runes_index[i])
        # Append the last group
        if nextrunes:
            return_runes.append(nextrunes)
            return_wli.append(nextwli)
        return return_runes,return_wli

    def hamming_distance_pos(self, dict_words, runes, wli, max_hd = 1):
        '''
            calc hamming distance <= max_hd
        :param dict_words: are reference words, word data
        :param word_data: output of create_word_data
        :param max_hd: max hamming distance tolerated (otherwise quit)
        :return: hamming distance <= max_hd
        '''
        min_hd = 15
        for word in dict_words:
            hd = sum(1 for i, r in zip(wli, runes) if word[i[0]] != r)
            if hd == 0:
                return 0
            if hd < min_hd:
                min_hd = hd
        return min_hd

    def find_min_HD(self, runes_index, wli_data, max_hd = 1):
        '''
        :param runes_index: list of rune-index values
        :param wli_data: list of pairs: [index-in-word, word-length]
        :param max_hd: the maximum HD allowed, otherwise return early
        :return: hamming distance
        '''
        runesword,wliwords = self.create_word_data(runes_index, wli_data)
        total_hd = 0
        spare_hd = max_hd - total_hd
        for r,w in zip(runesword,wliwords):
            # (item[1][0][1] - 1) is (wordlength-1) to get correct part of __all_words_index list

            #rot_ptnp = np.asarray(r, dtype=np.int64)
            dict_words = WordModel.__all_words_index[w[0][1] - 1]
            #spare_hd += self.hamming_distance_pos(dict_words, r, w, spare_hd)
            spare_hd += nm.hamming_distance_pos_C(dict_words, r, w, spare_hd)
            # dict_words = WordModel.__all_words_index_np[w[0][1] - 1]
            # spare_hd += nm.hamming_distance_pos_Cnp(dict_words, np.asarray(r, dtype=np.int64), w, spare_hd)
            if spare_hd > max_hd:
                break
        return spare_hd