import os # for walking through directories
import csv # for reading csv files
import numpy as np # for calculating the min, max, avg, and third quartile of each metric
import pandas as pd # for the csv file operations
import matplotlib.pyplot as plt # for plotting the graphs
import atexit # For playing a sound when the program finishes
import platform # For getting the operating system name
import time # For measuring the time
from tqdm import tqdm # for progress bar
from sklearn.linear_model import LinearRegression # for the linear regression
from sklearn.model_selection import train_test_split # for splitting the data into training and testing
from colorama import Style # For coloring the terminal

# Import from the main.py file
from ck_metrics import backgroundColors # For coloring the terminal outputs

# CONSTANTS:
PATH = os.getcwd() # Get the current working directory
PROCESS_CLASSES = input(f"{backgroundColors.GREEN}Do you want to process the {backgroundColors.CYAN}class.csv{backgroundColors.GREEN} file {backgroundColors.RED}(True/False){backgroundColors.GREEN}? {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file
MINIMUM_CHANGES = 1 # The minimum number of changes a method should have to be considered
NUMBER_OF_METRICS = 4 # The number of metrics
DEFAULT_REPOSITORY_NAME = ["commons-lang", "jabref", "kafka", "zookeeper"] # The default repository names
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The sound commands for each operating system
METRICS_POSITION = {"CBO": 0, "CBOModified": 1, "WMC": 2, "RFC": 3}

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

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
RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH = "/metrics_predictions" # The relative path to the directory containing the metrics prediction
SOUND_FILE = "../.assets/NotificationSound.wav" # The path to the sound file

# Directories Paths:
FULL_CK_METRICS_DIRECTORY_PATH = f"{PATH}{RELATIVE_CK_METRICS_DIRECTORY_PATH}" # The full path to the directory containing the ck metrics
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = f"{PATH}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}" # The full path to the directory containing the metrics evolution
FULL_METRICS_STATISTICS_DIRECTORY_PATH = f"{PATH}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}" # The full path to the directory containing the metrics statistics
FULL_METRICS_PREDICTION_DIRECTORY_PATH = f"{PATH}{RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH}" # The full path to the directory containing the metrics prediction

# @brief: This function is used to check if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Verify if the PATH constant contains whitespaces
   if " " in PATH: 
      return True # Return True if the PATH constant contains whitespaces
   return False # Return False if the PATH constant does not contain whitespaces

# @brief: Verifiy if the attribute is empty. If so, set it to the default value
# @param: attribute: The attribute to be checked
# @param: default_attribute_value: The default value of the attribute
# @return: The repository URL and the output directory
def validate_attribute(attribute, default_attribute_value):
   if not attribute: # Verify if the attribute is empty
      print(f"{backgroundColors.YELLOW}The attribute is empty! Using the default value: {backgroundColors.CYAN}{default_attribute_value}{Style.RESET_ALL}")
      attribute = default_attribute_value # Set the attribute to the default value
   return attribute

# @brief: Gets the user input for the repository name and returns the path to the directory
# @param: None
# @return: A tuple containing the repository name and the path to the directory
def get_directory_path():
	repository_name = input(f"{backgroundColors.GREEN}Enter the repository name {backgroundColors.CYAN}(String){backgroundColors.GREEN}: {Style.RESET_ALL}")
	repository_name = validate_attribute(repository_name, DEFAULT_REPOSITORY_NAME[0]) # Validate the repository name
	
	directory_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}"

	# Verify if the directory does not exist
	while not os.path.isdir(directory_path):
		print(f"{backgroundColors.RED}The directory does not exist. Please try again.{Style.RESET_ALL}")
		repository_name = input(f"{backgroundColors.GREEN}Enter the repository name {backgroundColors.CYAN}(String){backgroundColors.GREEN}: {Style.RESET_ALL}")
		directory_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}"

	return repository_name, directory_path

