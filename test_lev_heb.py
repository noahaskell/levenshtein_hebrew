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
    out = lh.calculate_oldN(wrd, lex, N=2)
    assert out[0][0] == "word", "first header incorrect."
    assert out[0][1] == "old2", "second header incorrect."
    assert out[1][0] == wrd[0], "calculate_oldN didn't return correct words."
    assert out[1][1] == 1.5, "OLD2 for 'hey' incorrect."
    assert out[2][0] == wrd[1], "calculate_oldN didn't return correct words."
    assert out[2][1] == 1.5, "OLD2 for 'man' incorrect."


def test_add_word_type():
    wrd = ['hey', 'man']
    lex = ['hex', 'ray', 'map', 'cab']
    out = lh.calculate_oldN(wrd, lex, N=2)
    wot = lh.add_word_type(out, "prime")
    assert wot[0][0] == "word", "incorrect first header"
    assert wot[0][1] == "old2", "incorrect second header"
    assert wot[0][2] == "type", "incorrect third header"
    assert wot[1][0] == "hey", "incorrect first word"
    assert wot[1][1] == 1.5, "incorrect first old2"
    assert wot[1][2] == "prime", "incorrect first word type"
    assert wot[2][0] == "man", "incorrect first word"
    assert wot[2][1] == 1.5, "incorrect first old2"
    assert wot[2][2] == "prime", "incorrect first word type"


def test_line_format():
    test_tup = ("hey", 1.5, "prime")
    line = lh.line_format(test_tup)
    assert line == "hey,1.5,prime\n", "line incorrectly formatted"


def test_write_word_stats():
    wrd = ['hey', 'man']
    lex = ['hex', 'ray', 'map', 'cab']
    out = lh.calculate_oldN(wrd, lex, N=2)
    wot = lh.add_word_type(out, "prime")
    test_fname = 'test_old2.csv'
    lh.write_word_stats(wot, fname=test_fname)
    with open(test_fname, 'r') as f:
        for i, line in enumerate(f):
            string = line.strip('\n')
            if i == 0:
                assert string == "word, old2, type"
            else:
                assert string == wrd[i-1] + ", " + str(1.5) + ", " + "prime"
