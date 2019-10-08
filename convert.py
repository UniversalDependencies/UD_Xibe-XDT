#!usr/bin/python

import os
import re
from striprtf.striprtf import rtf_to_text


def wordFeatures(word):
    '''for given word, generate its features
        return a list, without wordid
    '''
    result = []
    features = ['lemma', 'upos', 'xpos',
                'feats', 'head', 'deprel', 'deps', 'misc']
    for feature in features:
        featValue = {}
        if feature == 'misc':
            featValue[feature] = 'Translit='
        else:
            featValue[feature] = "_"
        result.append(featValue[feature])
    result.insert(0, word)
    return result


# def sentSerialize(sentence):
#     sent = sentence.split(' ')
#     wordid = 1
#     sents = []
#     for word in sent:
#         wordFeature = wordFeatures(word)
#         wordFeature.insert(0, wordid)
#         wordid += 1
#         sents.append(wordFeature)
#     return sents

# convert rtf to txt
# entext = open('sent-en.rtf', encoding='utf-8').readlines()
# output = open('sent_en.txt', 'w')
# for line in entext:
#     text = rtf_to_text(line)
#     output.write(text+'\n')
# output.close()

def conlluConvert(en_text, xb_text, translit_text):
    "convert raw data to conllu format"
    filename = xb_text.split('.')
    enText = open(en_text, 'r').readlines()
    xbText = open(xb_text, 'r').readlines()
    translitText = open(translit_text, 'r').readlines()
    test = open(filename[0]+".conllu", 'w', encoding='utf-8')

    en_dict = {}
    for line in enText:
        line = re.split(r'[.?!]', line)
        if len(line) == 3:
            en_dict[line[0]] = line[1].strip()
    # print(len(en_dict))

    xb_dict = {}  # {index:[xb_sent, translit]}
    for line in xbText:
        line = re.split(r'[.]', line)
        xbTranslit = []
        if len(line) == 2:
            xbTranslit.append(line[1].strip())

        for lineTranslit in translitText:
            lineTranslit = re.split(r'[.]', lineTranslit.strip())

            if (len(lineTranslit) == 3 or len(lineTranslit) == 2) and lineTranslit[0] == line[0]:
                xbTranslit.append(lineTranslit[1].strip())
        # print(xbTranslit)
        xb_dict[line[0]] = xbTranslit
    # print(len(xb_dict))

    # translit_dict = {}
    # for line in translitText:
    #     line =
    #     if len(line) == 2:
    #         translit_dict[line[0]] = line[1].strip()

    sentPairs = {}
    for k_xb, v_xb in xb_dict.items():
        for k_en, v_en in en_dict.items():
            if k_en == k_xb:
                sentPair = []
                sentPair.append(v_xb)
                sentPair.append(v_en)
                sentPairs[k_en] = sentPair
    # print(sentPairs)
    for key, value in sentPairs.items():
        sentID = "# sent_id = " + filename[0]+"_"+key + "\n"
        test.write(sentID)
        sentXB = "# sent = " + value[0][0] + "\n"
        test.write(sentXB)
        sentTrans = "# sent[phon] = " + value[0][1] + "\n"
        test.write(sentTrans)
        sentEN = "# sent[eng] = " + value[1] + "\n"
        test.write(sentEN)

        sentence = value[0][0].strip().split(" ")
        wordID = 1

        for w in sentence:
            feats = wordFeatures(w)
            entry = '\t'.join(feats)
            entry = str(wordID) + '\t' + entry + '\n'
            wordID += 1
            test.write(entry)
        test.write('\n')
    test.close()
    print("Convert over!")


conlluConvert('grammarbook_en_p1.txt',
              'grammarbook_sjo_p1.txt', 'grammarbook_translit_p1.txt')
