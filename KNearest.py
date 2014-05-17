def keywithmaxval(d):
     """ a) create a list of the dict's keys and values;
         b) return the key with the max value"""
     v=list(d.values())
     k=list(d.keys())
     return k[v.index(max(v))]

class WordBag:

    def __init__(self, word_list):
        self.word_set = set(word_list)

    def __str__(self):
        return str(self.word_set)

    def __repr__(self):
        return str(self.word_set)

    def dist(self, wb2):
        return len(self.word_set & wb2.word_set)

    def contains(self, word):
        if word in self.word_set:
            return True
        return False

class KNearest:
    def __init__(self, data_dic, k):
        self.data = data_dic
        self.k = k

    def k_nearest_neighs(self,x):
        k_neigh = ["first"]
        k_neigh_dist = [100000]
        for k in self.data.keys():
            dist = x.dist(k)
            for i in range(len(k_neigh) - 1, -1, -1):
                if(k_neigh_dist[i] > dist):
                    k_neigh.insert(i + 1, k)
                    k_neigh_dist.insert(i + 1, dist)
                    break
            if len(k_neigh) > (self.k + 1):
                del k_neigh[-1]
                del k_neigh_dist[-1]

        #sorted_keys = sorted( self.data.keys(), key = x.dist, reverse = True)
        #print x
        #print sorted_keys[0:self.k]
        #print k_neigh
        return k_neigh[1:]

    def k_nearest_class(self, x):
        neighs = self.k_nearest_neighs(x)
        cls_count = {}
        for neigh in neighs:
            cls_count[self.data[neigh]] = cls_count.get(self.data[neigh], 0) + 1
        return keywithmaxval(cls_count)
