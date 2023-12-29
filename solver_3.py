import numpy as np
from copy import*

ZERO_WORD=np.zeros(26)
alpha_dict={chr(ord('a')+i):i for i in range(26)}
inv_alpha_dict={i:chr(ord('a')+i) for i in range(26)}

def get_words(testing=True):
    if testing:
        words_all_fobj=open('words_alpha_test.txt') #this document has less words; used to test runtime
    else:
        words_all_fobj=open('words_alpha.txt')
    
    words_all=np.array(words_all_fobj.read().split())
    words_all_fobj.close()

    words=words_all[np.char.str_len(words_all)==5]

    return words

def remove_anagrams(words):
    existing_sorted_words=set()
    filtered_words=[]
    for word in words:
        sorted_word=''.join(sorted(word))
        if not sorted_word in existing_sorted_words:
            filtered_words.append(word)

    return np.array(filtered_words)

def remove_invalid_words(words):
    filtered_words=[]
    for word in words:
        letters=set()
        for c in word:
            letters.add(c)
        if len(letters)==5:
            filtered_words.append(word)

    global N_OF_WORDS
    N_OF_WORDS=len(filtered_words)
    return np.array(filtered_words)

def convert_to_np(words):
    words_np=np.zeros((N_OF_WORDS,26),dtype=int)
    for i,word in enumerate(words):
        word_vect=copy(ZERO_WORD)
        for c in word:
            word_vect[alpha_dict[c]]=1
        words_np[i]=word_vect

    return words_np

def check_unique_letters(word1,word2):
    return np.bitwise_and(word1,word2).sum()==0

def find_solutions(testing=True):
    words=remove_invalid_words(remove_anagrams(get_words(testing)))
    words_np=convert_to_np(words)

    print(N_OF_WORDS)

    list_of_solutions=[]

    for a,w1 in enumerate(words_np[:-4]):
        print(a)

        for b in range(N_OF_WORDS-3):
            if b<=a:
                b=a+1
                continue
            w2=words_np[b]
            if not check_unique_letters(w1,w2):
                continue
            w12=w1+w2

            for c in range(N_OF_WORDS-2):
                if c<=b:
                    c=b+1
                    continue
                w3=words_np[c]
                if not check_unique_letters(w12,w3):
                    continue
                w123=w12+w3

                for d in range(N_OF_WORDS-1):
                    if d<=c:
                        d=c+1
                        continue
                    w4=words_np[d]
                    if not check_unique_letters(w123,w4):
                        continue
                    w1234=w123+w4

                    for e in range(N_OF_WORDS):
                        if e<=d:
                            e=d+1
                            continue
                        w5=words_np[e]
                        if not check_unique_letters(w1234,w5):
                            continue
                        list_of_solutions.append({words[a],words[b],words[c],words[d],words[e]})

    return list_of_solutions