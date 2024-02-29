'''
    these decrypters should be able to solve 3 sections so test wwe can
'''

import time
import random
import src_py.gematria as gem
import src_py.cryption_methods_of_2_variables as cry
import src_py.key_drag as key_drag
import src_py.ngram_model as ngmod
import src_py.word_model as wmod


def get_welcompilgrim_data():
    # Decryption Attempts, need Cipher Text With word length info  and Key_guesses
    decrypt_data = {}
    decrypt_data['decrypt_functions'] = [cry.decrypt_p_plus_k_to_p]
    decrypt_data['c_and_k_directions'], decrypt_data['c_and_k_rotations'] = cry.get_gematria_options_for_method(
        decrypt_data["decrypt_functions"][0])
    decrypt_data['interrupters'] = list({None, gem.latin2position("F"),gem.latin2position("W"),gem.latin2position("G")})
    decrypt_data['transpositions'] = ['L2R']
    decrypt_data['c_and_k_directions'] = [["normal", 'atbash'], ["normal", 'normal']]

    decrypt_data['c_runes_string'] = "ᚢᛠᛝᛋᛇᚠᚳ ᚱᛇᚢᚷᛈᛠᛠ ᚠᚹᛉᛏᚳᛚᛠ ᚣᛗ ᛠᛇ ᛏᚳᚾᚫ ᛝᛗᛡᛡᛗᛗᚹ ᚫᛈᛞᛝᛡᚱ ᚩᛠ ᛡᛗᛁ ᚠᚠ ᛖᚢᛝ ᛇᚢᚫ \
                    ᚣᛈ ᚱᚫ ᛁᛈᚫ ᚳᚫ ᚫᚾᚹ ᛒᛉᛗᛞ ᚱᛡᛁ ᚠᛈᚳ ᛇᛇᚫᚳ ᚱᚦᛈ ᚠᛂᛗᚩ ᛇᚳᚹᛡ ᛒᚫᚹ ᛒᛠᛚᛋ ᚱᚣ ᛂᚫ ᚱ \
                    ᛗᚳᚦᛇᚫᛏᚳᛈᚹ ᛗᚷᛇ ᚳᛝᛈᚢ ᛇᚳ ᚱᛖᚹ ᛡᛈᛁ ᛒᚣᛒᛉ ᚠᛚᛁᚱ ᚱᛗ ᚳᚷᛒ ᚣᚱ ᚳᚠᚢ ᚦᛈᛡᛂᚹᛏᚠᛠ ᛂᚷᛒ \
                    ᚫᚦᚠᚠᛠᛈᚦ ᛈᚠᚪᛉ ᛂᛗᛖᛈᛝᛋᚩᛋᛗ ᚹᛇᛂᛚ ᚹᛉᚢᚦᚫᚹᛗᚦ ᛞᚣᛂᚳ ᛋᛡᛉᚩᛝᚱᛗᛒᚹ ᚱᛗᛁ ᛞᚣᛂᚳ ᛉᚻᚢᚣᛈᛚ \
                    ᛂᛝᚣᛗᚠᛂᛈᛇᚢᛡ ᚹᛇᛂ ᛞᚹᛉᚢ ᚪᛚᚪᛋᛗᛡᛇᛉ ᚫᛗ ᛡᛗᛁ ᛈᚣ ᚫᛗᚢᚠ ᛗᚣ ᚣᛇ ᚫᛉᚱᛂᛋᛖ ᛖᚹᚾ \
                    ᛞᛂᚢᛋᛉᚣᛏᛖᛏᛗ ᛇᚱᚣ ᛞᛋ ᚾᛖᚫᛞᛡ ᛈᛒᚢᚾᛠᛝᛂᛡᚫ ᛂᚷᛒ ᛈᚦᛉ ᛈᚾᚹᚹᛁᛚᛗᚫ ᛚᛈᛒᚢᚩᛠᛡ ᚱᛡᛠᚠ ᚱᚱᛇᛂᛗ \
                    ᚱᛗᛁ ᛞᚣᛂ ᚻᛚᚠᚢ ᛂᚢᛡᛚᚦᛠ ᛇᛂᚩᛇᚱᚱᛗ ᚢᛗᛋᚳ ᛠᛇ ᛚᛁᚫᚫᚳᛚ ᚹᛁ ᛚᛏ ᛈᛖᚢᛈ ᛠᛡᛈᚦᛏᛒ ᛏᛗᛖ \
                    ᚢᛚᚩᛚᛖ ᛇᛂᛈ ᚢᛠ ᛚᚳᚷ ᛠᚷᛋᛡᛏᛗ ᛒᛗᚱᚦᚠᛈ ᚹᚱᛂ ᚱᛉᚳ ᛝ ᛂᛠᛟ ᛂᛖᚣᛗ ᛞᚣᛂᚳᚫᛡᚢᚠ ᛈᚠᚪ ᚳᚳᛠ ᚱ \
                    ᚢᛂᚱ ᚪᛗᛒᛈ ᚷᛈᛒᚢᚾᛠᛝᚠ ᚾᛉᛖ ᚣᚷᛁᛠᛝᚢᛗᛏᚳᚷᛠᛠ ᛂᚫ ᛒᛈᚹᛞ ᚠᚣᛉ ᚫᚢᚠ ᛇᛂᛈ ᛉᛚᚦᛠᚪ ᛚᚦ ᚳᚣᚢᛡ \
                    ᚳᛖ ᛚᚫᛇᛁᛉᚦᛋᚫᚻᚫ ᚦᚣᚠᛚᚳᛖᚱ ᛈᚠᚪᛉ ᚱᛒᛖ ᚫᚳᛒᚠ"

    decrypt_data["c_runewords"] = decrypt_data['c_runes_string'].split()
    decrypt_data['c_index'] = [gem.rune2position(x) for x in list(decrypt_data['c_runes_string']) if x != ' ']
    # this odditiy is used to check if we get a valid plaintext
    decrypt_data['c_index_str'] = ''.join(str(i) for i in decrypt_data['c_index'])
    decrypt_data['c_latin'] = [gem.rune2latincanon(x) for x in list(decrypt_data['c_runes_string']) if x != ' ']
    decrypt_data['c_runes'] = [x for x in list(decrypt_data['c_runes_string']) if x != ' ']
    decrypt_data['wli'] = []
    [[decrypt_data['wli'].append([i, len(word)]) for i, x in enumerate(word)] for word in
     decrypt_data['c_runewords']]
    # key is divinity
    decrypt_data['key_guess'] = [23, 10, 1, 10, 9, 10, 16, 26]

    decrypt_data['p_runes_string'] = "ᚹᛖᛚᚳᚩᛗᛖ ᚹᛖᛚᚳᚩᛗᛖ ᛈᛁᛚᚷᚱᛁᛗ ᛏᚩ ᚦᛖ ᚷᚱᛠᛏ ᛂᚩᚢᚱᚾᛖᚣ ᛏᚩᚹᚪᚱᛞ ᚦᛖ ᛖᚾᛞ ᚩᚠ ᚪᛚᛚ ᚦᛝᛋ \
                                ᛁᛏ ᛁᛋ ᚾᚩᛏ ᚪᚾ ᛠᛋᚣ ᛏᚱᛁᛈ ᛒᚢᛏ ᚠᚩᚱ ᚦᚩᛋᛖ ᚹᚻᚩ ᚠᛁᚾᛞ ᚦᛖᛁᚱ ᚹᚪᚣ ᚻᛖᚱᛖ ᛁᛏ ᛁᛋ ᚪ \
                                ᚾᛖᚳᛖᛋᛋᚪᚱᚣ ᚩᚾᛖ ᚪᛚᚩᛝ ᚦᛖ ᚹᚪᚣ ᚣᚩᚢ ᚹᛁᛚᛚ ᚠᛁᚾᛞ ᚪᚾ ᛖᚾᛞ ᛏᚩ ᚪᛚᛚ ᛋᛏᚱᚢᚷᚷᛚᛖ ᚪᚾᛞ \
                                ᛋᚢᚠᚠᛖᚱᛝ ᚣᚩᚢᚱ ᛁᚾᚾᚩᚳᛖᚾᚳᛖ ᚣᚩᚢᚱ ᛁᛚᛚᚢᛋᛡᚾᛋ ᚣᚩᚢᚱ ᚳᛖᚱᛏᚪᛁᚾᛏᚣ ᚪᚾᛞ ᚣᚩᚢᚱ ᚱᛠᛚᛁᛏᚣ \
                                ᚢᛚᛏᛁᛗᚪᛏᛖᛚᚣ ᚣᚩᚢ ᚹᛁᛚᛚ ᛞᛁᛋᚳᚩᚢᛖᚱ ᚪᚾ ᛖᚾᛞ ᛏᚩ ᛋᛖᛚᚠ ᛁᛏ ᛁᛋ ᚦᚱᚩᚢᚷᚻ ᚦᛁᛋ \
                                ᛈᛁᛚᚷᚱᛁᛗᚪᚷᛖ ᚦᚪᛏ ᚹᛖ ᛋᚻᚪᛈᛖ ᚩᚢᚱᛋᛖᛚᚢᛖᛋ ᚪᚾᛞ ᚩᚢᚱ ᚱᛠᛚᛁᛏᛁᛖᛋ ᛂᚩᚢᚱᚾᛖᚣ ᛞᛖᛖᛈ ᚹᛁᚦᛁᚾ \
                                ᚪᚾᛞ ᚣᚩᚢ ᚹᛁᛚᛚ ᚪᚱᚱᛁᚢᛖ ᚩᚢᛏᛋᛁᛞᛖ ᛚᛁᚳᛖ ᚦᛖ ᛁᚾᛋᛏᚪᚱ ᛁᛏ ᛁᛋ ᚩᚾᛚᚣ ᚦᚱᚩᚢᚷᚻ ᚷᚩᛝ \
                                ᚹᛁᚦᛁᚾ ᚦᚪᛏ ᚹᛖ ᛗᚪᚣ ᛖᛗᛖᚱᚷᛖ ᚹᛁᛞᛋᚩᛗ ᚣᚩᚢ ᚪᚱᛖ ᚪ ᛒᛖᛝ ᚢᚾᛏᚩ ᚣᚩᚢᚱᛋᛖᛚᚠ ᚣᚩᚢ ᚪᚱᛖ ᚪ \
                                ᛚᚪᚹ ᚢᚾᛏᚩ ᚣᚩᚢᚱᛋᛖᛚᚠ ᛠᚳᚻ ᛁᚾᛏᛖᛚᛚᛁᚷᛖᚾᚳᛖ ᛁᛋ ᚻᚩᛚᚣ ᚠᚩᚱ ᚪᛚᛚ ᚦᚪᛏ ᛚᛁᚢᛖᛋ ᛁᛋ ᚻᚩᛚᚣ \
                                ᚪᚾ ᛁᚾᛋᛏᚱᚢᚳᛏᛡᚾ ᚳᚩᛗᛗᚪᚾᛞ ᚣᚩᚢᚱ ᚩᚹᚾ ᛋᛖᛚᚠ"
    decrypt_data['p_index'] = [gem.rune2position(x) for x in list(decrypt_data['p_runes_string']) if x != ' ']
    # this odditiy is used to check if we get a valid plaintext
    decrypt_data['p_index_str'] = ''.join(str(i) for i in decrypt_data['p_index'])
    decrypt_data['p_latin'] = [gem.rune2latincanon(x) for x in list(decrypt_data['p_runes_string']) if x != ' ']
    decrypt_data['p_runes'] = [x for x in list(decrypt_data['p_runes_string']) if x != ' ']
    return decrypt_data


