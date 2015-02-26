# coding: utf-8

import io
import string
from FE_Dict import FE_Dict
import nltk
from nltk.tag.stanford import POSTagger
from ngram_downloader import get_most_probable_bigram
import time

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
    st = POSTagger(r'stanford-postagger/models/french.tagger', r'stanford-postagger/stanford-postagger.jar', encoding="utf-8"    )
    # print "round"
    # print words
    tokens = st.tag(words)
    # print tokens
    last_word_type = ""
    last_word = ""
    post_order = tokens

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
    verbs = ["V", "VIMP", "VINF", "VPP", "VPR", "VS"]
    reflexive_pronouns = ['CLO']
    for i in range(1, len(post_order)):
        prev_word, prev_word_type = post_order[i-1]
        curr_word, curr_word_type = post_order[i]

        if (prev_word_type in reflexive_pronouns) and (curr_word_type in verbs):
            post_order[i] = (prev_word, prev_word_type)
            post_order[i-1] = (curr_word, curr_word_type)


    # print " ".join(post_order)
    words = [word for word, word_type in post_order]
    translation = translate_by_picking_best_bigrams(words, fe_dict)
    return " ".join(translation)
    # print "end"
    # tokens = nltk.word_tokenize(processed_sentence)
    # print tokens

def get_cross_product_bigrams(first_list, second_list):
    result = []
    for first_list_word in first_list:
        for second_list_word in second_list:
            result.append((first_list_word, second_list_word))
    return result

def translate_by_picking_best_bigrams(words, fe_dict):
    translation = words

    if len(words) == 0:
        return translation
    elif len(words) == 1:
        # Translate the only word and pick the best unigram.
        only_word = words[0]
        t = fe_dict.translate(only_word)
        translation.append(t[0])
        return translation
    # Otherwise, we have at least two words, and can use the regular procedure.
    else:
        for i in range(1, len(words)):
            # If we are looking at the first two words, go ahead and just find
            # out which translated bigram pair out of the possible translation
            # bigram pairs ranks the highest on Google's NGrams
            if (i == 1):
                # Create the list of bigrams as a list of tuples [(String, String)]
                first_word_translations = fe_dict.translate(words[i-1])
                second_word_translations = fe_dict.translate(words[i])
                bigrams = get_cross_product_bigrams(first_word_translations, second_word_translations)

                # Get the best bigram and use that
                best_first_word, best_second_word = get_most_probable_bigram(bigrams)
                translation[i-1] = best_first_word
                translation[i] = best_second_word
            else:
                prev_word = translation[i-1]
                current_word_translations = fe_dict.translate(words[i])
                bigrams = get_cross_product_bigrams([prev_word], current_word_translations)

                # Space out consecutive requests by 5 seconds to avoid getting
                # HTTP 429: Too Many Requests errors
                time.sleep(1.0)

                # 'prev_word' cannot possibly have changed from earlier since we passed
                # in a list of size one to the first argument for get_cross_product_bigrams
                prev_word, best_curr_word = get_most_probable_bigram(bigrams)
                translation[i] = best_curr_word

        return translation

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