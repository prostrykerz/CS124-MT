# coding: utf-8

import io
import string
from FE_Dict import FE_Dict
import nltk
from nltk.tag.stanford import POSTagger
from ngram_downloader import get_ngram_probabilities
from pprint import pprint
import Pluralizer

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

def remove_se_strategy(words):
    new_words = []
    last_word = ""
    for i, w in enumerate(words):
        if w != "se" or last_word == "il" or last_word == "elle":
            new_words.append(w)
        last_word = w
    return new_words

def pos_order_strategy(sentence, fe_dict):
    words = preprocess_words(sentence)
    # print words
    words = remove_se_strategy(words)
    # print words

    st = POSTagger(r'stanford-postagger/models/french.tagger', r'stanford-postagger/stanford-postagger.jar', encoding="utf-8"    )
    # print "round"
    # print words
    tokens = st.tag(words)
    # print tokens
    # print tokens
    last_word_type = ""
    last_word = ""
    post_order = tokens
    # print post_order
    # Invert tokens if they show up in (NOUN, ADJ) order to be (ADJ, NOUN)
    adjs = ['ADJ']
    nouns = ['NC','N']
    for i in range(1, len(post_order)):
        prev_word, prev_word_type = post_order[i-1]
        curr_word, curr_word_type = post_order[i]

        if (prev_word_type in nouns) and (curr_word_type in adjs):
            post_order[i] = (prev_word, prev_word_type)
            post_order[i-1] = (curr_word, curr_word_type)

    # Invert tokens if they show up as (REFLEXIVE PRONOUN, VERB) to be
    # (VERB, REFLEXIVE PRONOUN)
    # print post_order
    verbs = ["V", "VIMP", "VINF", "VPP", "VPR", "VS"]
    reflexive_pronouns = ['CLO', 'CLR']
    for i in range(1, len(post_order)):
        prev_word, prev_word_type = post_order[i-1]
        curr_word, curr_word_type = post_order[i]

        if (prev_word_type in reflexive_pronouns) and (curr_word_type in verbs):
            post_order[i] = (prev_word, prev_word_type)
            post_order[i-1] = (curr_word, curr_word_type)


    # print " ".join(post_order)
    # print post_order

    translation = []
    for i, (word, word_type) in enumerate(post_order):
        t = fe_dict.translate(word)
        w_t = translateWithSelectGender(word, word_type, t, i, post_order)
        translation.append(w_t)

    fixed_translation = pLuRaLiZe_wOrDs(translation)

    new_translation = []
    for w in fixed_translation:
        new_translation.extend(w.split())
    # new_translation.extend([w.split() for w in fixed_translation])
    print new_translation

    return " ".join(get_rid_of_unnecessary_words(fixed_translation))
    # print "end"
    # tokens = nltk.word_tokenize(processed_sentence)
    # print tokens

def get_rid_of_unnecessary_words(translation):
    words_to_remove = ["the", "to", "a"] #, "to", "a"]

    # List to keep track of indexes where the word ['the', 'to', 'a'] appear, so that
    # we can remove them after.
    indexes_to_remove = []

    all_ngrams_to_examine = []
    for i in range(1, len(translation)-1):
        word = translation[i]
        if word in words_to_remove:
            prev_word = translation[i-1]
            next_word = translation[i+1]

            # Heuristic: usually, "to the" and "of the" should be left alone
            if (word == "to" and next_word == "the") or (word == "of" and next_word == "the"):
                continue

            # In case somewhere in the sentence we have something of the form
            # "A the B", compare the bigram probabilities of (A,B) with (the, B)
            # to determine whether or not we keep the word "the". This holds for the words "to" and "a" as well.
            ngrams = [(prev_word, next_word), (prev_word, word, next_word)]
            all_ngrams_to_examine.extend(ngrams)

    # This way, we can perform a batch request for all the ngrams so we reduce risk of HTTP 429 errors
    ngram_probabilities = get_ngram_probabilities(all_ngrams_to_examine)

    # Do the same loop again, but now that we have the ngram probabilities we can do our comparisons.
    for i in range(1, len(translation)-1):
        word = translation[i]
        if word in words_to_remove:
            prev_word = translation[i-1]
            next_word = translation[i+1]

            ngrams = [(prev_word, next_word), (prev_word, word, next_word)]
            # Two cases for where we should remove the middle word, 'word':
            #     a) Both ngrams are in the dictionary, and prob(prev_word, next_word) > prob(prev_word, word, next_word)
            #     b) Only the (prev_word, next_word) is in dictionary, meaning (prev_word, word, next_word) is never found (=> extremely rare)
            if ((ngrams[0] in ngram_probabilities) and (ngrams[1] in ngram_probabilities) and (ngram_probabilities[ngrams[0]] > ngram_probabilities[ngrams[1]])) or ((ngrams[0] in ngram_probabilities) and (ngrams[1] not in ngram_probabilities)):
                indexes_to_remove.append(i)


    # Get rid of the 'the' words in the list indexes_of_the_to_remove
    refined_translation = []
    for i in range(len(translation)):
        word = translation[i]
        if i not in indexes_to_remove:
            refined_translation.append(word)
    return refined_translation

def pLuRaLiZe_wOrDs(words):
    prevWord = ""
    prevWordType = ""
    nouns = ["NC"]
    verbs = ["V","VPR"]
    not_allowed_verbs = ["VINF","VIMP","VPP","VPR","VS","V"]
    st = POSTagger(r'stanford-postagger/models/english-bidirectional-distsim.tagger', r'stanford-postagger/stanford-postagger.jar', encoding="utf-8")
    ret = []
    # print words

    english_singular_nouns = ["NN"]
    for i, (w, wt) in enumerate(words):
        if wt in verbs and prevWordType in nouns:
            n = ""
            if i < len(words)-1:
                nw, nwt = words[i+1]
                if nwt not in not_allowed_verbs:
                    token = st.tag([prevWord])
                    n = token[0][1]
                    # print n
            else:
                token = st.tag([prevWord])
                n = token[0][1]

            if n!="" and n in english_singular_nouns:
                pluralized_verb = Pluralizer.pluralize(w)
                prevWord = w
                prevWordType = wt
                ret.append(pluralized_verb)
                continue
        prevWord = w
        prevWordType = wt
        ret.append(w)

    return ret

def translateWithSelectGender(word, word_type, translations, i, post_order):
    # print word
    if word == "se":
        if i >= 2:
            prevWord, prevWordType = post_order[i-2]
            if prevWord == "il":
                for t in translations:
                    if  t == "himself":
                        return (t, word_type)
            if prevWord == "elle":
                for t in translations:
                    if  t == "herself":
                        return (t, word_type)
    return (translations[0], word_type)

def main():
    fe_dict = FE_Dict()

    with io.open("data/dev_set.txt", 'r', encoding="utf-8") as f:
        for line in f:
            baseline = baseline_translate(line, fe_dict)
            # print baseline

            pos_translation = pos_order_strategy(line, fe_dict)
            print pos_translation + "\n"

if __name__ == '__main__':
    main()
