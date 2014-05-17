class WordBucket:
    
    def __init__(self, word_list):
        self.word_set = set(word_list)
    
    def __str__(self):
        return str(self.word_set)
        
    def __repr__(self):
        return str(self.word_set)
        
    def dist(self, wb2):
        count = 0
        for val in self.word_set:
            if val in wb2.word_set:
                count+=1
        return count

def k_nearest_neighs(data, x, k):
    sorted_keys = sorted( data.keys(), key = x.dist, reverse = True)
    return sorted_keys[0:k]

def k_nearest_class(data, x, k):
    neighs = k_nearest_neighs(data, x, k)
    cls_count = [0] * 10
    for neigh in neighs:
        cls_count[data[neigh]] += 1
    return cls_count.index( max(cls_count))


def read_input_data(input_file):
    data = {}
    fp = open(input_file)
    line = fp.readline()
    for line in fp:
        word_list = line.split()
        word_list = word_list[2:]
        cls = int(word_list[-1])
        wb = WordBucket(word_list)
        data[wb] = cls
    return data

wb = WordBucket(["ana", "are", "mere", "ana"])

wb2 = WordBucket(["ana", "nu", "bare", "mere"])

wb3 = WordBucket(["ana", "e", "smeckera"])

wb4 = WordBucket(["mere", "are", "maria"])

data = { wb:1, wb2:2, wb3:1, wb4:2}


print k_nearest_neighs(data, wb, 2)

print k_nearest_class(data, wb, 2)

data = read_input_data("input/train.tsv")
print data
