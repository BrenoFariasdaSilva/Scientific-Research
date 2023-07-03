import os # for walking through directories
import csv # for reading csv files
import numpy as np # for calculating the min, max, avg, and third quartile of each metric
import pandas as pd # for the csv file operations
from tqdm import tqdm # for progress bar

# CONSTANTS:
MINIMUM_CHANGES = 2 # The minimum number of changes a method should have to be considered
NUMBER_OF_METRICS = 4 # The number of metrics

# Filenames:
CK_CSV_FILE = "method.csv" # The default csv file name. It could be "method.csv" or "class.csv"
TOP_CHANGED_METHODS_CSV_FILENAME = f"top_changed_{CK_CSV_FILE}" # The name of the csv file containing the top changed methods
SORTED_TOP_CHANGED_METHODS_CSV_FILENAME = f"sorted_top_changed_{CK_CSV_FILE}" # The name of the csv file containing the sorted top changed methods
CK_METRICS_DIRECTORY_NAME = "ck_metrics" # The relative path to the directory containing the ck metrics
METRICS_STATISTICS_DIRECTORY_NAME = "metrics_statistics" # The relative path to the directory containing the metrics statistics

# Directories Paths:
CK_METRICS_DIRECTORY_PATH = f"{os.getcwd()}/{CK_METRICS_DIRECTORY_NAME}" # The full path to the directory containing the ck metrics
METRICS_STATISTICS_DIRECTORY_PATH = f"{os.getcwd()}/{METRICS_STATISTICS_DIRECTORY_NAME}" # The full path to the directory containing the metrics statistics

# Full Files Paths:
TOP_CHANGED_FILES_CSV_FILE_PATH = f"{METRICS_STATISTICS_DIRECTORY_PATH}/{TOP_CHANGED_METHODS_CSV_FILENAME}" # The full path to the csv file containing the top changed methods
SORTED_TOP_CHANGED_FILES_CSV_FILE_PATH = f"{METRICS_STATISTICS_DIRECTORY_PATH}/{SORTED_TOP_CHANGED_METHODS_CSV_FILENAME}" # The full path to the csv file containing the sorted top changed methods

# @brief: This function create the output directories if they do not exist
# @param: None
# @return: None
def create_output_directories():
	# Create the output directories if they do not exist
	if not os.path.isdir(METRICS_STATISTICS_DIRECTORY_PATH):
		os.mkdir(METRICS_STATISTICS_DIRECTORY_PATH)

# @brief: Gets the user input for the repository name and returns the path to the directory
# @param: None
# @return: The path to the directory
def get_directory_path():
	repository_name = input("Enter the repository name (String): ")
	directory_path = f"{CK_METRICS_DIRECTORY_PATH}/{repository_name}"

	# Check if the directory exists
	while not os.path.isdir(directory_path):
		print("The directory does not exist.")
		repository_name = input("Enter the repository name (String): ")
		directory_path = f"{CK_METRICS_DIRECTORY_PATH}/{repository_name}"

	return directory_path

# @brief: Processes a csv file containing the metrics of a method
# @param file_path: The path to the csv file
# @param method_metrics: A dictionary containing the metrics of each method
# @return: None
def process_csv_file(file_path, method_metrics):
	# Open the csv file
	with open(file_path, "r") as csvfile:
		# Read the csv file
		reader = csv.DictReader(csvfile)
		# Iterate through each row, that is, for each method in the csv file
		for row in reader:
			class_name = row["class"]
			method_name = row["method"]
			cbo = float(row["cbo"])
			cbo_modified = float(row["cboModified"])
			wmc = float(row["wmc"])
			rfc = float(row["rfc"])

			# Create a tuple containing the metrics
			metrics = (cbo, cbo_modified, wmc, rfc)
			method = f"{class_name} {method_name}"

			if method not in method_metrics: # if the method is not in the dictionary
				method_metrics[method] = {"metrics": [], "changed": 0}

			# Get the metrics_changes list for the method
			metrics_changes = method_metrics[method]["metrics"]

			# Try to find the same metrics in the list for the same method. If it does not exist, then add it to the list
			if metrics not in metrics_changes: # if the metrics are not in the list
				metrics_changes.append(metrics) # add the metrics values to the list
				method_metrics[method]["changed"] += 1 # increment the number of changes

