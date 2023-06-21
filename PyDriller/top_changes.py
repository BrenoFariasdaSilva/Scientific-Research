import os # for walking through directories
import csv # for reading csv files
from tqdm import tqdm # for progress bar

# @brief: Processes a csv file containing the metrics of a method
# @param file_path: The path to the csv file
# @param method_metrics: A dictionary containing the metrics of each method
# @return: None
def process_csv_file(file_path, method_metrics):
	# Open the csv file
	with open(file_path, "r") as csvfile:
		# Read the csv file
		reader = csv.DictReader(csvfile)
		# Iterate through each row
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
					method_metrics[method] = {"metrics": metrics, "changes": 1}
			else: # if the method is in the dictionary
					if method_metrics[method]["metrics"] != metrics: # if the metrics are different
						method_metrics[method]["changes"] += 1 # increment the number of changes
						method_metrics[method]["metrics"] = metrics # update the metrics

# @brief: Traverses a directory and processes all the csv files
# @param directory_path: The path to the directory
# @return: A dictionary containing the metrics of each class and method combination
def traverse_directory(directory_path):
	method_metrics = {}
	file_count = 0
	progress_bar = None
	
	# Traverse the directory
	for root, dirs, files in os.walk(directory_path):
		# Iterate through each file
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
	print(f"Number of methods: {len(method_metrics)}")
	# Get the top changed methods
	top_changed_methods = sort_top_changed_methods(method_metrics)
	print(f"Number of methods with the most significant metric changes: {len(top_changed_methods)}")
	# Output the top changed methods
	write_top_changed_methods_to_csv(top_changed_methods)

# Directive to run the main function
if __name__ == "__main__":
	main() # Call the main function