import NaiveBayes as nb
import KNearest as knn
import os,re
import random
import sys
from sys import stdout

def read_mails(path):
    #path = dir_path  # remove the trailing '\'
    data = []
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            with open(dir_entry_path, 'r') as my_file:
                mail = my_file.read()
                mail_arr = mail.split("\n\n", 1)
                if len(mail_arr) > 1:
                    mail_str = mail_arr[1]
                    data.append(mail_str)
    return data

def retrieve_data(path, dirs):
    data = []
    for dir in dirs:
        mail_data = read_mails(path + dir)
        data.extend(mail_data)
    return data

def make_nb_mails_dic(data_ham, data_spam, proc):
    random.shuffle(data_ham)
    random.shuffle(data_spam)
    idx_ham = len(data_ham) * float(proc) / 100
    idx_ham = int(idx_ham)
    test_ham = data_ham[idx_ham:-1]
    data_ham = data_ham[0:idx_ham]
    idx_spam = len(data_spam) * float(proc) / 100
    idx_spam = int(idx_spam)
    test_spam = data_spam[idx_spam:-1]
    data_spam = data_spam[0:idx_spam]

    nb_dic = {"ham":[], "spam":[]}
    knn_dic = {}
    for data in data_ham:
        #words = p.split(data)
        words = data.split()
        nb_dic["ham"].extend(words)
        wb = knn.WordBag(words)
        knn_dic[wb] = "ham"


    for data in data_spam:
        #words = p.split(data)
        words = data.split()
        nb_dic["spam"].extend(words)
        wb = knn.WordBag(words)
        knn_dic[wb] = "spam"

    return nb_dic, knn_dic, test_ham, test_spam

path = "input/mails/good_sample/"
dirs_ham = ["easy_ham", "easy_ham_2", "hard_ham"]
dirs_spam = ["spam", "spam_2"]

data_ham = retrieve_data(path, dirs_ham)
data_spam = retrieve_data(path, dirs_spam)

proc = float(sys.argv[1])
k = int(sys.argv[2])

nb_dic, knn_dic, test_ham, test_spam = make_nb_mails_dic(data_ham, data_spam, proc)

shnb = nb.NaiveBayes(nb_dic)
shknn = knn.KNearest(knn_dic,k, False)
shwknn = knn.KNearest(knn_dic,k, True)
cnt_ham = 0
cnt_spam = 0
knn_cnt_ham = 0
knn_cnt_spam = 0
wknn_ham = 0
wknn_spam = 0
cnt = 0
print "ham"
for mail in test_ham:
    words = mail.split()
    c = shnb.find_class(words)
    knn_c = shknn.k_nearest_class(knn.WordBag(words))
    wknn_c = shwknn.k_nearest_class(knn.WordBag(words))
    if c == "ham":
        cnt_ham+=1
    if knn_c == "ham":
        knn_cnt_ham += 1
    if wknn_c == "ham":
        wknn_ham += 1
    cnt+= 1
    stdout.write("\r%f complete" % (float(cnt) / float(len(test_ham)) * 100 ))
    stdout.flush()

print ""
print "Naive-Bayes: ", cnt_ham, " detected, ", len(test_ham), " total"
print "KNN: ", knn_cnt_ham," detected, ",  len(test_ham), " total"
print "WKNN: ", wknn_ham," detected, ",  len(test_ham), " total"

cnt = 0
for mail in test_spam:
    words = mail.split()
    c = shnb.find_class(words)
    knn_c = shknn.k_nearest_class(knn.WordBag(words))
    if c == "spam":
        cnt_spam+=1
    if knn_c == "spam":
        knn_cnt_spam += 1
    if knn_c == "spam":
        wknn_spam += 1
    cnt+= 1
    stdout.write("\r%f complete" % (float(cnt) / float(len(test_spam)) * 100 ))
    stdout.flush()

print ""
print "Naive-Bayes: ", cnt_spam, " detected, ", len(test_spam), " total"
print "KNN: ", knn_cnt_spam," detected, ",  len(test_spam), " total"
print "WKNN: ", wknn_spam," detected, ",  len(test_spam), " total"
