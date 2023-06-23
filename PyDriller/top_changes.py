import os # for walking through directories
import csv # for reading csv files
from tqdm import tqdm # for progress bar

# @brief: Processes a csv file containing the metrics of a method
# @param file_path: The path to the csv file
# @param method_metrics: A dictionary containing the metrics of each method
# @return: None
def process_csv_file(file_path, method_metrics):
	metrics_changes = []
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
					metrics_changes.append(metrics) # add the metrics to the list
					method_metrics[method] = {"metrics": metrics_changes, "changes": 1}
			else: # if the method is in the dictionary
					if metrics not in metrics_changes: # if the metrics are not in the list
						metrics_changes.append(metrics) # add the metrics values to the list
						method_metrics[method]["changes"] += 1 # increment the number of changes

# @brief: Traverses a directory and processes all the csv files
# @param directory_path: The path to the directory
# @return: A dictionary containing the metrics of each class and method combination
def traverse_directory(directory_path):
	method_metrics = {}
	file_count = 0
	progress_bar = None
	
	# Traverse the directory
	for root, dirs, files in os.walk(directory_path):
		# Iterate through each file in the directory and call the process_csv_file function to get the methods metrics of each file in each file
		for file in files:
			# If the file is a csv file
			if file == "method.csv":
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
	sorted_methods = sorted(method_metrics.items(), key=lambda x: x[1]["changes"], reverse=True)
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
		writer.writerow(["Method", "Changes", "CBO", "CBO Modified", "WMC", "RFC"])
		# Write the rows
		for method, metrics in top_changed_methods:
			if metrics["changes"] == 1: # if the number of changes is 1, then
				return 
			writer.writerow([method, metrics["changes"], *metrics["metrics"]])

# @brief: The main function
# @param: None
# @return: None
def main():
	repository_name = input("Enter the repository name (String): ")
	directory_path = f"ck_metrics/{repository_name}"

	while not os.path.isdir(directory_path):
		print("The directory does not exist.")
		repository_name = input("Enter the repository name (String): ")
		directory_path = f"ck_metrics/{repository_name}"

	# Traverse the directory and get the method metrics
	method_metrics = traverse_directory(directory_path)
	# Get the top changed methods
	# print the first method, its changes, and its metrics
	for method, metrics in method_metrics.items():
		with open("metrics_statistics/top_changed_methods.csv", "w") as csvfile:
			writer = csv.writer(csvfile)
			writer.writerow(["Method", "Changes", "CBO", "CBO Modified", "WMC", "RFC"])
			writer.writerow([method, metrics["changes"], *metrics["metrics"]])
			# now make a loop inside the *metrics["metrics"] in order to get the min, max, avg, and third quartile of each metric (cbo, cbo_modified, wmc, rfc)
			# then print the results in the csv file
			for metric in metrics["metrics"]:	
				cbo = float(min(metric[0]))
				cbo_modified = float(max(metric[1]))
				wmc = metric[2]
				rfc = metric[3]
				writer.writerow([method, metrics["changes"], cbo, cbo_modified, wmc, rfc])

		break
	# top_changed_methods = sort_top_changed_methods(method_metrics)
	# # Output the top changed methods
	# write_top_changed_methods_to_csv(top_changed_methods)

# Directive to run the main function
if __name__ == "__main__":
	main() # Call the main function