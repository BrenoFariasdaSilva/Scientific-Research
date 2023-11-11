# Python program to generate word vectors using Word2Vec

import gensim # Importing gensim for the Word2Vec model
import nltk # Importing nltk for the tokenization
import warnings # Importing warnings to ignore any warnings
from gensim.models import Word2Vec # Importing Word2Vec from gensim
from getIssuesCounter import * # Import the getIssuesCounter function
from getTitles import * # Import the getTitles function
from nltk.tokenize import sent_tokenize, word_tokenize # Importing sent_tokenize and word_tokenize from nltk.tokenize
from colorama import Style # For coloring the terminal

# Macros:
class backgroundColors: # Colors for the terminal
	CYAN = "\033[96m" # Cyan
	GREEN = "\033[92m" # Green
	YELLOW = "\033[93m" # Yellow
	RED = "\033[91m" # Red
	BOLD = "\033[1m" # Bold
	UNDERLINE = "\033[4m" # Underline
	CLEAR_TERMINAL = "\033[H\033[J" # Clear the terminal

# Download the nltk packages
def download_nltk_packages():
	nltk.download("punkt")

# Load the issue titles
def load_issue_titles(quantity, filepath):
	return getTitles(quantity, filepath) # Return the issue titles

# Train the Word2Vec model
def train_word2vec_model(data):
	return gensim.models.Word2Vec(data, min_count=1, vector_size=100, window=5)

# Find the most similar issue titles
def find_most_similar_titles(model, titles, num_similar_titles):
	most_similar_titles = [] # List of the most similar issue titles

	for current_title in titles: # For each issue title
		temp = [] # Temporary list of the most similar issue titles
		for similar_title in titles: # For each similar issue title
			if current_title == similar_title: # If the current title is equal to the similar title
				continue # Continue to the next iteration
			
			# Calculate the similarity between the current title and the similar title
			similarity = model.wv.n_similarity([current_title], [similar_title])

			# If the similarity is greater than 0.0
			if similarity > 0.0:
				# If the list is empty or the length of the list is less than the number of similar titles
				if len(temp) <= num_similar_titles: 
					temp.append((similarity, similar_title)) # Append the similarity and the similar title to the list
				else:
					temp.sort(reverse=True) # Sort the list in descending order
					if similarity > temp[0][0]: # If the similarity is greater than the first element of the list
						temp[0] = ((similarity, similar_title)) # Replace the first element of the list

		temp.sort(reverse=True) # Sort the list in descending order
		most_similar_titles.append(temp[0:num_similar_titles]) # Append the most similar titles to the list

	return most_similar_titles # Return the most similar issue titles

# Print the most similar issue titles
def show_similar_issues(issue_titles, similar_titles):
	print(f"{backgroundColors.CYAN}Similar Issues:{Style.RESET_ALL}")
	for idx, issue in enumerate(issue_titles): # For each issue title
		for similar_issue in similar_titles: # For each similar issue title
			if similar_issue.__len__() == 0: # If the list is empty
				continue # Continue to the next iteration
			print(f'{backgroundColors.GREEN}Issue Nº{backgroundColors.CYAN}{idx}{backgroundColors.GREEN}: "{backgroundColors.CYAN}{issue}{backgroundColors.GREEN}" Similar to "{backgroundColors.CYAN}{similar_issue[0][1]}{backgroundColors.GREEN}" - similarity = {backgroundColors.CYAN}{similar_issue[0][0]}{Style.RESET_ALL}')
		print(f"")

# This is the main function
def main():
	warnings.filterwarnings(action="ignore") # Ignore any warnings

	download_nltk_packages() # Download the nltk packages

	issues_titles_to_read = 0 # 0 = Read All Issue Titles
	number_of_similar_issue_titles = 5 # Number of similar issue titles to find
	issues_filepath = "./jabref/issues.json" # Path to the issues json file

	# Print the number of issues
	print(f"{backgroundColors.GREEN}Number of Issues: {backgroundColors.CYAN}{getIssuesCounter(issues_filepath)}{Style.RESET_ALL}")

	# Load the issue titles
	issue_titles = load_issue_titles(issues_titles_to_read, issues_filepath)
	# Tokenize the issue titles
	data = [word_tokenize(issue.lower()) for issue in issue_titles]

	# Train the Word2Vec model
	cbow_model = train_word2vec_model(data)

	# Find the most similar issue titles
	most_similar_issue_titles = find_most_similar_titles(cbow_model, issue_titles, number_of_similar_issue_titles)

	# Print the most similar issue titles
	show_similar_issues(issue_titles, most_similar_issue_titles)

# This is the standard boilerplate that calls the main() function.
if __name__ == "__main__":
	main() # Call the main function