# @brief: Traverses a directory and processes all the csv files
# @param directory_path: The path to the directory
# @return: A dictionary containing the metrics of each class and method combination
def traverse_directory(directory_path):
	method_metrics = {}
	file_count = 0
	progress_bar = None

	# Traverse the directory
	for root, dirs, files in os.walk(directory_path):
		# Iterate through each file in the directory and call the process_csv_file function to get the methods metrics of each file
		for file in files:
			# If the file is a csv file
			if file == CK_CSV_FILE:
				file_path = os.path.join(root, file) # Get the path to the csv file
				process_csv_file(file_path, method_metrics) # Process the csv file
				file_count += 1 # Increment the file count

				if progress_bar is None: # If the progress bar is not initialized
					progress_bar = tqdm(total=file_count) # Initialize the progress bar
				else:
					progress_bar.update(1) # Update the progress bar

	# Close the progress bar
	if progress_bar is not None:
		progress_bar.close()

	# Return the method metrics, which is a dictionary containing the metrics of each method  
	return method_metrics

# @brief: Calculates the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
# @param csv_writer: The csv writer object
# @param method: The method name
# @param metrics: The list of metrics
# @param metrics_values: The list of metrics values
# @return: None
def write_method_metrics_statistics(csv_writer, method_name, metrics, metrics_values):
	cboMin = round(float(min(metrics_values[0])), 3)
	cboMax = round(float(max(metrics_values[0])), 3)
	cboAvg = round(float(sum(metrics_values[0])) / len(metrics_values[0]), 3)
	cboThirdQuartile = round(float(np.percentile(metrics_values[0], 75)), 3)
	cbo_modifiedMin = round(float(min(metrics_values[1])), 3)
	cbo_modifiedMax = round(float(max(metrics_values[1])), 3)
	cbo_modifiedAvg = round(float(sum(metrics_values[1])) / len(metrics_values[1]), 3)
	cbo_modifiedThirdQuartile = round(float(np.percentile(metrics_values[1], 75)), 3)
	wmcMin = round(float(min(metrics_values[2])), 3)
	wmcMax = round(float(max(metrics_values[2])), 3)
	wmcAvg = round(float(sum(metrics_values[2])) / len(metrics_values[2]), 3)
	wmcThirdQuartile = round(float(np.percentile(metrics_values[2], 75)), 3)
	rfcMin = round(float(min(metrics_values[3])), 3)
	rfcMax = round(float(max(metrics_values[3])), 3)
	rfcAvg = round(float(sum(metrics_values[3])) / len(metrics_values[3]), 3)
	rfcThirdQuartile = round(float(np.percentile(metrics_values[3], 75)), 3)

	csv_writer.writerow([method_name, metrics["changed"], cboMin, cboMax, cboAvg, cboThirdQuartile, cbo_modifiedMin, cbo_modifiedMax, cbo_modifiedAvg, cbo_modifiedThirdQuartile, wmcMin, wmcMax, wmcAvg, wmcThirdQuartile, rfcMin, rfcMax, rfcAvg, rfcThirdQuartile])

# @brief: Process the metrics in method_metrics to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
# @param method_metrics: A dictionary containing the metrics of each method
# @return: None
def process_method_metrics(method_metrics):
	# Open the csv file and process the metrics of each method
	with open(TOP_CHANGED_FILES_CSV_FILE_PATH, "w") as csvfile:
		writer = csv.writer(csvfile)	
		writer.writerow(["Method", "Changed", "CBOMin", "CBOMax", "CBOAvg", "CBOThirdQuartile", "CBO ModifiedMin", "CBO ModifiedMax", "CBO ModifiedAvg", "CBO ModifiedThirdQuartile", "WMCMin", "WMCMax", "WMCAvg", "WMCThirdQuartile", "RFCMin", "RFCMax", "RFCAvg", "RFCThirdQuartile"])

		# Loop inside the *metrics["metrics"] in order to get the min, max, avg, and third quartile of each metric (cbo, cbo_modified, wmc, rfc)
		for method, metrics in method_metrics.items():
			# check if the metrics changes is greater than the minimum changes
			if metrics["changed"] < MINIMUM_CHANGES:
				continue

			# This stores the metrics values in a list of lists of each metric
			metrics_values = []
			for i in range(0, NUMBER_OF_METRICS):
				# This get the metrics values of each metric occurence in the method in order to, later on, be able to get the min, max, avg, and third quartile of each metric
				metrics_values.append([sublist[i] for sublist in metrics["metrics"]])

			# Create a function to get the min, max, avg, and third quartile of each metric and then write it to the csv file
			write_method_metrics_statistics(writer, method, metrics, metrics_values)

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
	# Get the directory path from user input of the repository name
	directory_path = get_directory_path()

	# Create the output directories if they do not exist
	create_output_directories()

	# Traverse the directory and get the method metrics
	method_metrics = traverse_directory(directory_path)

	# Process the method metrics to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
	process_method_metrics(method_metrics)

	# Sort the csv file by the number of changes
	sort_csv_by_changes()

	# Remove the old csv file
	os.remove(TOP_CHANGED_FILES_CSV_FILE_PATH)

# Directive to run the main function
if __name__ == "__main__":
	main() # Call the main function