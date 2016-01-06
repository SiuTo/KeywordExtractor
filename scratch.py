#! /usr/bin/env python3

import urllib.request
import re
from html.parser import HTMLParser
import csv

Home = "http://movie.douban.com"
MaxLimit = 1

class ArticleParser(HTMLParser):
	def __init__(self):
		HTMLParser.__init__(self)
		self.content = ""

	def handle_data(self, data):
		self.content += data

def get(url):
	response = urllib.request.urlopen(url)
	return response.read().decode()


lines = open("subject_list.txt").readlines()
subject_list = [line.strip() for line in lines]

data = [["subject", "movie", "title", "star", "time", "useful", "useless", "content"]]
for subject in set(subject_list):
	print("Subject "+subject+":")
	baseurl = Home+"/subject/"+subject+"/reviews"
	parameters = ""
	html = get(baseurl)
	movie = re.search('<meta name="keywords" content="([^,]+),', html).group(1)
	cnt = 0
	while True:
		html = get(baseurl+parameters)
		article_list = re.findall('href="(\S+)" onclick="moreurl\(this, {from: \'\'}\)" class="">', html)
		for url in article_list:
			cnt += 1
			if cnt>MaxLimit: break
			print("Scratching "+url)
			page = get(url)
			title = re.search('<h1><span property="v:summary">(.+)</span></h1>', page).group(1)
			star = re.search('<span property="v:rating" class="main-title-hide">(\w+)</span>', page).group(1)
			time = re.search('class="main-meta">(.+)</span>', page).group(1)
			vote = re.findall('<em id="ucount\w+">(\d*)</em>', page)
			if vote[0]=="":
				vote[0] = "0"
			if vote[1]=="":
				vote[1] = "0"

			text = re.search('<div property="v:description" class="">(.+)<div class="clear"></div></div>', page).group(1)
			parser = ArticleParser()
			parser.feed(text)

			data.append([subject, movie, title, star, time, vote[0], vote[1], parser.content])

		if cnt>MaxLimit: break
		next_page = re.search('href="(\S+)" data-page="" class="next">', html)
		if next_page:
			parameters = next_page.group(1)
		else:
			break
	print()

dataCSV = csv.writer(open("douban.csv", "w"))
dataCSV.writerows(data)

