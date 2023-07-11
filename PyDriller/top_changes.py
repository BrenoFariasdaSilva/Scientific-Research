import os # for walking through directories
import csv # for reading csv files
import numpy as np # for calculating the min, max, avg, and third quartile of each metric
import pandas as pd # for the csv file operations
from tqdm import tqdm # for progress bar
from colorama import Style # For coloring the terminal

# Import from the main.py file
from ck_metrics import backgroundColors

# CONSTANTS:
PATH = os.getcwd() # Get the current working directory
PROCESS_CLASSES = input(f"{backgroundColors.OKGREEN}Do you want to process the {backgroundColors.OKCYAN}class.csv{backgroundColors.OKGREEN} file? {backgroundColors.OKCYAN}(True/False){backgroundColors.OKGREEN}: {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file
MINIMUM_CHANGES = 1 # The minimum number of changes a method should have to be considered
NUMBER_OF_METRICS = 4 # The number of metrics
DEFAULT_REPOSITORY_NAME = ["commons-lang", "jabref"] # The default repository name

# Extensions:
CSV_FILE_EXTENSION = ".csv" # The extension of the file that contains the commit hashes

# Filenames:
CK_CSV_FILE = "class.csv" if PROCESS_CLASSES else "method.csv" # The name of the csv generated file from ck.
CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # The name of the csv generated file from ck.
CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}-changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the top changed methods
SORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '')}-sorted_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the sorted top changed methods
RELATIVE_CK_METRICS_DIRECTORY_PATH = "/ck_metrics" # The relative path to the directory containing the ck metrics
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "/metrics_evolution" # The relative path to the directory containing the metrics evolution
RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH = "/metrics_statistics" # The relative path to the directory containing the metrics statistics

# Directories Paths:
FULL_CK_METRICS_DIRECTORY_PATH = f"{PATH}{RELATIVE_CK_METRICS_DIRECTORY_PATH}" # The full path to the directory containing the ck metrics
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = f"{PATH}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}" # The full path to the directory containing the metrics evolution
FULL_METRICS_STATISTICS_DIRECTORY_PATH = f"{PATH}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}" # The full path to the directory containing the metrics statistics

# @brief: This function is used to check if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Verify if the PATH constant contains whitespaces
   if " " in PATH:
      return True
   return False

# @brief: Verifiy if the attribute is empty. If so, set it to the default value
# @param: attribute: The attribute to be checked
# @param: default_attribute_value: The default value of the attribute
# @return: The repository URL and the output directory
def validate_attribute(attribute, default_attribute_value):
   if not attribute:
      print(f"{backgroundColors.WARNING}The attribute is empty! Using the default value: {backgroundColors.OKCYAN}{default_attribute_value}{Style.RESET_ALL}")
      attribute = default_attribute_value
   return attribute

# @brief: Gets the user input for the repository name and returns the path to the directory
# @param: None
# @return: A tuple containing the repository name and the path to the directory
def get_directory_path():
	repository_name = input(f"{backgroundColors.OKGREEN}Enter the repository name {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")
	repository_name = validate_attribute(repository_name, DEFAULT_REPOSITORY_NAME[0])
	
	directory_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}"

	# Verify if the directory does not exist
	while not os.path.isdir(directory_path):
		print(f"{backgroundColors.FAIL}The directory does not exist. Please try again.{Style.RESET_ALL}")
		repository_name = input(f"{backgroundColors.OKGREEN}Enter the repository name {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")
		directory_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}"

	return repository_name, directory_path

