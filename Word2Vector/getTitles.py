import json # Import the json module
from tqdm import tqdm # For the progress bar
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

# This function returns the titles of the issues
def getTitles(quantity, issues_filepath):
	file = open(issues_filepath, encoding="utf8") # Open the json file
	data = json.load(file) # Load the json file

	if quantity == 0: # If the quantity is 0
		quantity = len(data) # Set the quantity to the number of issues

	words = [] # Initialize the list of words

	# For each issue in the json file
	print(f"{backgroundColors.GREEN}Quantity: {backgroundColors.CYAN}{quantity}{Style.RESET_ALL}")
	print(f"{backgroundColors.GREEN}Began Processing Titles{Style.RESET_ALL}")

	# For each issue in the json file
	for i in tqdm(range(len(data)), desc=f"{backgroundColors.GREEN}Processing Issues{Style.RESET_ALL}", unit="item"):
		if i >= quantity: # If the quantity of issues to read has been reached
			break # Stop reading issues
		
		currentIssue = data[i]["issue_data"] # Get the issue data

		# If the issue has a title
		if currentIssue["title"]: 
			# Add the title to the list of words
			currentIssue["title"] = currentIssue["title"].replace("/", " ").replace("\n", " ").strip().lower()
			words.append(currentIssue["title"])

	print(f"{backgroundColors.GREEN}Finished Processing Titles{Style.RESET_ALL}")

	return words # Return the list of words