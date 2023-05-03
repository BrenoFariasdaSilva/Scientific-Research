# Python program to generate word vectors using Word2Vec
# pip install nltk
# pip install gensim

# importing all necessary modules
from gensim.models import Word2Vec
import gensim
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from getTitles import *
from getIssuesCounter import *
import warnings

nltk.download('punkt')
warnings.filterwarnings(action='ignore')

quantityOfissueTitlesToRead = 0
numberOfSimilarissueTitles = 5

# print(f"Number of Issues: {getIssuesCounter()}")
issueTitles = getTitles(quantityOfissueTitlesToRead)
mostSimilarIssueTitles = []

data = []

# tokenize the sentence into words
for issue in issueTitles:
	data.append(word_tokenize(issue.lower()))

CBOWModel = gensim.models.Word2Vec(
	data, min_count=1, vector_size=100, window=5)

for currentTitle in issueTitles:
	temp = []
	for similarTitle in issueTitles:
		if currentTitle == similarTitle:
			continue
		similarity = CBOWModel.wv.n_similarity([currentTitle], [similarTitle])
		if similarity > 0.0:
			if len(temp) <= numberOfSimilarissueTitles:
				temp.append((similarity, similarTitle))
			else:
				temp.sort(reverse=True)
				if similarity > temp[0][0]:
					temp[0] = ((similarity, similarTitle))

	temp.sort(reverse=True)
	# if len(temp) > 0:
	# 	print(f'TEMP: {temp}')
	mostSimilarIssueTitles.append(temp[0:numberOfSimilarissueTitles])

for idx,issue in enumerate(issueTitles):
	for similarIssue in mostSimilarIssueTitles:
		if (similarIssue.__len__() == 0):
			continue
		print(
			f'Issue Nº{idx}: "{issue}" Similar to "{similarIssue[0][1]}" - similarity = {similarIssue[0][0]}')
	print()
