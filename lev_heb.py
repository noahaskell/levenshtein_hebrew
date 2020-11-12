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
        also 'headers' and 'other' keys for writing full results
        to mimic original file with added OLDN column(s)
    """
    words = {x: [] for x in cols}
    indices = {x: [] for x in cols}
    with open(fname, 'r') as f:
        for i, line in enumerate(f):
            vals = line.strip('\n')
            if i == 0:
                headers = vals.split(',')
                all_idx = list(range(len(headers)))
                for c in cols:
                    this_idx = [j for j, h in enumerate(headers) if c in h][0]
                    indices[c] = this_idx
                    all_idx.remove(this_idx)
                words['other'] = [[headers[j] for j in all_idx]]
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


def calculate_oldN(word_dict, cols, lexicon, N=20):
    """
    Calculates OLDN for the words in targets using the words in lexicon
    OLDN = mean orthographic Levenshtein distance for the N nearest neighbors

    Parameters
    ----------
    word_dict: dict
        dictionary of the type returned by read_word_list()
    cols : tuple or list
        contains keys for accessing words lists for which OLDN stats are wanted
    lexicon : list
        list of words for which Levenshtein distance will be calculated
    N : int
        the number of closest neighbors for which to calculate and average OLD

    Returns
    -------
    word_dict : dict
        internal word lists modified in place to include OLDN stats
    """
    for col in cols:
        for idx, word in enumerate(word_dict[col]):
            old_t = []
            for neighbor in lexicon:
                ld = lev.distance(word, neighbor)
                if ld != 0:
                    old_t.append(ld)
            closest = sorted(old_t)[:N]
            oldN = sum(closest)/N
            word_dict[col][idx] = (word, oldN)
    return word_dict


def write_word_stats(word_dict, fname='oldN.csv'):
    """
    Writes words and OLDN stats to csv

    Parameters
    ----------
    word_dict : dict
        output from calculate_oldN() or read_word_list()
    fname : str
        filename for opening and writing word, oldN pairs
    """
    head_t = list(word_dict.keys())
    head_t.remove('other')
    head_a = []
    for h in head_t:
        head_a.append(h)
        head_a.append(h + '_oldN')
    head_b = word_dict['other'][0]
    headers = head_a + head_b
    lenny = len(word_dict['other'])-1
    str_list = [line_format(headers)]
    for i in range(lenny):
        str_t = []
        for h in head_t:
            tup_t = word_dict[h][i]
            str_t.append(tup_t[0])
            str_t.append(tup_t[1])
        str_u = [x for x in word_dict['other'][i+1]]
        str_l = str_t + str_u
        str_list.append(line_format(str_l))
    with open(fname, 'w') as f:
        f.writelines(str_list)


def line_format(out_tuple):
    """
    Formats tuples for writing

    Parameters
    ----------
    out_tuple : tuple
        contains original row info plus OLDN values

    Returns
    -------
    str
        formatted for writing to csv, ends with \n
    """
    ol = [o if isinstance(o, str) else str(round(o, 3)) for o in out_tuple]
    out = ",".join(ol) + "\n"
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
