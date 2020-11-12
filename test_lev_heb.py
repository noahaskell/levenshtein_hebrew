import lev_heb as lh


def test_read_word_list():
    word_dict = lh.read_word_list('example_word_list.csv')
    assert word_dict['Prime'][0] == 'העללה', 'First Prime incorrect.'
    assert word_dict['Prime'][-1] == 'כופתר', 'Last Prime incorrect.'
    assert word_dict['Target'][0] == 'עצמאות', 'First Target incorrect.'
    assert word_dict['Target'][-1] == 'השיט', 'Last Target incorrect.'
    assert word_dict['other'][0][0] == 'Extra', 'First other item incorrect.'
    assert word_dict['other'][0][1] == 'Again', 'First other item incorrect.'
    assert word_dict['other'][-1][0] == 'other', 'Last other item incorrect.'
    assert word_dict['other'][-1][1] == 'code', 'Last other item incorrect.'


def test_read_lexicon():
    base = lh.read_lexicon('base_lexicon.csv')
    assert base[0] == 'העללה', "First base lexical item incorrect."
    assert base[-1] == 'לחינם', "Last base lexical item incorrect."


def test_calculate_oldN():
    wrd = ['hey', 'man']
    lex = ['hex', 'ray', 'map', 'cab']
    wd = {'wrd': wrd.copy()}
    out_dict = lh.calculate_oldN(wd, ("wrd",), lex, N=2)
    out_list = out_dict["wrd"]
    assert out_list[0][0] == wrd[0], "First word in list incorrect."
    assert out_list[0][1] == 1.5, "OLD2 for 'hey' incorrect."
    assert out_list[1][0] == wrd[1], "Second word in list incorrect."
    assert out_list[1][1] == 1.5, "OLD2 for 'man' incorrect."


def test_line_format():
    test_tup = ("hey", 1.5, "prime")
    line = lh.line_format(test_tup)
    assert line == "hey,1.5,prime\n", "line incorrectly formatted"


def test_write_word_stats():
    wrd = ['hey', 'man']
    non = ['woz', 'zow']
    lex = ['hex', 'ray', 'map', 'cab']
    wd = {'wrd': wrd.copy(),
          'non': non.copy(),
          'other': [['g', 'h'], ['x', 'y'], ['w', 'z']]}
    out_dict = lh.calculate_oldN(wd, ("wrd", "non"), lex, N=2)
    test_fname = 'test_old2.csv'
    lh.write_word_stats(out_dict, fname=test_fname)
    with open(test_fname, 'r') as f:
        for i, line in enumerate(f):
            string = line.strip('\n')
            if i == 0:
                assert string == "wrd,wrd_oldN,non,non_oldN,g,h"
            elif i == 1:
                temp = [wrd[i-1], "1.5", non[i-1], "3.0", "x", "y"]
                assert string == ",".join(temp)
            elif i == 2:
                temp = [wrd[i-1], "1.5", non[i-1], "3.0", "w", "z"]
                assert string == ",".join(temp)
