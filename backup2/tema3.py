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
    count = 0
    for line in fp:
        word_list = line.split()
        word_list = word_list[2:]
        cls = int(word_list[-1])
        wb = WordBucket(word_list[0:-1])
        data[wb] = cls
        if count < 10:
            count += 1
            print word_list
    return data


data = read_input_data("input/train.tsv")

wb = WordBucket(['A', 'series'])
print k_nearest_neighs(data, wb, 10)

print k_nearest_class(data, wb, 10)