# @brief: This verifies if all the ck metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: repository_name: Name of the repository to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def verify_ck_metrics_folders(repository_name):
	print(f"{backgroundColors.GREEN}Checking if all the {backgroundColors.CYAN}CK metrics{backgroundColors.GREEN} are already calculated for the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository...{Style.RESET_ALL}")
	current_path = PATH
	data_path = os.path.join(current_path, RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]) # Join the current path with the relative path of the ck metrics directory
	commit_file = f"{repository_name}-commit_hashes{CSV_FILE_EXTENSION}" # The name of the commit hashes file
	commit_file_path = os.path.join(data_path, commit_file) # Join the data path with the commit hashes file

	# Verify if the repository exists
	if not os.path.exists(commit_file_path):
		print(f"{backgroundColors.RED}File {backgroundColors.CYAN}{commit_file}{backgroundColors.RED} does not exist inside {backgroundColors.CYAN}{data_path}{backgroundColors.RED}.{Style.RESET_ALL}")
		return False # Return False if the repository does not exist

	# Read the commit hashes file with pandas and get only the "commit_hash" column
	commit_hashes = pd.read_csv(commit_file_path)["commit hash"].tolist()

	repo_path = os.path.join(data_path, repository_name) # Join the data path with the repository name
	# Verify if the repository exists
	for commit_hash in commit_hashes:
		folder_path = os.path.join(repo_path, commit_hash) # Join the repo path with the commit hash

		if not os.path.exists(folder_path): # Verify if the folder exists
			print(f"{backgroundColors.RED}Folder {backgroundColors.CYAN}{commit_hash}{backgroundColors.RED} does not exist inside {backgroundColors.CYAN}{repo_path}{backgroundColors.RED}.{Style.RESET_ALL}")
			return False # Return False if the folder does not exist
		
	print(f"{backgroundColors.GREEN}All the {backgroundColors.CYAN}CK metrics{backgroundColors.GREEN} are already calculated for the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository.{Style.RESET_ALL}")
	return True # Return True if all the metrics are already calculated

