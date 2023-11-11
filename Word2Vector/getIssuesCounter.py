import json # Import the json module

# This function returns the number of issues that have a title
def getIssuesCounter(issues_filepath):
	file = open(issues_filepath, encoding="utf8") # Open the json file
	data = json.load(file) # Load the json file

	numberOfIssues = 0 # Initialize the number of issues with a title

	# For each issue in the json file
	for i in range(len(data)):
		currentIssue = data[i]["issue_data"] # Get the issue data

		# If the issue has a title
		if currentIssue["title"]:
			numberOfIssues += 1 # Increment the number of issues with a title
	
	return numberOfIssues  # Return the number of issues with a title