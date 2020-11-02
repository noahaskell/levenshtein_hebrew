import lev_heb as lh


def test_read_word_list():
    word_list = lh.read_word_list('example_word_list.csv')
    assert word_list['Prime'][0] == 'העללה', 'First Prime incorrect.'
    assert word_list['Prime'][-1] == 'כופתר', 'Last Prime incorrect.'
    assert word_list['Target'][0] == 'עצמאות', 'First Target incorrect.'
    assert word_list['Target'][-1] == 'השיט', 'Last Target incorrect.'


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


def test_write_word_stats():
    wrd = ['hey', 'man']
    lex = ['hex', 'ray', 'map', 'cab']
    out = lh.calculate_oldN(wrd, lex, N=2)
    test_fname = 'test_old2.csv'
    lh.write_word_stats(out, fname=test_fname)
    with open(test_fname, 'r') as f:
        for i, line in enumerate(f):
            string = line.strip('\n')
            if i == 0:
                assert string == "word, old2"
            else:
                assert string == wrd[i-1] + ", " + str(1.5)
