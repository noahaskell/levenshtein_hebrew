import Levenshtein as lev

# architecture notes
# read in word list for which OLD20 stats are wanted
# read in lexicon (surface only? base? both? input spec'd?
# loop through words, calculate OLD20
# write to output file


def read_word_list(fname, cols=("Prime", "Target")):
    """
    Reads in csv with Prime and Target Hebrew words

    Parameters
    ----------
    fname : str
        filename containing word lists
    cols : tuple
        contains keys for output dict corresponding
        to columns in input

    Returns
    -------
    dict
        Dictionary with keys specified by cols input
        with lists containing associated words
    """
    words = {x: [] for x in cols}
    indices = {x: [] for x in cols}
    with open(fname, 'r') as f:
        for i, line in enumerate(f):
            vals = line.strip('\n')
            if i == 0:
                headers = vals.split(',')
                words['headers'] = headers
                all_idx = list(range(len(headers)))
                for c in cols:
                    this_idx = [j for j, h in enumerate(headers) if c in h][0]
                    indices[c] = this_idx
                    all_idx.remove(this_idx)
                words['other'] = []
            else:
                try:
                    word_list = vals.split(',')
                    for k in cols:
                        words[k].append(word_list[indices[k]])
                    ol = [w for j, w in enumerate(word_list) if j in all_idx]
                    words['other'].append(ol)
                except IndexError:
                    print("Tried to split, wasn't having it.")

    return words


def read_lexicon(fname="base_lexicon.csv"):
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


def add_word_type(oldN_list, word_type):
    """
    Adds word type to list of tuples

    Parameters
    ----------
    oldN_list : list of tuples
        tuples contain word, oldN pairs, returned by calculate_oldN()
    word_type : {'prime', 'target'}
        string indicating which type of word each word is

    Returns
    -------
    list of tuples
        tuples contain word, oldN, type triplets
    """
    headers = oldN_list[0]
    headers += ("type",)
    new_list = [headers]
    for wo in oldN_list[1:]:
        wo += (word_type,)
        new_list.append(wo)
    return new_list


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
    headers = [line_format(word_list[0])]
    str_l = [line_format(x) for x in word_list[1:]]
    str_list = headers + str_l
    with open(fname, 'w') as f:
        f.writelines(str_list)


def line_format(oldN_tuple):
    """
    Formats tupes for writing

    Parameters
    ----------
    oldN_tuple : tuple
        contains word, oldN, type triplet

    Returns
    -------
    str
        formatted for writing to csv, ends with \n
    """
    ot = oldN_tuple
    if isinstance(ot[1], str):
        out = ",".join(ot) + "\n"
    elif isinstance(ot[1], float):
        out = ot[0] + "," + str(round(ot[1], 3)) + "," + ot[2] + "\n"
    return out


if __name__ == "__main__":
    # some word lists: ["concrete", "fillers", "nonwords"]
    # columns: [("Prime", "Target")]*3
    all_word_lists = ["Frostetal1997_roots"]
    columns = [("Heb",)]
    lex = ["surface"]  # ["base"]
    N = 20
    for this_lex in lex:
        lexicon = read_lexicon(this_lex + "_lexicon.csv")
        for wl, cols in zip(all_word_lists, columns):
            word_dict = read_word_list(wl + '.csv', cols=cols)
            for word_type, word_list in word_dict.items():
                oldN_list = calculate_oldN(word_list, lexicon, N=N)
                wot_list = add_word_type(oldN_list, word_type)
                oldN = "OLD" + str(N)
                out_fname = "_".join([wl, this_lex, oldN, word_type]) + ".csv"
                write_word_stats(wot_list, fname=out_fname)
