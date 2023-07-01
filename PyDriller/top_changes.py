import os # for walking through directories
import csv # for reading csv files
import numpy as np # for calculating the min, max, avg, and third quartile of each metric
import pandas as pd # for the csv file operations
from tqdm import tqdm # for progress bar

# CONSTANTS:
DEFAULT_CSV_FILE = "method.csv" # The default csv file name
MINIMUM_CHANGES = 2 # The minimum number of changes a method should have to be considered
TOP_CHANGED_METHODS_CSV_FILENAME = "top_changed_methods.csv" # The name of the csv file containing the top changed methods
SORTED_TOP_CHANGED_METHODS_CSV_FILENAME = "sorted_top_changed_methods.csv" # The name of the csv file containing the sorted top changed methods

# Relative paths
RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH = "/ck_metrics"
RELATIVE_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH = "/metrics_statistics"

# @brief: Gets the user input for the repository name and returns the path to the directory
# @param: None
# @return: The path to the directory
def get_directory_path():
	repository_name = input("Enter the repository name (String): ")
	directory_path = f"{RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH}/{repository_name}"

	while not os.path.isdir(directory_path):
		print("The directory does not exist.")
		repository_name = input("Enter the repository name (String): ")
		directory_path = f"{RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH}/{repository_name}"

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
			if file == DEFAULT_CSV_FILE:
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

# @brief: Gets the top changed methods
# @param method_metrics: A dictionary containing the metrics of each method
# @param num_methods: The number of methods to return
# @return: A list of tuples containing the method name and the metrics
def sort_top_changed_methods(method_metrics):
	# Sort the methods by the number of changes
	sorted_methods = sorted(method_metrics.items(), key=lambda x: x[1]["changed"], reverse=True)
	# Return the top num_methods methods
	return sorted_methods

# @brief: This function writes the top changed methods to a csv file
# @param top_changed_methods: A list of tuples containing the method name and the metrics
# @return: None
def write_top_changed_methods_to_csv(top_changed_methods):
	# Create the csv file
	with open("metrics_statistics/top_changed_methods.csv", "w") as csvfile:
		# Create the csv writer
		writer = csv.writer(csvfile)
		# Write the header
		writer.writerow(["Method", "Changed", "CBO", "CBO Modified", "WMC", "RFC"])
		# Write the rows
		for method, metrics in top_changed_methods:
			if metrics["changed"] == 1: # if the number of changes is 1, then go to the next method
				continue
			writer.writerow([method, metrics["changed"], *metrics["metrics"]])

# @brief: The main function
# @param: None
# @return: None
def main():
	# Get the directory path from user input of the repository name
	directory_path = get_directory_path()

	# Traverse the directory and get the method metrics
	# method_metrics = traverse_directory(directory_path)
	method_metrics = traverse_directory(directory_path)

	with open("junk/method_metrics.txt", "w") as file:
		file.write(str(method_metrics))

	# Get the top changed methods
	for method, metrics in method_metrics.items():
		with open("metrics_statistics/top_changed_methods.csv", "w") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(["Method", "Changes", "CBOMin", "CBOMax", "CBOAvg", "CBOThirdQuartile", "CBO ModifiedMin", "CBO ModifiedMax", "CBO ModifiedAvg", "CBO ModifiedThirdQuartile", "WMCMin", "WMCMax", "WMCAvg", "WMCThirdQuartile", "RFCMin", "RFCMax", "RFCAvg", "RFCThirdQuartile"])
			# writer.writerow([method, metrics["changes"], *metrics["metrics"]])
			# now make a loop inside the *metrics["metrics"] in order to get the min, max, avg, and third quartile of each metric (cbo, cbo_modified, wmc, rfc)
			# then print the results in the csv file
			for metric in metrics["metrics"]:
				# check if the metrics changes is 1, then return
				if metrics["changed"] == 1:
					continue
				print(f"metrics of {method}: {metric}")	
				cboMin = float(min(metric[0]))
				cboMax = float(max(metric[0]))
				cboAvg = float(sum(metric[0])) / len(metric[0])
				cboThirdQuartile = float(np.percentile(metric[0], 75))
				cbo_modifiedMin = float(min(metric[1]))
				cbo_modifiedMax = float(max(metric[1]))
				cbo_modifiedAvg = float(sum(metric[1])) / len(metric[1])
				cbo_modifiedThirdQuartile = float(np.percentile(metric[1], 75))
				wmcMin = float(min(metric[2]))
				wmcMax = float(max(metric[2]))
				wmcAvg = float(sum(metric[2])) / len(metric[2])
				wmcThirdQuartile = float(np.percentile(metric[2], 75))
				rfcMin = float(min(metric[3]))
				rfcMax = float(max(metric[3]))
				rfcAvg = float(sum(metric[3])) / len(metric[3])
				rfcThirdQuartile = float(np.percentile(metric[3], 75))
				writer.writerow([method, metrics["changed"], cboMin, cboMax, cboAvg, cboThirdQuartile, cbo_modifiedMin, cbo_modifiedMax, cbo_modifiedAvg, cbo_modifiedThirdQuartile, wmcMin, wmcMax, wmcAvg, wmcThirdQuartile, rfcMin, rfcMax, rfcAvg, rfcThirdQuartile])
				# cbo_modified = float(max(metric[1]))
				# wmc = metric[2]
				# rfc = metric[3]
				# writer.writerow([method, metrics["changes"], cbo, cbo_modified, wmc, rfc])

		# break
	# top_changed_methods = sort_top_changed_methods(method_metrics)
	# # Output the top changed methods
	# write_top_changed_methods_to_csv(top_changed_methods)

# Directive to run the main function
if __name__ == "__main__":
	main() # Call the main function