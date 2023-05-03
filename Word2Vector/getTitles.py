import json

def getTitles(qnt):
	file = open('./jabref/issues.json', encoding="utf8") # Insert here the path to the issues.json file
	data = json.load(file)

	if qnt == 0:
		qnt = len(data)

	words = []

	print(f'Began Processing Titles')
	for i in range(len(data)):
		if i >= qnt:
			break
		currentIssue = data[i]['issue_data']
		if currentIssue['title']:
			currentIssue['title'] = currentIssue['title'].replace('/', ' ').replace('\n', ' ').strip().lower()
			words.append(currentIssue['title'])
	print(f'Finished Processing Titles')
	return words 