# coding: utf-8

import io
from FE_Dict import FE_Dict

def main():
    fe_dict = FE_Dict()

    with io.open("sentences.txt", 'r', encoding="utf-8") as f:
        for line in f:
            line = line.lower()
            line = line.replace(u'’', 'e ')
            line = line.replace('\'', 'e ')

            words = line.split(' ')
            translation = []
            for word in words:
                print word
                print fe_dict.translate(word)

            # print " ".join(translation)

if __name__ == '__main__':
	main()