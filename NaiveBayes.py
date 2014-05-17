import collections
import math

def rev_data_dic(data_dic):
    inv_dic = {}
    for k, v in data_dic.iteritems():
        inv_dic[v] = inv_dic.get(v, [])
        inv_dic[v] += k
    return inv_dic

def count_words(data_dic):
    words = []
    for k in data_dic.values():
        words += k
    return len(words), len(set(words)), set(words)

class NaiveBayes:
    def __init__(self, data_dic):
        self.probs = {}
        self.train(data_dic)

    def train(self,data_dic):
        tot_words, tot_dist_words, all_words = count_words(data_dic)
        #print tot_words, tot_dist_words, all_words
        self.cs = []
        iter = 0
        for c, ws in data_dic.iteritems():
            self.cs.append(c)
            self.probs[c] = float(len(ws))/float(tot_words)
            no_ws = len(ws)
            cnt = collections.Counter(ws)
            for w in all_words:
                iter+=1
                #print iter
                self.probs[(w, c)] = float(cnt[w] + 1) / \
                                    (no_ws + tot_dist_words)

        #print self.probs
        #print self.cs
    def find_class(self, text):
        c_dic = {}
        pmax = float('-inf')
        cmax = None
        for c in self.cs:
            p = math.log10(self.probs[c])
            for w in text:
                #daca un cuvant nu exista in setul de date il ignoram
                #(cu probabilitatea 1)
                p  += math.log10(self.probs.setdefault((w, c), 1))
            if p > pmax:
                pmax = p
                cmax = c
            #c_dic[c] = p


        return cmax
