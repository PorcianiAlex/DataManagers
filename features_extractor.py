import numpy as np
from textacy.doc import Doc
from textacy.corpus import Corpus
from textacy.text_stats import TextStats
from textacy.lexicon_methods import emotional_valence
from textacy.preprocess import preprocess_text
import random


def doc_creator(text):
    text = preprocess_text(text, fix_unicode=True, lowercase=True, no_numbers=True, no_punct=True,
                            no_contractions=True, no_accents=True)
    return Doc(text, lang="en_core_web_md")


def count_uppercase_words(txt):
    return sum(map(str.isupper, txt.split()))


def stats(doc):
    ts = TextStats(doc)
    try:
        n_words = ts.n_words
    except:
        n_words = random.randint(200, 1000)
    try:
        complexity = ts.flesch_kincaid_grade_level
    except:
        complexity = 0.5
    return (n_words, ts.n_sents, ts.n_chars, ts.n_unique_words, ts.n_long_words, complexity)


def em_extractor(doc):
    return emotional_valence(doc.tokens)


def extract_features(text):
    uc_words = count_uppercase_words(text)
    doc = doc_creator(text)
    st = stats(doc)
    emotions = em_extractor(doc)
    features = [uc_words / st[0], st[5], st[4] / st[0], st[3] / st[0], st[2], st[0], st[1],
                emotions['AFRAID'], emotions['AMUSED'], emotions['ANGRY'], emotions['ANNOYED'],
                emotions['DONT_CARE'], emotions['HAPPY'], emotions['INSPIRED'], emotions['SAD'],
                ]
    return features
