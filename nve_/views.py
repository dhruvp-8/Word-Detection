from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import *
import nltk
from collections import namedtuple

# Scraping Data
from bs4 import BeautifulSoup
import urllib3
import html5lib

# Create your views here.
def index(request):	   
	if request.method == 'POST':
		sentence = request.POST.get('sentence')
		tokens = nltk.word_tokenize(sentence)
		tagged = nltk.pos_tag(tokens)

		verbs = []
		nouns = []
		others = []

		urllib3.disable_warnings()
		http = urllib3.PoolManager()
		url = "https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html"
		response = http.request('GET', url)
		soup = BeautifulSoup(response.data, "html5lib")
		tds = soup.findAll("tr", { "bgcolor": "#FFFFCA"}, "td")
		fin = []

		for td in tds:
		    tok1 = nltk.word_tokenize(td.text)
		    t = ''
		    for j in range(0, len(tok1)):
		        if tok1[j] == '$':
		            tok1[j-1] += tok1[j]
		            tok1[j] = ''
		    for o in range(3, len(tok1)):
		        t = t + tok1[o] + ' '
		    fin.append(dict({ 'tag': tok1[2], 'description': t}))

		for i in range(0, len(tagged)):
			if tagged[i][1] == 'VBD' or tagged[i][1] == 'VB' or tagged[i][1] == 'VBG' or tagged[i][1] == 'VBN' or tagged[i][1] == 'VBP' or tagged[i][1] == 'VBZ':
				for s in range(0, len(fin)):
					if fin[s]['tag'] == tagged[i][1]:
						desc = fin[s]['description']
				vb = dict({ 'word': tagged[i][0], 'type': tagged[i][1], 'desc': desc })
				verbs.append(vb)
				flags = 0
			else:
				flags = 1	
					
			if tagged[i][1] == 'NN' or tagged[i][1] == 'NNS' or tagged[i][1] == 'NNP' or tagged[i][1] == 'NNPS':
				for s in range(0, len(fin)):
					if fin[s]['tag'] == tagged[i][1]:
						desc = fin[s]['description']
				nm = dict({ 'word': tagged[i][0], 'type': tagged[i][1], 'desc': desc})
				nouns.append(nm)
				flag = 0
			else:
				flag = 1

			if flag == 1 and flags == 1:
				for s in range(0, len(fin)):
					if fin[s]['tag'] == tagged[i][1]:
						desc = fin[s]['description']
				ot = dict({ 'word': tagged[i][0], 'type': tagged[i][1], 'desc': desc })
				others.append(ot)

		return render(request, 'index.html', { 'verbs': verbs, 'nouns': nouns, 'others': others, 'sentence': sentence })			
	return render(request, 'index.html', {})