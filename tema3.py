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

    def contains(self, word):
        if word in self.word_set:
            return True
        return False

def bayes_count_cls(data):
    cls_count = [0] * (max(data.values()) + 1)
    for cls in data.values():
        cls_count[cls] += 1
    return cls_count

def bayes_count_words(data, word, cls):
    count = 0
    for wb in data.keys():
        if data[wb] == cls and wb.contains(word):
            count+=1
    return count

def bayes_count_words_cls(data, word):
    word_cls = [0] * (max(data.values()) + 1)
    for wb in data.keys():
        if wb.contains(word):
            word_cls[data[wb]]+=1
    return count

def bayes_probs(data, wb, cls_count):
    probs = {}
    for cls in range(len(cls_count)):
        prob = float(cls_count[cls]) / len(data.values())
        for word in wb.word_set:
            count = bayes_count_words(data, word, cls)
            count += 1
            prob *= float(count) / cls_count[cls]
        probs[cls] = prob
    return probs

def k_nearest_neighs(data, x, k):
    sorted_keys = sorted( data.keys(), key = x.dist, reverse = True)
    return sorted_keys[0:k]

def k_nearest_class(data, x, k):
    neighs = k_nearest_neighs(data, x, k)
    cls_count = [0] * (max(data.values()) + 1)
    for neigh in neighs:
        cls_count[data[neigh]] += 1
    return cls_count.index( max(cls_count))


def read_input_data(input_file):
    data = {}
    words = set([])
    fp = open(input_file)
    line = fp.readline()
    maxi = 0
    for line in fp:
        word_list = line.split()
        word_list = word_list[2:]
        cls = int(word_list[-1])
        wb = WordBucket(word_list[0:-1])
        if(len(wb.word_set) > maxi):
            maxi = len(wb.word_set)
        words.update(wb.word_set)
        data[wb] = cls
    print len(words), maxi
    return data


data = read_input_data("input/train.tsv")

wb = WordBucket("A series of escapades demonstrating the adage that what is good for the goose is also good for the gander , some of which occasionally amuses but none of which amounts to much of a story ".split())
print k_nearest_neighs(data, wb, 10)

print k_nearest_class(data, wb, 10)

cls_count =  bayes_count_cls(data)

print cls_count

print bayes_count_words(data, 'A', 2)

print bayes_probs(data, wb, cls_count)