def get_anend_data():
    # Decryption Attempts, need Cipher Text With word length info  and Key_guesses
    decrypt_data = {}
    decrypt_data['decrypt_functions'] = [cry.decrypt_p_plus_k_to_p]
    decrypt_data['c_and_k_directions'], decrypt_data['c_and_k_rotations'] = cry.get_gematria_options_for_method(
        decrypt_data["decrypt_functions"][0])
    decrypt_data['interrupters'] = list({None, gem.latin2position("F")})
    decrypt_data['transpositions'] = ['L2R']
    decrypt_data['c_and_k_directions'] = [["normal", 'atbash'], ["normal", 'normal']]

    decrypt_data['c_runes_string'] = "ᚫᛂ ᛟᛋᚱ ᛗᚣᛚᚩᚻ ᚩᚫ ᚳᚦᚷᚹ ᚹᛚᚫ ᛉᚩᚪᛈ ᛗᛞᛞᚢᚷᚹ ᛚ ᛞᚾᚣᛂ ᚳᚠᛡ ᚫᛏᛈᛇᚪᚦ ᚳᚫ ᚳᛞ ᚠᚾ ᛡᛖ \
                                      ᚠᚾᚳᛝ ᚱᚠ ᚫᛁᚱᛞᛖ ᛋᚣᛂᛠᚢᛝᚹ ᛉᚩ ᛗᛠᚹᚠ ᚱᚷᛡ ᛝᚱᛒ ᚫᚾᚢᛋ"

    decrypt_data["c_runewords"] = decrypt_data['c_runes_string'].split()
    decrypt_data['c_index'] = [gem.rune2position(x) for x in list(decrypt_data['c_runes_string']) if x != ' ']
    # this odditiy is used to check if we get a valid plaintext
    decrypt_data['c_index_str'] = ''.join(str(i) for i in decrypt_data['c_index'])
    decrypt_data['c_latin'] = [gem.rune2latincanon(x) for x in list(decrypt_data['c_runes_string']) if x != ' ']
    decrypt_data['c_runes'] = [x for x in list(decrypt_data['c_runes_string']) if x != ' ']
    decrypt_data['wli'] = []
    [[decrypt_data['wli'].append([i, len(word)]) for i, x in enumerate(word)] for word in
     decrypt_data['c_runewords']]
    # key is divinity
    prime_key =[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, \
                67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, \
                139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, \
                223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, \
                293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, \
                383, 389, 397, 401, 409, 419, 421, 431, 433, 439]

    decrypt_data['key_guess'] = random.choice([prime_key[i:i+8] for i in range(len(prime_key)-8)])

    decrypt_data['p_runes_string'] = "ᚪᚾ ᛖᚾᛞ ᚹᛁᚦᛁᚾ ᚦᛖ ᛞᛖᛖᛈ ᚹᛖᛒ ᚦᛖᚱᛖ ᛖᛉᛁᛋᛏᛋ ᚪ ᛈᚪᚷᛖ ᚦᚪᛏ ᚻᚪᛋᚻᛖᛋ ᛏᚩ ᛁᛏ ᛁᛋ ᚦᛖ \
                                      ᛞᚢᛏᚣ ᚩᚠ ᛖᚢᛖᚱᚣ ᛈᛁᛚᚷᚱᛁᛗ ᛏᚩ ᛋᛖᛖᚳ ᚩᚢᛏ ᚦᛁᛋ ᛈᚪᚷᛖ"
    decrypt_data['p_index'] = [gem.rune2position(x) for x in list(decrypt_data['p_runes_string']) if x != ' ']
    # this odditiy is used to check if we get a valid plaintext
    decrypt_data['p_index_str'] = ''.join(str(i) for i in decrypt_data['p_index'])
    decrypt_data['p_latin'] = [gem.rune2latincanon(x) for x in list(decrypt_data['p_runes_string']) if x != ' ']
    decrypt_data['p_runes'] = [x for x in list(decrypt_data['p_runes_string']) if x != ' ']
    return decrypt_data


