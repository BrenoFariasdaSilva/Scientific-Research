import os # for walking through directories
import csv # for reading csv files
import numpy as np # for calculating the min, max, avg, and third quartile of each metric
import pandas as pd # for the csv file operations
from tqdm import tqdm # for progress bar
from colorama import Style # For coloring the terminal

# Import from the main.py file
from main import backgroundColors

# CONSTANTS:
PROCESS_CLASSES = input(f"{backgroundColors.OKGREEN}Do you want to process the {backgroundColors.OKCYAN}class.csv{backgroundColors.OKGREEN} file? {backgroundColors.OKCYAN}(True/False){backgroundColors.OKGREEN}: {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file
MINIMUM_CHANGES = 2 # The minimum number of changes a method should have to be considered
NUMBER_OF_METRICS = 4 # The number of metrics
DEFAULT_REPOSITORY_NAME = "commons-lang" # The default repository name

# Filenames:
CK_CSV_FILE = "class.csv" if PROCESS_CLASSES else "method.csv" # The name of the csv generated file from ck.
CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '').upper()}-changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the top changed methods
SORTED_CHANGED_METHODS_CSV_FILENAME = f"{CK_CSV_FILE.replace('.csv', '').upper()}-sorted_changes.{CK_CSV_FILE.split('.')[1]}" # The name of the csv file containing the sorted top changed methods
CK_METRICS_DIRECTORY_NAME = "ck_metrics" # The relative path to the directory containing the ck metrics
METRICS_STATISTICS_DIRECTORY_NAME = "metrics_statistics" # The relative path to the directory containing the metrics statistics

# Directories Paths:
CK_METRICS_DIRECTORY_PATH = f"{os.getcwd()}/{CK_METRICS_DIRECTORY_NAME}" # The full path to the directory containing the ck metrics
METRICS_STATISTICS_DIRECTORY_PATH = f"{os.getcwd()}/{METRICS_STATISTICS_DIRECTORY_NAME}" # The full path to the directory containing the metrics statistics

# Full Files Paths:
TOP_CHANGED_FILES_CSV_FILE_PATH = f"{METRICS_STATISTICS_DIRECTORY_PATH}/{CHANGED_METHODS_CSV_FILENAME}" # The full path to the csv file containing the top changed methods
SORTED_TOP_CHANGED_FILES_CSV_FILE_PATH = f"{METRICS_STATISTICS_DIRECTORY_PATH}/{SORTED_CHANGED_METHODS_CSV_FILENAME}" # The full path to the csv file containing the sorted top changed methods

# @brief: This function create the output directories if they do not exist
# @param: None
# @return: None
def create_output_directories():
	# Create the output directories if they do not exist
	if not os.path.isdir(METRICS_STATISTICS_DIRECTORY_PATH):
		os.mkdir(METRICS_STATISTICS_DIRECTORY_PATH)

# @brief: Gets the user input for the repository name and returns the path to the directory
# @param: None
# @return: A tuple containing the repository name and the path to the directory
def get_directory_path():
	repository_name = input(f"{backgroundColors.OKGREEN}Enter the repository name {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")
	if repository_name == "":
		repository_name = DEFAULT_REPOSITORY_NAME
	directory_path = f"{CK_METRICS_DIRECTORY_PATH}/{repository_name}"

	# Check if the directory does not exist
	while not os.path.isdir(directory_path):
		print(f"{backgroundColors.FAIL}The directory does not exist. Please try again.{Style.RESET_ALL}")
		repository_name = input(f"{backgroundColors.OKGREEN}Enter the repository name {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")
		directory_path = f"{CK_METRICS_DIRECTORY_PATH}/{repository_name}"

	return repository_name, directory_path

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
	with open(METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "-" + SORTED_TOP_CHANGED_METHODS_CSV_FILENAME, "w") as csvfile:
		writer = csv.writer(csvfile)	
		if PROCESS_CLASSES:
			writer.writerow(["Class", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "CBOModified Min", "CBOModified Max", "CBOModified Avg", "CBOModified Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3"])
		else:
			writer.writerow(["Method", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "CBOModified Min", "CBOModified Max", "CBOModified Avg", "CBOModified Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3"])

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

			# Create a function to get the min, max, avg, and third quartile of each metric and then write it to the csv file
			write_method_metrics_statistics(writer, identifier, metrics, metrics_values)

# @brief: This function sorts the csv file according to the number of changes
# @param: None
# @return: None
def sort_csv_by_changes():
	# Read the csv file
	data = pd.read_csv(TOP_CHANGED_FILES_CSV_FILE_PATH)
	# Sort the csv file by the number of changes
	data = data.sort_values(by=["Changed"], ascending=False)
	# Write the sorted csv file to a new csv file
	data.to_csv(SORTED_TOP_CHANGED_FILES_CSV_FILE_PATH, index=False)

# @brief: The main function
# @param: None
# @return: None
def main():
	print(f"{backgroundColors.OKGREEN}This script calculates the minimum, maximum, average, and third quartile of each metric and writes it to a csv file.{Style.RESET_ALL}")
	print(f"{backgroundColors.OKGREEN}The source of the metrics values is the {backgroundColors.OKCYAN}{CK_CSV_FILE}{backgroundColors.OKGREEN} file.{Style.RESET_ALL}")

	# Get the directory path from user input of the repository name
	repository_name, directory_path = get_directory_path()

	# Create the output directories if they do not exist
	create_output_directories()

	# Traverse the directory and get the method metrics
	metrics_track_record = traverse_directory(directory_path)

	# Process the method metrics to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
	process_metrics_track_record(repository_name, metrics_track_record)

	# Sort the csv file by the number of changes
	sort_csv_by_changes()

	# Remove the old csv file
	os.remove(TOP_CHANGED_FILES_CSV_FILE_PATH)

# Directive to run the main function
if __name__ == "__main__":
	main() # Call the main function