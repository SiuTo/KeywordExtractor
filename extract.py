#! /usr/bin/env python3

# Usage: python3 extract.py [options] filename
# options:
#   -k [NUM]:	Specify the number of keywords.
#   -w:			Print out the weight of keywords.

import jieba
import csv
import nltk
import string
import math
import operator
import re
import sys
import getopt

Accept_chars = "[a-zA-Z0-9\u4E00-\u9FFF]+"
English_stopwords = nltk.corpus.stopwords.words("english")
Chinese_stopwords = [line.strip() for line in open("chinese_stopwords.txt")]

# pass the arguments
TopK = 10
WithWeight = False
optlist, args = getopt.getopt(sys.argv[1:], "wk:")
for opt, value in optlist:
	if opt=="-w":
		WithWeight = True
	elif opt=="-k":
		TopK = int(value)
FileName = args[0]

# read data
dataCSV = csv.reader(open(FileName))
next(dataCSV, None)
total_article = 0
occur_list = []
articles = nltk.defaultdict(list)
for row in dataCSV:
	total_article += 1
	subject, movie, title, star, time, useful, useless, content = row
	words = [w.lower() for w in jieba.cut(content) if re.match(Accept_chars, w) and w.lower() not in English_stopwords and w not in Chinese_stopwords]
	occur_list += list(set(words))
	articles[int(subject)].append((int(useful), words))
fd = nltk.FreqDist(occur_list)
IDF = dict((w, math.log(total_article/fd[w])) for w in fd)

for subject in sorted(articles):
	weight = nltk.defaultdict(float)
	sum_weight = 0
	for (useful, words) in articles[subject]:
		TF_fd = nltk.FreqDist(words)
		temp = useful+1
		sum_weight += temp
		for w in words:
			weight[w] += temp*TF_fd.freq(w)
	for w in weight:
		weight[w] *= IDF[w]/sum_weight
	keywords = sorted(weight.items(), key=operator.itemgetter(1), reverse=True)
	if WithWeight:
		print(str(subject)+":", "; ".join(["{} {:.2F}".format(pair[0], pair[1]) for pair in keywords[:TopK]]))
	else:
		print(str(subject)+":", " ".join([pair[0] for pair in keywords[:TopK]]))

