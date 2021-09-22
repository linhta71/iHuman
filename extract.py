from nltk import tokenize
from operator import itemgetter
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import math
from medformal import *

def extract_main():
    meddict = {}
    medterms_vs_explain = mapping()
    for key in medterms_vs_explain:
        if (len(medterms_vs_explain[key])==2):
            medterms_vs_explain[key] = [medterms_vs_explain[key][1]]
    for key in medterms_vs_explain:
        key_words = extract_key_words(medterms_vs_explain[key][0]) 
        meddict[key] = key_words
    print("beta blockers: " + str(medterms_vs_explain["beta blockers"])) 
    print()
    print("beta blockers: " + str(meddict["beta blockers"])) 
    

    

def extract_key_words(sentence):
    stop_words = set(stopwords.words('english'))
    stop_words.add("a")
    stop_words.add("an")
    stop_words.add("the")
    stop_words.add("is")
    stop_words.add("and")
    stop_words.add("(")
    stop_words.add(")")
    totalWords = sentence.split()
    total_sentences = tokenize.sent_tokenize(sentence)
    tf_scores = calculate_TF_for_each_word(totalWords, stop_words)
    idf_scores = calculate_IDF(totalWords, stop_words, total_sentences)
    tf_idf_scores = {key: tf_scores[key] * idf_scores.get(key, 0) for key in tf_scores.keys()}
    key_words = get_top_n(tf_idf_scores, ((len(totalWords)*2)//3))
    return key_words.keys()

def calculate_TF_for_each_word(total_words, stop_words):
    tf_score = {}   
    for word in total_words:
        word = word.replace(".", "")
        if word.lower() not in stop_words:
            if word in tf_score:
                tf_score[word] += 1
            else:
                tf_score[word] = 1
        # take out the score 
    tf_score.update((x, y/int(len(total_words))) for x, y in tf_score.items())
    return tf_score

def check_words_in_sentence(word, sentences):
    final = [all([w in x for w in word]) for x in sentences] 
    sent_len = [sentences[i] for i in range(0, len(final)) if final[i]]
    return int(len(sent_len))

def calculate_IDF(total_words, stop_words, total_sentences):
    idf_score = {}
    for each_word in total_words:
        each_word = each_word.replace('.','')
        if each_word.lower() not in stop_words:
            if each_word in idf_score:
                idf_score[each_word] = check_words_in_sentence(each_word, total_sentences)
            else:
                idf_score[each_word] = 1

    # Performing a log and divide
    idf_score.update((x, math.log(int(len(total_sentences))/y)) for x, y in idf_score.items())
    return idf_score
def get_top_n(dict_elem, n):
    result = dict(sorted(dict_elem.items(), key = itemgetter(1), reverse = True)[:n]) 
    return result
def main():
    #print(extract_key_words("I am a graduate. I want to learn Python. I like learning Python. Python is easy. Python is interesting. Learning increases thinking. Everyone should invest time in learning"))
    print(extract_main())
main()