import os # OS module in Python provides functions for interacting with the operating system
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
import statistics # The statistics module provides functions for calculating mathematical statistics of numeric (Real-valued) data
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from tqdm import tqdm # TQDM is a progress bar library with good support for nested loops and Jupyter/IPython notebooks.
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
import matplotlib.pyplot as plt # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
from colorama import Style # For coloring the terminal

# Import from the main.py file
from main import backgroundColors
        
# Default paths:
PATH = os.getcwd() # Get the current working directory
PROCESS_CLASSES = input(f"{backgroundColors.OKGREEN}Do you want to process the {backgroundColors.OKCYAN}class.csv{backgroundColors.OKGREEN} file? {backgroundColors.OKCYAN}(True/False){backgroundColors.OKGREEN}: {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file

# Filenames:
CK_CSV_FILE = "class.csv" if PROCESS_CLASSES else "method.csv" # The name of the csv generated file from ck.
 
# Relative paths:
RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH = "/ck_metrics"
RELATIVE_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH = "/metrics_evolution"
RELATIVE_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH = "/metrics_statistics"
RELATIVE_REPOSITORY_DIRECTORY_PATH = "/repositories"
RELATIVE_CK_JAR_PATH = "/ck/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

# Default values:
DEFAULT_FOLDER = PATH # Get the current working directory
DEFAULT_REPOSITORY_NAME = "commons-lang"
DEFAULT_METHODS_NAME = ["testBothArgsNull/0"]
FULL_CK_METRICS_OUTPUT_DIRECTORY_PATH = PATH + RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH
FULL_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH = PATH + RELATIVE_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH
FULL_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH = PATH + RELATIVE_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH
FULL_REPOSITORY_DIRECTORY_PATH = PATH + RELATIVE_REPOSITORY_DIRECTORY_PATH
FULL_CK_JAR_PATH = PATH + RELATIVE_CK_JAR_PATH

# @brief: This function is used to check if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Check if the PATH constant contains whitespaces
   if " " in PATH:
      print(f"{backgroundColors.FAIL}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return True
   return False

# @brief: This function asks for the user input of the repository name
# @param: None
# @return: repository_name: Name of the repository to be analyzed
def get_repository_name_user():
   # Ask for user input of the repository name
   repository_name = input(f"{backgroundColors.OKGREEN}Enter the repository name {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

   # If empty, get from the default repository url
   if not repository_name:
      repository_name = DEFAULT_REPOSITORY_NAME
      print(f"{backgroundColors.OKGREEN}Using the default repository name: {backgroundColors.OKCYAN}{repository_name}{Style.RESET_ALL}")

   # Return the repository name
   return repository_name

# @brief: This verifies if all the metrics are already calculated
# @param: repository_name: Name of the repository to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def check_metrics_folders(repository_name):
   print(f"{backgroundColors.OKGREEN}Checking if all the metrics are already calculated{Style.RESET_ALL}")
   current_path = PATH
   data_path = os.path.join(current_path, "ck_metrics")
   repo_path = os.path.join(data_path, repository_name)
   commit_file = f"commit_hashes-{repository_name}.txt"
   commit_file_path = os.path.join(data_path, commit_file)

   if not os.path.exists(commit_file_path):
      print(f"{backgroundColors.FAIL}File {backgroundColors.OKCYAN}{commit_file}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{data_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
      return False

   with open(commit_file_path, "r") as file:
      lines = file.readlines()

   for line in lines:
      folder_name = line.strip()
      folder_path = os.path.join(repo_path, folder_name)

      if not os.path.exists(folder_path):
         print(f"{backgroundColors.FAIL}Folder {backgroundColors.OKCYAN}{folder_name}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{repo_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
         return False
   return True

# @brief: Create a subdirectory
# @param: full_directory_name: Name of the directory to be created
# @param: relative_directory_name: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_name, relative_directory_name):
   if os.path.isdir(full_directory_name): # Check if the directory already exists
      print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory already exists{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_name)
      print (f"{backgroundColors.OKGREEN}Successfully created the {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print(f"{backgroundColors.OKGREEN}The creation of the {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory failed{Style.RESET_ALL}")

# brief: Get user method name input
# param: None
# return: method_name: Name of the method to be analyzed
def get_user_method_input():
   # Ask for user input of the method name
   method_name = input(f"{backgroundColors.OKGREEN}Enter the method name {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

   # If empty, get from the method_names list
   if not method_name:
      method_name = DEFAULT_METHODS_NAME
      print(f"{backgroundColors.OKGREEN}Using the default stored names: {backgroundColors.OKCYAN}{method_name}{Style.RESET_ALL}")

   print()
   # Return the method name
   return method_name

# @brief: This function is analyze the repository metrics evolution over time
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def search_method_metrics(repository_name, method_name):
   print(f"{backgroundColors.OKGREEN}Analyzing the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository for the {backgroundColors.OKCYAN}{method_name}{backgroundColors.OKGREEN} method...{Style.RESET_ALL}")

   metrics_track_record = [] # Dictionary to store the metrics track records
   metrics_changes = [] # List to store the metrics of the method or class
   method_variables_counter = 0 # Counter to store the number of variables of the method

   # Get the list of commit hashes
   commit_hashes = os.listdir(f"ck_metrics/{repository_name}/")
   
   for commit_hash in tqdm(commit_hashes):
      method_path = f"ck_metrics/{repository_name}/{commit_hash}/{CK_CSV_FILE}"

      # Check if the method file exists for the current commit hash
      if os.path.isfile(method_path):
         with open(method_path, "r") as file:
            reader = csv.DictReader(file) # Read the CK_CSV_FILE file
            
            # Search for the method in the current commit's method.csv file
            for row in reader:
               if row["method"] == method_name:
                  current_metrics = (float(row["cbo"]), float(row["cboModified"]), float(row["wmc"]), float(row["rfc"]))
                  current_attributes = (commit_hash, float(row["cbo"]), float(row["cboModified"]), float(row["wmc"]), float(row["rfc"]))

                  # Store the metrics if they aren't in the metrics_track_records dictionary
                  if current_metrics not in metrics_changes:
                     metrics_changes.append(current_metrics)
                     metrics_track_record.append(current_attributes)
                     method_variables_counter += 1

   # If the data is empty, then the method was not found
   if not metrics_track_record:
      print(f"{backgroundColors.FAIL}Method {backgroundColors.OKCYAN}{method_name}{backgroundColors.FAIL} not found{Style.RESET_ALL}")
      return
   
   print(f"{backgroundColors.OKGREEN}The method {backgroundColors.OKCYAN}{method_name}{backgroundColors.OKGREEN} changed {backgroundColors.OKCYAN}{method_variables_counter} of {method_variables_counter}{backgroundColors.OKGREEN} time(s){Style.RESET_ALL}")

   # Write the method_data to a file in the /metrics_evolution folder
   # remove everything that comes before the / in the method_name
   output_file = f"metrics_evolution/{repository_name}-{str(method_name.split('/')[0:-1])[2:-2]}.csv"
   with open(output_file, 'w') as file:
      writer = csv.writer(file)
      writer.writerow([f"commit_hash", "cbo", "cboModified", "wmc", "rfc"])
      writer.writerows(metrics_track_record)
   print(f"{backgroundColors.OKGREEN}Successfully wrote the method evolution to {backgroundColors.OKCYAN}{output_file}{Style.RESET_ALL}")

# @brief: Main function
# @param: None
# @return: None
def main(): 
   # check if the path constants contains whitespaces
   if path_contains_whitespaces():
      return
   
   # Get the name of the repository from the user
   repository_name = get_repository_name_user()

   # Check if the metrics were already calculated
   if not check_metrics_folders(repository_name):
      print(f"{backgroundColors.FAIL}The metrics for {backgroundColors.OKCYAN}{repository_name}{backgroundColors.FAIL} were not calculated. Please run the main.py file first{Style.RESET_ALL}")
      return
   
   # create the metrics_evolution directory
   create_directory(FULL_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH, RELATIVE_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH)

   # create the metrics_statistics directory
   create_directory(FULL_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH, RELATIVE_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH)

   # Get the methods from the user
   methods = get_user_method_input()

   # Make a for loop to run the search_method_metrics and calculate_statistics function for every method in the user input
   for method in methods:
      if "/" in method:
         method_processed = str(method.split('/')[0:-1])[2:-2]
      print(f"{backgroundColors.OKGREEN}Calculating metrics evolution for {backgroundColors.OKCYAN}{method_processed}{Style.RESET_ALL}")
      # Calculate the CBO and WMC metrics evolution for the given method
      search_method_metrics(repository_name, method)

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function