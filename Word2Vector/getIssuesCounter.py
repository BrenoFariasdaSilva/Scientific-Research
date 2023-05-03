import json

def getIssuesCounter():
	file = open('./jabref/issues.json')
	data = json.load(file)

	numberOfIssues = 0

	for i in range(len(data)):
		currentIssue = data[i]['issue_data']

		if currentIssue['title']:
			numberOfIssues += 1
	
	return numberOfIssues 