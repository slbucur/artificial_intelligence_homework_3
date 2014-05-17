import NaiveBayes as nb
import random as rand
import KNearest as knn
from multiprocessing import Process, Queue

# dic = {("a", "b"):"a", ("a", "b","c"):"a", ("c", "d"):"b", ("a", "b", "d"):"b"}
# print nb.rev_data_dic(dic)
# print nb.count_words(dic)
#
# rtnb = nb.NaiveBayes(nb.rev_data_dic(dic))
# print rtnb.find_class(("a", "b"))


def read_input_data(input_file, proc):
    nb_dic = {}
    fp = open(input_file)
    line = fp.readline()
    all_lines = []
    for line in fp:
        all_lines.append(line)


    rand.shuffle(all_lines)

    end_index = int((float(proc) / 100) * len(all_lines))
    train_lines = all_lines[0:end_index]
    test_lines = all_lines[end_index:]
    knn_dic = {}
    for line in train_lines:
        word_list = line.split()
        c = int(word_list[-1])
        nb_dic.setdefault(c, []).extend(word_list[2:-1])
        wb = knn.WordBag(word_list[2:-1])
        knn_dic[wb] = c
    return nb_dic, knn_dic, test_lines

nb_dic, knn_dic, test_lines = read_input_data("input/train.tsv", 90.9)
nb1 = nb.NaiveBayes(nb_dic)
knn1 = knn.KNearest(knn_dic, 11)

def test(q, idx_start, idx_end):
    count_nb = 0
    count_knn = 0
    #print len(test_lines)
    count = 0
    for line in test_lines[idx_start:idx_end]:
        text = line.split()
        c = int(text[-1])
        text = text[2:-1]
        nbc = nb1.find_class(text)
        knnc = knn1.k_nearest_class(knn.WordBag(text))
        if c == nbc:
            count_nb += 1
        if c == knnc:
            count_knn += 1
        print c, nbc, knnc, float(count) / float(len(test_lines)) * 100
        count+=1

    q.put((count_nb, count_knn))

q = Queue()
n = 8
ps = []
l = len(test_lines)
for i in range(n):
    idx_start = i * l / n
    idx_end = (i + 1) * l / n
    print idx_start, idx_end
    p = Process(target=test, args=(q,idx_start, idx_end,))
    ps.append(p)
for p in ps:
    p.start()
for p in ps:
    p.join()
count_nb = 0
count_knn = 0
for i in range(n):
    p_nb, p_knn = q.get()
    count_nb += p_nb
    count_knn += p_knn

#count_nb, count_knn = test()
print float(count_nb)/ len(test_lines) * 100
print float(count_knn)/ len(test_lines) * 100