def get_akoan_data():
    # Decryption Attempts, need Cipher Text With word length info  and Key_guesses
    decrypt_data = {}
    decrypt_data['decrypt_functions'] = [cry.decrypt_p_plus_k_to_p]
    decrypt_data['c_and_k_directions'], decrypt_data['c_and_k_rotations'] = cry.get_gematria_options_for_method(
        decrypt_data["decrypt_functions"][0])
    decrypt_data['interrupters'] = list({None, gem.latin2position("F")})
    decrypt_data['transpositions'] = ['L2R']
    decrypt_data['c_and_k_directions'] = [["normal", 'atbash'], ["normal", 'normal']]

    decrypt_data['c_runes_string'] = "ᚪ ᛋᚹᚪᛁ ᛈᚢᛟᚫ ᛈ ᚠᛖᚱᛋᛈᛈ ᚦᛗ ᚾᚪᚱᛚᚹᛈ ᛖᚩᛈᚢᛠᛁᛁᚻᛞ ᛚᛟ ᛠ ᛂᛖ ᛠ ᛁᚫ ᚷᛖ ᚦᛟᛁᛞᛟ ᛝᚠ ᛂᛖ \
                                    ᛞᛁᛉᚾᚢᛚᚠᚻᚱᚹᛈᛞᛡ ᚻᚹ ᛋᚳᛉᛞ ᚻᛡᛖᛡ ᛠᚱᛉᛖᛇ ᛒᚹ ᛠ ᛋᛒᛚᛞᚹᛈᚳ ᚫᚩ ᚹᛉᛞᚪᚪᛂᛠ ᚹᚣᛠᚳ ᛂᚪᚳ \
                                    ᛗᚾᛈᛏ ᚩᚻ ᛗᛈᛗᚳᛡᚱ ᚱᚪᛚᛡ ᛁᛒ ᚠᛋ ᛈ ᚳᛝᛗᚳᚹ ᛁᛗᛗᛁᚪᚻ ᚣᛝᚳᛟ ᛒᛠᛇ ᛁ ᚱᚹᚾᛒ ᛡᚪᛗᛟ ᛈ ᛁᚩᛠᚳᛠ \
                                    ᛉᚾ ᛚᛏ ᚻᛒᛡ ᛚᛇᚢᚪᚻᚣ ᚷᛖ ᛏᚷᚢᛇᛟᛡᚫ ᚪᛡᛞ ᛖᛟ ᚱᚫᚠᛋᚹᛡ ᚣᛗᛋ ᚣᚪᛗᛡ ᛏᚱ ᚷᛖᚾᚪ ᛚᛡ ᛗᛈᛋᚣᛟᚱ \
                                    ᚩᚻ ᛗᛈᛗᚳᛡᚱ ᚱᛏᛈᛒᛈᛗᛈ ᚦᚹ ᛗᚳᛁᛞᚹᚾᚣ ᛠᚾᚪ ᚳᚪᛠᛡ ᛚᛡ ᚢᛝᛁᛋᛟ ᚦᚫᚷ ᛂᛗᛗᚳ ᚪᚪᛠᛞ ᚹᚹᚢ ᚾᛉᚢᚹ \
                                    ᛈᛝ ᛁᚩᛠᚳᛠ ᛉᚾ ᛡᛟᚢᛟ ᛇᛒᚩ ᛁᚱ ᚦᛠ ᛉ ᚪᛁᛈ ᚦᚹ ᛗᚳᛁᛞᚹᚾᚣᛗ ᚹᛗᛞᛖ ᚹᛈᚾᛗᚷᚣᛏᛠᛈᛖᚪ"
    decrypt_data["c_runewords"] = decrypt_data['c_runes_string'].split()
    decrypt_data['c_index'] = [gem.rune2position(x) for x in list(decrypt_data['c_runes_string']) if x != ' ']
    # this odditiy is used to check if we get a valid plaintext
    decrypt_data['c_index_str'] = ''.join(str(i) for i in decrypt_data['c_index'])
    decrypt_data['c_latin'] = [gem.rune2latincanon(x) for x in list(decrypt_data['c_runes_string']) if x != ' ']
    decrypt_data['c_runes'] = [x for x in list(decrypt_data['c_runes_string']) if x != ' ']
    decrypt_data['wli'] = []
    [[decrypt_data['wli'].append([i, len(word)]) for i, x in enumerate(word)] for word in
     decrypt_data['c_runewords']]
    # key is firfumferenfe
    decrypt_data['key_guess'] = [0, 10, 4, 0, 1, 19, 0, 18, 4, 18, 9, 0, 18]

    decrypt_data['p_runes_string'] = "ᚪ ᚳᚩᚪᚾ ᛞᚢᚱᛝ ᚪ ᛚᛖᛋᛋᚩᚾ ᚦᛖ ᛗᚪᛋᛏᛖᚱ ᛖᛉᛈᛚᚪᛁᚾᛖᛞ ᚦᛖ ᛁ ᚦᛖ ᛁ ᛁᛋ ᚦᛖ ᚢᚩᛁᚳᛖ ᚩᚠ ᚦᛖ \
                                        ᚳᛁᚱᚳᚢᛗᚠᛖᚱᛖᚾᚳᛖ ᚻᛖ ᛋᚪᛁᛞ ᚹᚻᛖᚾ ᚪᛋᚳᛖᛞ ᛒᚣ ᚪ ᛋᛏᚢᛞᛖᚾᛏ ᛏᚩ ᛖᛉᛈᛚᚪᛁᚾ ᚹᚻᚪᛏ ᚦᚪᛏ \
                                        ᛗᛠᚾᛏ ᚦᛖ ᛗᚪᛋᛏᛖᚱ ᛋᚪᛁᛞ ᛁᛏ ᛁᛋ ᚪ ᚢᚩᛁᚳᛖ ᛁᚾᛋᛁᛞᛖ ᚣᚩᚢᚱ ᚻᛠᛞ ᛁ ᛞᚩᚾᛏ ᚻᚪᚢᛖ ᚪ ᚢᚩᛁᚳᛖ \
                                        ᛁᚾ ᛗᚣ ᚻᛠᛞ ᚦᚩᚢᚷᚻᛏ ᚦᛖ ᛋᛏᚢᛞᛖᚾᛏ ᚪᚾᛞ ᚻᛖ ᚱᚪᛁᛋᛖᛞ ᚻᛁᛋ ᚻᚪᚾᛞ ᛏᚩ ᛏᛖᛚᛚ ᚦᛖ ᛗᚪᛋᛏᛖᚱ \
                                        ᚦᛖ ᛗᚪᛋᛏᛖᚱ ᛋᛏᚩᛈᛈᛖᛞ ᚦᛖ ᛋᛏᚢᛞᛖᚾᛏ ᚪᚾᛞ ᛋᚪᛁᛞ ᚦᛖ ᚢᚩᛁᚳᛖ ᚦᚪᛏ ᛂᚢᛋᛏ ᛋᚪᛁᛞ ᚣᚩᚢ ᚻᚪᚢᛖ \
                                        ᚾᚩ ᚢᚩᛁᚳᛖ ᛁᚾ ᚣᚩᚢᚱ ᚻᛠᛞ ᛁᛋ ᚦᛖ ᛁ ᚪᚾᛞ ᚦᛖ ᛋᛏᚢᛞᛖᚾᛏᛋ ᚹᛖᚱᛖ ᛖᚾᛚᛁᚷᚻᛏᛖᚾᛖᛞ"
    decrypt_data['p_index'] = [gem.rune2position(x) for x in list(decrypt_data['p_runes_string']) if x != ' ']
    # this odditiy is used to check if we get a valid plaintext
    decrypt_data['p_index_str'] = ''.join(str(i) for i in decrypt_data['p_index'])
    decrypt_data['p_latin'] = [gem.rune2latincanon(x) for x in list(decrypt_data['p_runes_string']) if x != ' ']
    decrypt_data['p_runes'] = [x for x in list(decrypt_data['p_runes_string']) if x != ' ']
    return decrypt_data


