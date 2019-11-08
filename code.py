
#!/usr/bin/env python
# AnySubtitleDownloader.py

__copyright__ = "Copyright 2019"
__version__ = "1.0.1"
__github_repo__ = "https://github.com/jai-singhal/cldt"

# Import the essential libraries
import collections
from decimal import Decimal
import dill as pickle
import re
import sys

def tokenize(sentence):
    """
    Converts sentence to list of words:
    Args: sentence: str
    Returns list of words
    """
    consonants = "bcdfghjklmnpqrstvwxyz"
    # remove the punctuaations, just take the [a-zA-Z0-9]+ type of regex
    words=re.split(r'[` \t\-=~!@#$%^&*()_+\[\]{};\\\:"|<,./<>?,\n\']', sentence)
    output = list()
    for w in words:
        # remove the consonetnts if any
        if len(w) == 1 and w.lower() in list(consonants):
            continue
        if w in [''] and w.isdigit():
            continue
        w = w.strip()
        output.append(w.lower())
    return output

def getTranslations():
    """
    Get the translations from trained model, get the first translation with highest probability
    Args: None
    Returns Translations from english to dutch
    """
    print("Reading Translations.....")
    print("Reading the pickle time may takes time....")

    finalTranlationsOut = "translations.pickle"
    try:
        x = pickle.load(open(finalTranlationsOut, "rb"))
    except FileNotFoundError:
        print("File not found on appropriate location")
        filename = input("Input the finalTrained pickle file location: ")
        x = pickle.load(open(filename, "rb"))
    translations_prob = {}
    translations = {}
    for key, val in x.items():
        if key[0] in translations_prob:
            if translations_prob[key[0]] < val:
                translations_prob[key[0]] = val
                translations[key[0]] = key[1]
        else:
            translations_prob[key[0]] = val
            translations[key[0]] = key[1]
    return translations

def getCosineSimilarity(src, target):

    """
    Get the cosine similarity between 2 documents
    Cosine similarity from 0 to 1

    Args: Two strings of docs
    Returns cosine similarity : float(0, 1)
    """

    l1 =[];l2 =[] 
    # remove stop words from string 
    X_set = {w for w in src if len(w) > 0}  
    Y_set = {w for w in target if len(w) > 0} 

    # form a set containing keywords of both strings  
    rvector = X_set.union(Y_set)
    for w in rvector: 
        if w in X_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 
    c = 0

    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i]
    try:
        cosine = c / float((sum(l1)*sum(l2))**0.5)
        return cosine 
    except decimal.DivisionByZero:
        print("Zero error")
        return None

    
def getJacardCoeficient(src, target):

    """
    Get the Jacard coef between 2 documents
    Jacard coef ranges from 0 to 1
    Args: Two strings of docs
    Returns Jac Coef: float(0, 1)
    """
    d1 = {w for w in src if len(w) > 0}  
    d2 = {w for w in target if len(w) > 0} 
    d1ud2 = d1.union(d2)
    d1id2 = d1.intersection(d2)
    return float(len(d1id2))/len(d1ud2)


def run():
    """
    Driver code
    """

    print("Welcome to Cross Language Translations(English<-->Dutch)")
    averageJC_score = 0
    averageCS_score = 0
    total_tests = 0
    translations_e_d = getTranslations()
    translations_d_e = dict([(value, key) for key, value in translations_e_d.items()]) 

    while True:
        print("Which Translation you want?")
        print("1. ENGLISH TO DUTCH")
        print("2. DUTCH TO ENGLISH")
        ch = int(input("Please select the option: "))
        
        if ch == 1:
            translations = translations_e_d
        elif ch == 2:
            translations = translations_d_e
        else:
            print("Wrong Option Selected. Try again later")
            sys.exit()

        src_path = input("Enter source document path: ")
        trg_path = input("Enter target document path: ")
        try:
            src_file = open(src_path, 'r')
            src = src_file.read()
        except FileNotFoundError:
            print("Src file does not exists")
            print("Wrong Option Selected. Try again later")
            raise FileNotFoundError
            sys.exit()
        try:
            targ_file = open(trg_path, 'r')
            trg = targ_file.read()
        except:
            print("Destination file does not exists")
            print("Wrong Option Selected. Try again later")
            raise FileNotFoundError
            sys.exit()

        src_words = tokenize(src)
        trg_words = tokenize(trg)

        translated_wordlist = list()
        for w in src_words:
            if len(w) > 0 and w in translations.keys():
                translated_wordlist.append(translations[w])

        
        cs = getCosineSimilarity(trg_words, translated_wordlist)
        jc = getJacardCoeficient(trg_words, translated_wordlist)

        print("This document has cosine similarity: {}".format(cs))
        print("This document has Jacard similarity: {}".format(jc))

        
        translated_doc = " ".join(translated_wordlist)
        print("Ouputing your result into filename: translated_{}.txt".format(total_tests+1))
        with open("translated_{}.txt".format(total_tests+1), "w") as fout:
            fout.write(translated_doc)

        
        total_tests += 1
        averageCS_score += cs
        averageJC_score += jc

        print("Do you want to continue? ")
        ch = input("Please select the option(Y/N)?: ")

        if ch == 'Y' or ch == 'y':
            #normal exn
            print("Current Average cosine similarity: {}".format(averageCS_score/total_tests))
            print("Current Average Jacard similarity: {}".format(averageJC_score/total_tests))
            print("\n\n")
        elif ch == 'N' or ch == 'n':
            # print the average coefficent score
            print("Final Average cosine similarity: {}".format(averageCS_score/total_tests))
            print("Final Average Jacard similarity: {}".format(averageJC_score/total_tests))
            break
        else:
            print("Wrong Option Selected. Try again later")
            sys.exit()

if __name__ == "__main__":
    run()