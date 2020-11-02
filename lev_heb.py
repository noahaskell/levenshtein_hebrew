import Levenshtein as lev

# architecture notes
# read in word list for which OLD20 stats are wanted
# read in lexicon (surface only? base? both? input spec'd?
# loop through words, calculate OLD20
# write to output file


def read_word_list(fname):
    """
    Reads in csv with Prime and Target Hebrew words

    Parameters
    ----------
    fname : str
        filename containing word lists
        Primes in first column, Targets in second column

    Returns
    -------
    dict
        Dictionary with keys 'Prime' and 'Target'
        with lists containing associated words
    """
    words = {'Prime': [], 'Target': []}
    with open(fname, 'r') as f:
        for i, line in enumerate(f):
            if i != 0:
                vals = line.strip('\n')
                try:
                    p, t = vals.split(',')
                    words['Prime'].append(p)
                    words['Target'].append(t)
                except IndexError:
                    print("Tried to split, wasn't having it.")

    return words


def read_lexicon(fname):
    """
    Reads in lexicon of Hebrew word forms.

    Parameters
    ----------
    fname : {'base_lexicon.csv', 'surface_lexicon.csv'}
        filename for lexicon

    Returns
    -------
    list
        list of words in the lexicon
    """
    words = []
    with open(fname, 'r') as f:
        for line in f:
            words.append(line.strip('\n'))
    return words


def calculate_oldN(targets, lexicon, N=20):
    """
    Calculates OLDN for the words in targets using the words in lexicon
    OLDN = mean orthographic Levenshtein distance for the N nearest neighbors

    Parameters
    ----------
    targets : list
        list of target words (strings) for with OLDN is desired
    lexicon : list
        list of words for which Levenshtein distance will be calculated
    N : int
        the number of closest neighbors for which to calculate and average OLD

    Returns
    -------
    list
        list with tuple elements containing word-OLDN pairs
    """
    oldN_list = [("word", "old" + str(N))]
    for word in targets:
        old_t = []
        for neighbor in lexicon:
            ld = lev.distance(word, neighbor)
            if ld != 0:
                old_t.append(ld)
        closest = sorted(old_t)[:N]
        oldN = sum(closest)/N
        oldN_list.append((word, oldN))
    return oldN_list


def write_word_stats(word_list, fname='oldN.csv'):
    """
    Writes words and OLDN stats to csv

    Parameters
    ----------
    word_list : list of tuples
        tuples contain word, OLDN pairs, returned by calculate_oldN()
    fname : str
        filename for opening and writing word, oldN pairs
    """
    headers = [word_list[0][0] + ", " + word_list[0][1] + "\n"]
    str_l = [x[0] + ", " + str(round(x[1], 3)) + "\n" for x in word_list[1:]]
    str_list = headers + str_l
    with open(fname, 'w') as f:
        f.writelines(str_list)
