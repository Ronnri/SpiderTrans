# encoding: utf-8 
from GoogleFreeTrans import Translator
from pytest import raises


def test_translation():
    en = 'china'
    fr = 'chine'
    translator = Translator.translator(src='en', dest='fr')
    out = translator.translate(en)
    print(out)
    assert out.lower() == fr


def test_mutil_sent_trans():
    en = 'hello. china.'
    translator = Translator.translator(src='en', dest='fr')
    rep = translator.translate('hello. china.', multi=True)
    print(rep)
    assert rep[0][0].lower() == 'bonjour. '
    assert rep[1][0].lower() == 'chine.'


def test_unicode():
    translator = Translator.translator(src='ko', dest='ja')
    result = translator.translate('안녕하세요.')
    print(result)
    assert result == u'こんにちは。'


def test_special_chars():
    text = u"©×《》"
    translator = Translator.translator(src='en', dest='en')
    rep = translator.translate(text)
    print(rep)
    assert rep == text
