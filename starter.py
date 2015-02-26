# coding: utf-8

import io
import string
from FE_Dict import FE_Dict
import nltk
from nltk.tag.stanford import POSTagger

# I have already added environment variables as

# CLASSPATH = D:/stanford-postagger/stanford-postagger.jar
# STANFORD_MODELS =  D:/stanford-postagger/models/


def preprocess_words(sentence):
    # Convert apostrophes to 'e ', such that
    # L'enterprise  => Le enterprise
    # D'un          => De un
    sentence = sentence.replace(u'’', 'e ')
    sentence = sentence.replace('\'', 'e ')

    # Break words separated by a dash into two separate words
    sentence = sentence.replace('-', ' ')

    # Removing newlines/whitespace
    sentence = sentence.strip()

    # Remove all punctuation inside the sentence. We need to loop through the
    # characters of the string because this is a unicode string and we cannot
    # use the .translate() method on a unicode string.
    sentence = "".join([ch for ch in sentence if ch not in string.punctuation])
    return sentence.lower().split(' ')

def baseline_translate(sentence, fe_dict):
    words = preprocess_words(sentence)
    translation = []

    for word in words:
        t = fe_dict.translate(word)
        translation.append(t[0])

    return " ".join(translation)

def pos_order_strategy(sentence, fe_dict):
    words = preprocess_words(sentence)
    st = POSTagger(r'stanford-postagger/models/french.tagger',r'stanford-postagger/stanford-postagger.jar', encoding="utf-8"    )
    # print "round"
    # print words
    tokens = st.tag(words)
    # print tokens
    last_word_type = ""
    last_word = ""
    adjs = ['ADJ']
    nouns = ['NC','N']
    post_order = []
    for word, word_type in tokens:
        if last_word_type in nouns and word_type in adjs:
            post_order[-1] = word
            post_order.append(last_word)
        else:
            post_order.append(word)
        last_word_type = word_type
        last_word = word

    # print " ".join(post_order)
    translation = []
    for word in post_order:
        t = fe_dict.translate(word)
        translation.append(t[0])
    return " ".join(translation)
    # print "end"
    # tokens = nltk.word_tokenize(processed_sentence)
    # print tokens


def main():
    fe_dict = FE_Dict()

    with io.open("data/dev_set.txt", 'r', encoding="utf-8") as f:
        for line in f:
            baseline = baseline_translate(line, fe_dict)
            print baseline
            pos_translation = pos_order_strategy(line, fe_dict)
            print pos_translation

if __name__ == '__main__':
	main()