# @brief: Create a directory
# @param: full_directory_name: Name of the directory to be created
# @param: relative_directory_name: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_name, relative_directory_name):
   if os.path.isdir(full_directory_name): # Verify if the directory already exists
      print(f"{backgroundColors.GREEN}The {backgroundColors.CYAN}{relative_directory_name}{backgroundColors.GREEN} directory already exists{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_name)
      print (f"{backgroundColors.GREEN}Successfully created the {backgroundColors.CYAN}{relative_directory_name}{backgroundColors.GREEN} directory{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print (f"{backgroundColors.GREEN}The creation of the {backgroundColors.CYAN}{relative_directory_name}{backgroundColors.GREEN} directory failed{Style.RESET_ALL}")

# @brief: This function create all the desired directories
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def create_directories(repository_name):
	# Create the output RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH directory if it does not exist
	create_directory(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH)
	# Create the output RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH directory if it does not exist
	create_directory(FULL_METRICS_STATISTICS_DIRECTORY_PATH, RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH)
	# Create the output RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH directory if it does not exist
	create_directory(FULL_METRICS_PREDICTION_DIRECTORY_PATH, RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH)
	# Create the metrics evolution output repository_name directory if it does not exist
	create_directory(FULL_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS, RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS) # Create the directory where the csv file will be stored
	# Create the metrics statistics output repository_name directory if it does not exist
	create_directory(FULL_METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name, RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name)
	# Create the metrics prediction output repository_name directory if it does not exist
	create_directory(FULL_METRICS_PREDICTION_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS, RELATIVE_METRICS_PREDICTION_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS)

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
				metrics_track_record[identifier] = {"metrics": [], "commit_hashes": [], "changed": 0}

			# Get the metrics_changes list for the method
			metrics_changes = metrics_track_record[identifier]["metrics"]
			# Get the commit hashes list for the method
			commit_hashes = metrics_track_record[identifier]["commit_hashes"]

			# Try to find the same metrics in the list for the same method. If it does not exist, then add it to the list
			if metrics not in metrics_changes: # if the metrics are not in the list
				metrics_changes.append(metrics) # add the metrics values to the list
				metrics_track_record[identifier]["changed"] += 1 # increment the number of changes
				commit_hash = file_path[file_path.rfind("/", 0, file_path.rfind("/")) + 1:file_path.rfind("/")]
				commit_hashes.append(commit_hash) # add the commit hash to the list

# @brief: Traverses a directory and processes all the csv files
# @param directory_path: The path to the directory
# @return: A dictionary containing the metrics of each class and method combination
def traverse_directory(directory_path):
	print(f"{backgroundColors.GREEN}Traversing the {backgroundColors.CYAN}{'/'.join(directory_path.rsplit('/', 2)[-2:])}{backgroundColors.GREEN} directory...{Style.RESET_ALL}")
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

# @brief: This function receives an id and verify if it contains slashes, if so, it returns the id without the slashes
# @param: id: ID of the class or method to be analyzed
# @return: ID of the class or method to be analyzed without the slashes
def get_clean_id(id):
   # If the id contains slashes, remove them
   if "/" in id:
      return str(id.split("/")[0:-1])[2:-2]
   else:
      return id
   
# @brief: Perform linear regression on the given metrics and save the plot to a PNG file
# @param: metrics: A list containing the metrics values for linear regression
# @param: filename: The filename for the PNG plot
# @param: repository_name: The name of the repository
# @param: progress_status: The progress status
# @return: None
def linear_regression_predictions(metrics, filename, repository_name, progress_status):
	print(f"{backgroundColors.GREEN}Linear Regression {progress_status}{backgroundColors.GREEN} for the {backgroundColors.CYAN}{filename} {CK_CSV_FILE.replace('.csv', '')}{backgroundColors.GREEN} in the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository...{Style.RESET_ALL}")
	# Check for empty metrics list
	if not metrics:
		print(f"{backgroundColors.RED}Metrics list is empty!{Style.RESET_ALL}")
		return

	# Check for invalid values in the metrics
	if np.isnan(metrics).any() or np.isinf(metrics).any():
		print(f"{backgroundColors.RED}Metrics list contains invalid values (NaN or inf)!{Style.RESET_ALL}")
		return
	
	# Loop through the metrics_position dictionary
	for key, value in METRICS_POSITION.items():
		# Extract the metrics values
		x = np.arange(len(metrics))
		y = np.array(metrics)[:, value] # Considering the metric in the value variable for linear regression

		# Check for sufficient data points for regression
		if len(x) < 2 or len(y) < 2:
			return
		
		# Perform linear regression using numpy.polyfit
		coeffs = np.polyfit(x, y, deg=1)
		linear_fit = coeffs[1] + coeffs[0] * x

		# Create the plot
		plt.figure(figsize=(10, 6))
		plt.plot(x, y, "o", label=f"{key}")
		plt.plot(x, linear_fit, "-", label="Linear Regression Fit")
		plt.xlabel("Commit Number")
		plt.ylabel(f"{key} Value")
		plt.title(f"Linear Regression for {key} metric of {filename}")
		plt.legend()

		class_name = filename.split(' ')[0] # Get the class name
		variable_attribute = get_clean_id(filename.split(" ")[1]) # Get the variable attribute which could be the type of the class or the method name

		# Create the Class/Method linear prediction directory if it does not exist
		if not os.path.exists(f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}"):
			os.makedirs(f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}")

		# Save the plot to a PNG file
		plt.savefig(f"{FULL_METRICS_PREDICTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}/{key}.png")
		plt.close()
   
# @brief: This function writes the metrics evolution to a csv file
# @param: repository_name: The name of the repository
# @param: metrics_track_record: A dictionary containing the metrics of each method or class
# @return: None
def write_metrics_evolution_to_csv(repository_name, metrics_track_record):
	print(f"{backgroundColors.GREEN}Writing the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} metrics track record to a csv file inside {backgroundColors.CYAN}{RELATIVE_CK_METRICS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}{backgroundColors.GREEN}...{Style.RESET_ALL}")
	progress_counter = 0
	# For every identifier in the metrics_track_record, store each metrics values tuple in a row of the csv file
	for identifier, record in metrics_track_record.items():
		metrics = record["metrics"]
		class_name = identifier.split(' ')[0] # Get the identifier which is currently the class name
		variable_attribute = get_clean_id(identifier.split(" ")[1]) # Get the variable attribute which could be the type of the class or the method name
		filename = f"{class_name} {variable_attribute}" # The filename of the csv file without the file extension
		with open(FULL_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + filename + CSV_FILE_EXTENSION, "w") as csvfile:
			writer = csv.writer(csvfile)
			if PROCESS_CLASSES:
				unique_identifier = class_name
				writer.writerow(["Class", "Commit Hash", "CBO", "CBO Modified", "WMC", "RFC"])
			else:
				unique_identifier = variable_attribute
				writer.writerow(["Method", "Commit Hash", "CBO", "CBO Modified", "WMC", "RFC"])
			
			# get the len of the metrics list
			metrics_len = len(metrics)
			for i in range(metrics_len):
				writer.writerow([unique_identifier, record["commit_hashes"][i], metrics[i][0], metrics[i][1], metrics[i][2], metrics[i][3]])
		progress_counter += 1
		progress_status = f"{backgroundColors.CYAN}{progress_counter}{backgroundColors.GREEN} of {backgroundColors.CYAN}{len(metrics_track_record)}{Style.RESET_ALL}"
		linear_regression_predictions(metrics, filename, repository_name, progress_status) # Update the filename to remove the csv file extension

	print(f"{backgroundColors.GREEN}Finished writing the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} metrics track record to a csv file inside {backgroundColors.CYAN}{RELATIVE_CK_METRICS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}{Style.RESET_ALL}")

# @brief: Calculates the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
# @param csv_writer: The csv writer object
# @param id: The id of the method
# @param key: The key of the method
# @param metrics: The list of metrics
# @param metrics_values: The list of metrics values
# @param first_commit_hash: The first commit hash of the method
# @param last_commit_hash: The last commit hash of the method
# @return: None
def write_method_metrics_statistics(csv_writer, id, key, metrics, metrics_values, first_commit_hash, last_commit_hash):
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

	csv_writer.writerow([id, key, metrics["changed"], cboMin, cboMax, cboAvg, cboQ3, cboModifiedMin, cboModifiedMax, cboModifiedAvg, cboModifiedQ3, wmcMin, wmcMax, wmcAvg, wmcQ3, rfcMin, rfcMax, rfcAvg, rfcQ3, first_commit_hash, last_commit_hash])

# @brief: Process the metrics in metrics_track_record to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
# @param repository_name: The name of the repository
# @param metrics_track_record: A dictionary containing the metrics of each method or class
# @return: None
def process_metrics_track_record(repository_name, metrics_track_record):
	# Open the csv file and process the metrics of each method
	with open(FULL_METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "/" + CHANGED_METHODS_CSV_FILENAME, "w") as csvfile:
		writer = csv.writer(csvfile)	
		if PROCESS_CLASSES:
			writer.writerow(["Class", "Type", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "CBOModified Min", "CBOModified Max", "CBOModified Avg", "CBOModified Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3", "First Commit Hash", "Last Commit Hash"])
		else:
			writer.writerow(["Class", "Method", "Changed", "CBO Min", "CBO Max", "CBO Avg", "CBO Q3", "CBOModified Min", "CBOModified Max", "CBOModified Avg", "CBOModified Q3", "WMC Min", "WMC Max", "WMC Avg", "WMC Q3", "RFC Min", "RFC Max", "RFC Avg", "RFC Q3", "First Commit Hash", "Last Commit Hash"])

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

			# Create a function to get the min, max, avg, and third quartile of each metric, the first commit hash and the last commit hash, and then write it to the csv file
			write_method_metrics_statistics(writer, id, key, metrics, metrics_values, metrics_track_record[identifier]["commit_hashes"][0], metrics_track_record[identifier]["commit_hashes"][-1])

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
	print(f"{backgroundColors.CYAN}Successfully sorted{backgroundColors.GREEN} the {backgroundColors.CYAN}{CLASSES_OR_METHODS}{backgroundColors.GREEN} by the {backgroundColors.CYAN}number of times they changed{backgroundColors.GREEN} and {backgroundColors.CYAN}stored{backgroundColors.GREEN} inside the {backgroundColors.CYAN}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}{backgroundColors.GREEN} directory.{Style.RESET_ALL}")

# @brief: This function defines the command to play a sound when the program finishes
# @param: None
# @return: None
def play_sound():
	if os.path.exists(SOUND_FILE):
		if platform.system() in SOUND_COMMANDS: # if the platform.system() is in the SOUND_COMMANDS dictionary
			os.system(f"{SOUND_COMMANDS[platform.system()]} {SOUND_FILE}")
		else: # if the platform.system() is not in the SOUND_COMMANDS dictionary
			print(f"{backgroundColors.RED}The {backgroundColors.CYAN}platform.system(){backgroundColors.RED} is not in the {backgroundColors.CYAN}SOUND_COMMANDS dictionary{backgroundColors.RED}. Please add it!{Style.RESET_ALL}")
	else: # if the sound file does not exist
		print(f"{backgroundColors.RED}Sound file {backgroundColors.CYAN}{SOUND_FILE}{backgroundColors.RED} not found. Make sure the file exists.{Style.RESET_ALL}")

# Register the function to play a sound when the program finishes
atexit.register(play_sound)

# @brief: This function outputs time, considering the appropriate time unit
# @param: output_string: String to be outputted
# @param: time: Time to be outputted
# @return: None
def output_time(output_string, time):
   if float(time) < int(TIME_UNITS[0]):
      time_unit = "seconds"
      time_value = time
   elif float(time) < float(TIME_UNITS[1]):
      time_unit = "minutes"
      time_value = time / TIME_UNITS[0]
   elif float(time) < float(TIME_UNITS[2]):
      time_unit = "hours"
      time_value = time / TIME_UNITS[1]
   else:
      time_unit = "days"
      time_value = time / TIME_UNITS[2]

   rounded_time = round(time_value, 2)
   print(f"{backgroundColors.GREEN}{output_string}{backgroundColors.CYAN}{rounded_time} {time_unit}{Style.RESET_ALL}")

# @brief: The main function
# @param: None
# @return: None
def main():
	start_time = time.time() # Start the timer
	# check if the path constants contains whitespaces
	if path_contains_whitespaces():
		print(f"{backgroundColors.RED}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
		return

	print(f"{backgroundColors.GREEN}This script {backgroundColors.CYAN}generates the csv files{backgroundColors.GREEN} with the {backgroundColors.CYAN}{CLASSES_OR_METHODS} metrics values{backgroundColors.GREEN} for {backgroundColors.CYAN}each commit hash{backgroundColors.GREEN} and store them inside the {backgroundColors.CYAN}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}/repository_name/commit_hash{backgroundColors.GREEN} directory.{Style.RESET_ALL}")
	print(f"{backgroundColors.GREEN}This script {backgroundColors.CYAN}generates a csv file{backgroundColors.GREEN} with the {backgroundColors.CYAN}{CLASSES_OR_METHODS} sorted{backgroundColors.GREEN} by the {backgroundColors.CYAN}number of times that the {CK_CSV_FILE.replace('.csv', '')} changed{backgroundColors.GREEN} and store it inside the {backgroundColors.CYAN}{RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH}{backgroundColors.GREEN} directory.{Style.RESET_ALL}")
	print(f"{backgroundColors.GREEN}The {backgroundColors.CYAN}source of the metrics values{backgroundColors.GREEN} is the {backgroundColors.CYAN}{CK_CSV_FILE}{backgroundColors.GREEN} files.{Style.RESET_ALL}")

	# Get the directory path from user input of the repository name
	repository_name, directory_path = get_directory_path()

	# Verify if the ck metrics were already calculated, which are the source of the data processed by traverse_directory(directory_path).
	if not verify_ck_metrics_folders(repository_name):
		print(f"{backgroundColors.RED}The metrics for {backgroundColors.CYAN}{repository_name}{backgroundColors.RED} were not calculated. Please run the ck_metrics.py file first{Style.RESET_ALL}")
		return
	
	# Create the desired directory if it does not exist
	create_directories(repository_name)

	# Traverse the directory and get the method metrics
	metrics_track_record = traverse_directory(directory_path)

	# Write, for each identifier, the metrics evolution values to a csv file
	write_metrics_evolution_to_csv(repository_name, metrics_track_record)

	# Process the method metrics to calculate the minimum, maximum, average, and third quartile of each metric and writes it to a csv file
	process_metrics_track_record(repository_name, metrics_track_record)

	# Sort the csv file by the number of changes
	sort_csv_by_changes(repository_name)

	# Remove the old csv file
	os.remove(FULL_METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "/" + CHANGED_METHODS_CSV_FILENAME)

	elapsed_time = time.time() - start_time
	elapsed_time_string = f"Time taken to generate the {backgroundColors.CYAN}metrics changes{backgroundColors.GREEN} for the {backgroundColors.CYAN}{CLASSES_OR_METHODS}{backgroundColors.GREEN} in {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
	output_time(elapsed_time_string, round(elapsed_time, 2))

# Directive to run the main function
if __name__ == "__main__":
	main() # Call the main function