def apply_key(decrypt_data, ans_data):
    # set up key-dragger
    kd = key_drag.KeyDrag()
    # what to do with errors? for now, exclude them (could treat as a form of interrupter, etc.)
    discard_errors = True
    [wlis, r] = kd.drag_key(ct=decrypt_data['c_index'], key=decrypt_data['key_guess'],
                                           wli=decrypt_data['wli'], interrupters=decrypt_data['interrupters'],
                                           transpositions=decrypt_data['transpositions'],
                                           c_and_k_directions=decrypt_data['c_and_k_directions'],
                                           c_and_k_rotations=decrypt_data['c_and_k_rotations'],
                                           decrypt_functions=decrypt_data['decrypt_functions'],
                                           discard_errors=discard_errors)
    #assert len(pts_with_opts) == len(wlis)
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
                result1 = lm1.get_distance_from_mean_w3w4(rot_pt, wli_at_this_index)
                all_neg = all([x > lm_threshold for x in result1])
                if all_neg:
                    # 2nd tets on word
                    result2 = lm2.find_min_HD(rot_pt, wli_at_this_index)
                    max_hd = 1
                    if result2 <= max_hd:
                        # a hit
                        this_pt_as_string = kd.get_as_runeglish_plaintext(this_pt=rot_pt, this_wli=wli_at_this_index)
                        if this_pt_as_string not in hit_dict:
                            datatosave = [this_pt_as_string, this_i, result1, these_opts]

                            rot_pt_s = ''.join(str(i) for i in rot_pt)
                            if rot_pt_s in ans_data:
                                #print(f'TRU HIT {this_pt_as_string}, {this_i}, {result1} {opts_for_this_pt}')
                                tru_hits += 1
                                datatosave.append(True)
                            else:
                                datatosave.append(False)
                            hit_dict[this_pt_as_string] = datatosave
                            hit_data.append(datatosave)


    return hit_data, total_attempts, tru_hits




