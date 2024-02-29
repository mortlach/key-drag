'''
#!/usr/bin/env python3
# simple gematria encoding
# thanks to 'solvers, and bb who started this many years ago
'''
# my canonical definitions
__rune_position = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22,
                   23, 24, 25, 26, 27, 28]
__runes = ["ᚠ", "ᚢ", "ᚦ", "ᚩ", "ᚱ", "ᚳ", "ᚷ", "ᚹ", "ᚻ", "ᚾ", "ᛁ", "ᛂ", "ᛇ", "ᛈ", "ᛉ", "ᛋ", "ᛏ",
           "ᛒ", "ᛖ", "ᛗ", "ᛚ", "ᛝ", "ᛟ", "ᛞ", "ᚪ", "ᚫ", "ᚣ", "ᛡ", "ᛠ"]
__latin_canon = ["F", "U", "TH", "O", "R", "C", "G", "W", "H", "N", "I", "J", "EO", "P", "X", "S",
                 "T", "B", "E", "M", "L", "(I)NG", "OE", "D", "A", "AE", "Y", "IO", "EA"]

# rune to position (index) in gematria
__rune2position_dict = {r: p for r, p in zip(__runes, __rune_position)}
# oddities
__rune2position_dict["ᛄ"] = __rune2position_dict["ᛂ"]
#  rune to latin
__rune2latin_dict = {r: l for r, l in zip(__runes, __latin_canon)}
# oddities
__rune2latin_dict["ᛄ"] = __rune2latin_dict["ᛂ"]
# latin to position
__latin2position_dict = {l: p for l, p in zip(__latin_canon, __rune_position)}
__latin2position_dict['ING'] = __latin2position_dict["(I)NG"]
__latin2position_dict['NG'] = __latin2position_dict["(I)NG"]
__latin2position_dict['Z'] = __latin2position_dict["S"]
__latin2position_dict['K'] = __latin2position_dict["C"]
__latin2position_dict['IA'] = __latin2position_dict["IO"]
__latin2position_dict['Q'] = __latin2position_dict["K"]
# latin to rune
__latin2rune_dict = {l: r for l, r in zip(__latin_canon, __runes)}
__latin2rune_dict['ING'] = __latin2rune_dict["(I)NG"]
__latin2rune_dict['NG'] = __latin2rune_dict["(I)NG"]
__latin2rune_dict['Z'] = __latin2rune_dict["S"]
__latin2rune_dict['K'] = __latin2rune_dict["C"]
__latin2rune_dict['IA'] = __latin2rune_dict["IO"]
__latin2rune_dict['Q'] = __latin2rune_dict["K"]
# position to rune / latin, always canonical - no oddities
__position2rune_dict = {p: r for p, r in zip(__rune_position, __runes)}
__position2latin_dict = {p: l for p, l in zip(__rune_position, __latin_canon)}


# as functions
def latin2rune(c):
    return __latin2rune_dict.get(c, c)


def latin2position(c):
    return __latin2position_dict.get(c, c)


def position2rune(c):
    return __position2rune_dict.get(c, c)


def position2latincanon(c):
    return __position2latin_dict.get(c, c)


def rune2latincanon(c):
    return __rune2latin_dict.get(c, c)


def rune2position(c):
    return __rune2position_dict.get(c, c)


BIGRM = ['TH', 'EO', 'NG', 'OE', 'AE', 'IA', 'IO', 'EA']
TRGRAM = 'ING'


def translate_to_gematria(word):
    '''
        convert word standard english to runes (Latin)
    '''
    res = []
    skip = 0
    WORD = word.upper().replace("QU", "KW")
    WORD = WORD.replace("Q", "K")
    for i, val in enumerate(WORD):
        if skip:
            skip -= 1
            continue
        if WORD[i:i + 3] == TRGRAM:
            res.append(TRGRAM)
            skip += 2
            continue
        if WORD[i:i + 2] in BIGRM:
            res.append(WORD[i:i + 2])
            skip += 1
            continue
        if WORD[i] == '\'':
            res.append('\'')
            continue
        if WORD[i] == '"':
            res.append('"')
            continue
        res.append(val)
    return ''.join([latin2rune(r) for r in res])
