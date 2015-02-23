# coding: utf-8

import io
from FE_Dict import FE_Dict

def main():
    fe_dict = FE_Dict()

    with io.open("sentences.txt", 'r', encoding="utf-8") as f:
        for line in f:
            line = line.replace(u'’', 'e ')
            line = line.replace('\'', 'e ')

            print fe_dict.translate("des")
            print line

if __name__ == '__main__':
	main()