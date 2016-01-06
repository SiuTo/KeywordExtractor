#! /usr/bin/env python3

import jieba
import csv
import nltk
import string
import math
import operator

Symbols = string.punctuation+string.whitespace+"[！￥……（）——【】{}、；：‘’“”，。《》「」『』？]　＝－•─"

# read data
dataCSV = csv.reader(open("douban.csv"))
next(dataCSV, None)
total_article = 0
occur_list = []
articles = nltk.defaultdict(list)
for row in dataCSV:
	total_article += 1
	subject, movie, title, star, time, useful, useless, content = row
	words = [w for w in jieba.cut(content) if w not in Symbols]
	occur_list += list(set(words))
	articles[subject].append((int(useful), words))
fd = nltk.FreqDist(occur_list)
IDF = dict((w, math.log(total_article/fd[w])) for w in fd)

for subject in articles:
	weight = nltk.defaultdict(float)
	for (useful, words) in articles[subject]:
		TF_fd = nltk.FreqDist(words)
		for w in words:
			weight[w] += useful*TF_fd.freq(w)
	for w in weight:
		weight[w] *= IDF[w]
	keywords = sorted(weight.items(), key=operator.itemgetter(1), reverse=True)
	print(subject+":", " ".join([pair[0] for pair in keywords[:10]]))

