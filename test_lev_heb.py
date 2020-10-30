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
    assert out[0][1] == 1.5, "OLD2 for 'hey' incorrect."
    assert out[1][1] == 1.5, "OLD2 for 'man' incorrect."