# @brief: This verifies if all the ck metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: repository_name: Name of the repository to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def verify_ck_metrics_folders(repository_name):
   print(f"{backgroundColors.OKGREEN}Checking if all the {backgroundColors.OKCYAN}CK metrics{backgroundColors.OKGREEN} are already calculated for the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository...{Style.RESET_ALL}")
   current_path = PATH
   data_path = os.path.join(current_path, RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]) # Join the current path with the relative path of the ck metrics directory
   repo_path = os.path.join(data_path, repository_name) # Join the data path with the repository name
   commit_file = f"{repository_name}-commit_hashes{CSV_FILE_EXTENSION}" # The name of the commit hashes file
   commit_file_path = os.path.join(data_path, commit_file) # Join the data path with the commit hashes file

   # Verify if the repository exists
   if not os.path.exists(commit_file_path):
      print(f"{backgroundColors.FAIL}File {backgroundColors.OKCYAN}{commit_file}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{data_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
      return False

   # Read the commit hashes file
   with open(commit_file_path, "r") as file:
      lines = file.readlines() # Read all the lines of the file and store them in a list

   # Verify if the repository exists
   for line in lines:
      # Get the commit hash
      folder_name = line.strip() # Remove the \n from the line
      folder_path = os.path.join(repo_path, folder_name) # Join the repo path with the folder name

      if not os.path.exists(folder_path): # Verify if the folder exists
         print(f"{backgroundColors.FAIL}Folder {backgroundColors.OKCYAN}{folder_name}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{repo_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
         return False
   return True

# @brief: Create a directory
# @param: full_directory_name: Name of the directory to be created
# @param: relative_directory_name: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_name, relative_directory_name):
   if os.path.isdir(full_directory_name): # Verify if the directory already exists
      print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory already exists{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_name)
      print (f"{backgroundColors.OKGREEN}Successfully created the {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print (f"{backgroundColors.OKGREEN}The creation of the {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory failed{Style.RESET_ALL}")

# @brief: Validate the class name, that is, if it contains any dots in the name
# @param class_name: The name of the class
# @return: True if the class name is valid, False otherwise
def valid_class_name(class_name):
	return "." in class_name

# @brief: Gets the package name of the class, which is, get the substring between that starts with "/src/"(excluded) until the last dot(excluded)
# @param file_name: The file name where the class is located
# @return: The package name of the class
def get_class_package_name(file_name):
	start_substring = "/src/"
	package_name = file_name[file_name.find(start_substring) + len(start_substring):file_name.rfind(".")]

	# Replace the slashes with dots
	package_name = package_name.replace("/", ".")

	return package_name

# @brief: Processes a csv file containing the metrics of a method nor class
# @param file_path: The path to the csv file
# @param metrics_track_record: A dictionary containing the track record of the metrics of each method nor class
# @return: None
def process_csv_file(file_path, metrics_track_record):
	# Open the csv file
	with open(file_path, "r") as csvfile:
		# Read the csv file
		reader = csv.DictReader(csvfile)
		# Iterate through each row, that is, for each method in the csv file
		for row in reader:
			class_name = row["class"]
			if PROCESS_CLASSES:
				if not valid_class_name(class_name):
					class_name = get_class_package_name(row["file"])
				variable_attribute = row["type"]
			else:
				variable_attribute = row["method"]
			cbo = float(row["cbo"])
			cboModified = float(row["cboModified"])
			wmc = float(row["wmc"])
			rfc = float(row["rfc"])

			# Create a tuple containing the metrics
			metrics = (cbo, cboModified, wmc, rfc)
			identifier = f"{class_name} {variable_attribute}"

			if identifier not in metrics_track_record: # if the identifier (of the method or class) is not in the dictionary
				metrics_track_record[identifier] = {"metrics": [], "changed": 0}

			# Get the metrics_changes list for the method
			metrics_changes = metrics_track_record[identifier]["metrics"]

			# Try to find the same metrics in the list for the same method. If it does not exist, then add it to the list
			if metrics not in metrics_changes: # if the metrics are not in the list
				metrics_changes.append(metrics) # add the metrics values to the list
				metrics_track_record[identifier]["changed"] += 1 # increment the number of changes

# @brief: Traverses a directory and processes all the csv files
# @param directory_path: The path to the directory
# @return: A dictionary containing the metrics of each class and method combination
def traverse_directory(directory_path):
	print(f"{backgroundColors.OKGREEN}Traversing the {backgroundColors.OKCYAN}{'/'.join(directory_path.rsplit('/', 2)[-2:])}{backgroundColors.OKGREEN} directory...{Style.RESET_ALL}")
	metrics_track_record = {}
	file_count = 0
	progress_bar = None

	# Traverse the directory
	for root, dirs, files in os.walk(directory_path):
		# Iterate through each file in the directory and call the process_csv_file function to get the methods metrics of each file
		for file in files:
			# If the file is a csv file
			if file == CK_CSV_FILE:
				file_path = os.path.join(root, file) # Get the path to the csv file
				process_csv_file(file_path, metrics_track_record) # Process the csv file
				file_count += 1 # Increment the file count

				if progress_bar is None: # If the progress bar is not initialized
					progress_bar = tqdm(total=file_count) # Initialize the progress bar
				else:
					progress_bar.update(1) # Update the progress bar

	# Close the progress bar
	if progress_bar is not None:
		progress_bar.close()

	# Return the method metrics, which is a dictionary containing the metrics of each method  
	return metrics_track_record

# @brief: Calculates the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
# @param csv_writer: The csv writer object
# @param id: The id of the method
# @param key: The key of the method
# @param metrics: The list of metrics
# @param metrics_values: The list of metrics values
# @return: None
def write_method_metrics_statistics(csv_writer, id, key, metrics, metrics_values):
	cboMin = round(float(min(metrics_values[0])), 3)
	cboMax = round(float(max(metrics_values[0])), 3)
	cboAvg = round(float(sum(metrics_values[0])) / len(metrics_values[0]), 3)
	cboQ3 = round(float(np.percentile(metrics_values[0], 75)), 3)
	cboModifiedMin = round(float(min(metrics_values[1])), 3)
	cboModifiedMax = round(float(max(metrics_values[1])), 3)
	cboModifiedAvg = round(float(sum(metrics_values[1])) / len(metrics_values[1]), 3)
	cboModifiedQ3 = round(float(np.percentile(metrics_values[1], 75)), 3)
	wmcMin = round(float(min(metrics_values[2])), 3)
	wmcMax = round(float(max(metrics_values[2])), 3)
	wmcAvg = round(float(sum(metrics_values[2])) / len(metrics_values[2]), 3)
	wmcQ3 = round(float(np.percentile(metrics_values[2], 75)), 3)
	rfcMin = round(float(min(metrics_values[3])), 3)
	rfcMax = round(float(max(metrics_values[3])), 3)
	rfcAvg = round(float(sum(metrics_values[3])) / len(metrics_values[3]), 3)
	rfcQ3 = round(float(np.percentile(metrics_values[3], 75)), 3)

	csv_writer.writerow([id, key, metrics["changed"], cboMin, cboMax, cboAvg, cboQ3, cboModifiedMin, cboModifiedMax, cboModifiedAvg, cboModifiedQ3, wmcMin, wmcMax, wmcAvg, wmcQ3, rfcMin, rfcMax, rfcAvg, rfcQ3])

# @brief: Process the metrics in metrics_track_record to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
# @param repository_name: The name of the repository
# @param metrics_track_record: A dictionary containing the metrics of each method or class
# @return: None
def process_metrics_track_record(repository_name, metrics_track_record):
	# Open the csv file and process the metrics of each method
	with open(FULL_METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "/" + CHANGED_METHODS_CSV_FILENAME, "w") as csvfile:
		writer = csv.writer(csvfile)	
		if PROCESS_CLASSES:
			writer.writerow(["Class", "Type", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "CBOModified Min", "CBOModified Max", "CBOModified Avg", "CBOModified Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3"])
		else:
			writer.writerow(["Class", "Method", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "CBOModified Min", "CBOModified Max", "CBOModified Avg", "CBOModified Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3"])

		# Loop inside the *metrics["metrics"] in order to get the min, max, avg, and third quartile of each metric (cbo, cboModified, wmc, rfc)
		for identifier, metrics in metrics_track_record.items():
			# check if the metrics changes is greater than the minimum changes
			if metrics["changed"] < MINIMUM_CHANGES:
				continue

			# This stores the metrics values in a list of lists of each metric
			metrics_values = []
			for i in range(0, NUMBER_OF_METRICS):
				# This get the metrics values of each metric occurence in the method in order to, later on, be able to get the min, max, avg, and third quartile of each metric
				metrics_values.append([sublist[i] for sublist in metrics["metrics"]])

			# split the identifier to get the id and key which is separated by a space
			id = identifier.split(" ")[0]
			key = identifier.split(" ")[1]

			# Create a function to get the min, max, avg, and third quartile of each metric and then write it to the csv file
			write_method_metrics_statistics(writer, id, key, metrics, metrics_values)

# @brief: This function sorts the csv file according to the number of changes
# @param: repository_name: The name of the repository
# @return: None
def sort_csv_by_changes(repository_name):
	# Read the csv file
	data = pd.read_csv(FULL_METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "/" + CHANGED_METHODS_CSV_FILENAME)
	# Sort the csv file by the number of changes
	data = data.sort_values(by=["Changed"], ascending=False)
	# Write the sorted csv file to a new csv file
	data.to_csv(FULL_METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "/" + SORTED_CHANGED_METHODS_CSV_FILENAME, index=False)

# @brief: This function writes the metrics evolution to a csv file
# @param: repository_name: The name of the repository
# @param: metrics_track_record: A dictionary containing the metrics of each method or class
# @return: None
def write_metrics_evolution_to_csv(repository_name, metrics_track_record):
	# For every identifier in the metrics_track_record, store each metrics values tuple in a row of the csv file
	for identifier, metrics in metrics_track_record.items():
		identifier = identifier.split(' ')[0] # Get the identifier which is currently the class name
		variable_attribute = identifier.split(" ")[1] # Get the variable attribute which could be the type of the class or the method name
		with open(FULL_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "/" + identifier + "-" + variable_attribute + CSV_FILE_EXTENSION, "w") as csvfile:
			writer = csv.writer(csvfile)
			if PROCESS_CLASSES:
				writer.writerow(["Class", "CBO", "CBO Modified", "WMC", "RFC"])
			else:
				identifier = identifier.split(" ")[1] # Make the identifier be the method name
				writer.writerow(["Method", "CBO", "CBO Modified", "WMC", "RFC"])
			
			for metrics_values in metrics["metrics"]:
				writer.writerow([identifier, metrics_values[0], metrics_values[1], metrics_values[2], metrics_values[3], metrics_values[4]])

# @brief: The main function
# @param: None
# @return: None
def main():
	# check if the path constants contains whitespaces
	if path_contains_whitespaces():
		print(f"{backgroundColors.FAIL}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
		return

	print(f"{backgroundColors.OKGREEN}This script {backgroundColors.OKCYAN}generates a csv file{backgroundColors.OKGREEN} with the {backgroundColors.OKCYAN}{CLASSES_OR_METHODS} sorted{backgroundColors.OKGREEN} by the {backgroundColors.OKCYAN}number of times that the {CK_CSV_FILE.replace('.csv', '')} changed{backgroundColors.OKGREEN} and store it inside the {backgroundColors.OKCYAN}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}{backgroundColors.OKGREEN} directory.{Style.RESET_ALL}")
	print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}source of the metrics values{backgroundColors.OKGREEN} is the {backgroundColors.OKCYAN}{CK_CSV_FILE}{backgroundColors.OKGREEN} files.{Style.RESET_ALL}")

	# Get the directory path from user input of the repository name
	repository_name, directory_path = get_directory_path()

	# Verify if the ck metrics were already calculated, which are the source of the data processed by traverse_directory(directory_path).
	if not verify_ck_metrics_folders(repository_name):
		print(f"{backgroundColors.FAIL}The metrics for {backgroundColors.OKCYAN}{repository_name}{backgroundColors.FAIL} were not calculated. Please run the ck_metrics.py file first{Style.RESET_ALL}")
		return

	# Create the output RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH directory if it does not exist
	create_directory(FULL_METRICS_STATISTICS_DIRECTORY_PATH, RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH)

	# Traverse the directory and get the method metrics
	metrics_track_record = traverse_directory(directory_path)

	# Process the method metrics to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
	process_metrics_track_record(repository_name, metrics_track_record)

	# Sort the csv file by the number of changes
	sort_csv_by_changes(repository_name)

	# Remove the old csv file
	os.remove(FULL_METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "-" + CHANGED_METHODS_CSV_FILENAME)

	# Write the metrics_evolution files to a csv file
	write_metrics_evolution_to_csv(repository_name, metrics_track_record)

	print(f"{backgroundColors.OKCYAN}Successfully sorted{backgroundColors.OKGREEN} by the {backgroundColors.OKCYAN}number of times they changed{backgroundColors.OKGREEN} and {backgroundColors.OKCYAN}stored{backgroundColors.OKGREEN} inside the {backgroundColors.OKCYAN}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}{backgroundColors.OKGREEN} directory.{Style.RESET_ALL}")

# Directive to run the main function
if __name__ == "__main__":
	main() # Call the main function