if __name__ == "__main__":
    tload1 = time.time()

    lm1 = ngmod.NGramModel(True, True)
    lm2 = wmod.WordModel(True)
    print(f'Load time {time.time() - tload1} seconds')
    ts = time.time()
    print(f'\n******** WELCOME PILGRIM TEST *********')
    decrypt_data = get_welcompilgrim_data()
    for k,v in decrypt_data.items():
        print(k,v)
    hits, total_attempts, tru_hits = apply_key(decrypt_data, decrypt_data['p_index_str'])
    for item in hits:
        print(item)
    print([tru_hits, len(hits), total_attempts])
    if tru_hits > 0:
        print('SUCCESS welcome pilgrim passed')
    else:
        print('FAILURE welcome pilgrim failed')


    print(f'\n******** A KOAN TEST *********')
    decrypt_data = get_akoan_data()
    for k,v in decrypt_data.items():
        print(k,v)
    hits, total_attempts, tru_hits = apply_key(decrypt_data, decrypt_data['p_index_str'])
    for item in hits:
        print(item)
    print([tru_hits, len(hits), total_attempts])
    if tru_hits > 0:
        print('SUCCESS a koan passed')
    else:
        print('FAILURE a koan failed')

    print(f'\n******** AN END TEST *********')
    decrypt_data = get_anend_data()
    for k,v in decrypt_data.items():
        print(k,v)
    hits, total_attempts, tru_hits = apply_key(decrypt_data, decrypt_data['p_index_str'])
    for item in hits:
        print(item)
    print([tru_hits, len(hits), total_attempts])
    if tru_hits > 0:
        print('SUCCESS an end passed')
    else:
        print('FAILURE an end failed')

    print(f'FIN, run time {time.time() - ts} seconds')

    #signal_to_noise.append([tru_hits, len(hits), total_attempts])

