import NaiveBayes as nb
import KNearest as knn
import os,re
import random

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

path = "input/mails/bla/"
dirs_ham = ["easy_ham", "easy_ham_2", "hard_ham"]
dirs_spam = ["spam", "spam_2"]

data_ham = retrieve_data(path, dirs_ham)
data_spam = retrieve_data(path, dirs_spam)

nb_dic, knn_dic, test_ham, test_spam = make_nb_mails_dic(data_ham, data_spam, 70)
#print nb_dic.values()
shnb = nb.NaiveBayes(nb_dic)
shknn = knn.KNearest(knn_dic,11)
cnt_ham = 0
cnt_spam = 0
knn_cnt_ham = 0
knn_cnt_spam = 0
#print test_ham
for mail in test_ham:
    c = shnb.find_class(mail.split())
    knn_c = shknn.k_nearest_class(knn.WordBag(mail.split()))
    if c == "ham":
        cnt_ham+=1
    if knn_c == "ham":
        knn_cnt_ham += 1
print cnt_ham, len(test_ham)
print knn_cnt_ham, len(test_ham)

for mail in test_spam:
    c = shnb.find_class(mail.split())
    knn_c = shknn.k_nearest_class(knn.WordBag(mail.split()))
    if c == "spam":
        cnt_spam+=1
    if knn_c == "spam":
        knn_cnt_spam += 1
print cnt_spam, len(test_spam)
print knn_cnt_spam, len(test_spam)
print "Change"
