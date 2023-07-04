# @TODO: Change the variables names and refactor to be more readable and generic (could be method or class)
# @TODO: Comment every line of code

import os # OS module in Python provides functions for interacting with the operating system
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
import statistics # The statistics module provides functions for calculating mathematical statistics of numeric (Real-valued) data
from tqdm import tqdm # TQDM is a progress bar library with good support for nested loops and Jupyter/IPython notebooks.
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
import matplotlib.pyplot as plt # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
from colorama import Style # For coloring the terminal

# Import from the main.py file
from main import backgroundColors
        
# Constants:
PATH = os.getcwd() # Get the current working directory
DEFAULT_FOLDER = PATH # Get the current working directory

# Changable constants:
CLASS_CSV_FILE = "class.csv" # The name of the csv generated file from ck.
METHOD_CSV_FILE = "method.csv" # The name of the csv generated file from ck.
PROCESS_CLASSES = input(f"{backgroundColors.OKGREEN}Do you want to process the {backgroundColors.OKCYAN}class.csv{backgroundColors.OKGREEN} file? {backgroundColors.OKCYAN}(True/False){backgroundColors.OKGREEN}: {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file
CK_CSV_FILE = CLASS_CSV_FILE if PROCESS_CLASSES else METHOD_CSV_FILE # The name of the csv generated file from ck.
DEFAULT_REPOSITORY_NAME = "commons-lang"
# DEFAULT_IDS = {"org.apache.commons.lang.StringUtils": "class"} # The default ids to be analyzed. It stores the class:type or method:class
DEFAULT_IDS = {"testBothArgsNull/0": "org.apache.commons.lang3.AnnotationUtilsTest", "suite/0": "org.apache.commons.lang.LangTestSuite"} # The default ids to be analyzed. It stores the class:type or method:class
 
# Relative paths:
RELATIVE_CK_METRICS_DIRECTORY_PATH = "/ck_metrics"
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "/metrics_evolution"
RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH = "/metrics_statistics"
RELATIVE_REPOSITORY_DIRECTORY_PATH = "/repositories"
RELATIVE_CK_JAR_PATH = "/ck/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

# Default values:
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = PATH + RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH
FULL_METRICS_STATISTICS_DIRECTORY_PATH = PATH + RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH

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
   print(f"{backgroundColors.OKGREEN}Checking if all the {backgroundColors.OKCYAN}CK metrics{backgroundColors.OKGREEN} are already calculated for the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository...{Style.RESET_ALL}")
   current_path = PATH
   data_path = os.path.join(current_path, RELATIVE_CK_METRICS_DIRECTORY_PATH[1:])
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

# @brief: Create a directory if it does not exist
# @param: full_directory_path: Name of the directory to be created
# @param: relative_directory_path: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_path, relative_directory_path):
   if os.path.isdir(full_directory_path): # Check if the directory already exists
      print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}{relative_directory_path}{backgroundColors.OKGREEN} directory already exists{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_path)
      print (f"{backgroundColors.OKGREEN}Successfully created the {backgroundColors.OKCYAN}{relative_directory_path}{backgroundColors.OKGREEN} directory{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print(f"{backgroundColors.OKGREEN}The creation of the {backgroundColors.OKCYAN}{relative_directory_path}{backgroundColors.OKGREEN} directory failed{Style.RESET_ALL}")

# brief: Get user method name input
# param: None
# return: id: Name of the method to be analyzed
def get_user_ids_input():
   # Ask for user input of the method name
   id = input(f"{backgroundColors.OKGREEN}Enter the id of the {CK_CSV_FILE.replace('.csv', '')} {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

   # If empty, get from the method_names list
   if not id:
      id = DEFAULT_IDS
      print(f"{backgroundColors.OKGREEN}Using the default stored {CK_CSV_FILE.replace('.csv', '')} names: {backgroundColors.OKCYAN}{list(id.keys())}{Style.RESET_ALL}")

   # Return the method name
   return id

# @brief: This function is analyze the repository metrics evolution over time
# @param: repository_name: Name of the repository to be analyzed
# @param: id_key: Name of the method to be analyzed
# @return: None
def search_id_metrics(repository_name, id_key):
   print(f"{backgroundColors.OKGREEN}Analyzing the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository for the {backgroundColors.OKCYAN}{id_key}{backgroundColors.OKGREEN} {CK_CSV_FILE.replace('.csv', '')}...{Style.RESET_ALL}")

   metrics_track_record = [] # Dictionary to store the metrics track records
   metrics_changes = [] # List to store the metrics of the method or class
   method_variables_counter = 0 # Counter to store the number of variables of the method

   # Get the list of commit hashes
   commit_hashes = os.listdir(f"{RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]}/{repository_name}/")
   
   for commit_hash in tqdm(commit_hashes):
      method_path = f"{RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]}/{repository_name}/{commit_hash}/{CK_CSV_FILE}"

      # Check if the method file exists for the current commit hash
      if os.path.isfile(method_path):
         with open(method_path, "r") as file:
            reader = csv.DictReader(file) # Read the CK_CSV_FILE file
            get_metrics = False # Flag to get the metrics of the method or class
            # Search for the id_key in the CK_CSV_FILE file
            for row in reader:
               if (CK_CSV_FILE == CLASS_CSV_FILE) and (row["class"] == id_key and row["type"] == DEFAULT_IDS[id_key]):
                     get_metrics = True
               elif (CK_CSV_FILE == METHOD_CSV_FILE) and (row["method"] == id_key and row["class"] == DEFAULT_IDS[id_key]):
                     get_metrics = True

               if get_metrics:
                  current_metrics = (float(row["cbo"]), float(row["cboModified"]), float(row["wmc"]), float(row["rfc"]))
                  current_attributes = (commit_hash, float(row["cbo"]), float(row["cboModified"]), float(row["wmc"]), float(row["rfc"]))

                  # Store the metrics if they aren't in the metrics_track_records dictionary
                  if current_metrics not in metrics_changes:
                     metrics_changes.append(current_metrics)
                     metrics_track_record.append(current_attributes)
                     method_variables_counter += 1
                  get_metrics = False

   # If the data is empty, then the method was not found
   if not metrics_track_record:
      print(f"{backgroundColors.FAIL}Method {backgroundColors.OKCYAN}{id_key}{backgroundColors.FAIL} not found{Style.RESET_ALL}")
      return
   
   print(f"{backgroundColors.OKGREEN}The {CK_CSV_FILE.replace('.csv', '')} {backgroundColors.OKCYAN}{id_key}{backgroundColors.OKGREEN} changed {backgroundColors.OKCYAN}{method_variables_counter} of {method_variables_counter}{backgroundColors.OKGREEN} time(s){Style.RESET_ALL}")

   # Write the method_data to a file in the /metrics_evolution folder
   output_file = f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH[1:]}/{repository_name}-{id_key}.csv" if PROCESS_CLASSES else f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH[1:]}/{repository_name}-{str(id_key.split('/')[0:-1])[2:-2]}.csv"
   with open(output_file, "w") as file:
      writer = csv.writer(file)
      writer.writerow([f"commit_hash", "cbo", "cboModified", "wmc", "rfc"])
      writer.writerows(metrics_track_record)
   print(f"{backgroundColors.OKGREEN}Successfully wrote the {CK_CSV_FILE.replace('.csv', '')} evolution to {backgroundColors.OKCYAN}{output_file}{Style.RESET_ALL}")

# @brief: This function is used to analyze the repository metrics evolution over time for the CSV files in the given directory
# @param: data_directory: Directory containing the CSV files to be analyzed
# @param: output_file: Name of the output file
# @return: None
def calculate_statistics(data_directory, output_file):
   print(f"{backgroundColors.OKGREEN}Calculating statistics from the CSV file in {backgroundColors.OKCYAN}{data_directory.split('/')[-1]}/{output_file.split('/')[-1]}{Style.RESET_ALL}")

   # Create the output file
   with open(output_file, "w", newline='') as csvfile:
      writer = csv.writer(csvfile) # Create a CSV writer
      # Write the header row
      writer.writerow(["File", "Metric", "Min", "Max", "Average", "Median", "Third Quartile"])

      # Iterate through the CSV files in the data_directory 
      for root, dirs, files in os.walk(data_directory):
         # Iterate through the files in the current data_directory 
         for file in files:
            # Check if the file is the desired CSV file
            if file == output_file.split('/')[-1]:
               file_path = os.path.join(root, file) # Get the full path of the file
               # Read the CSV file
               with open(file_path, "r") as csvfile:
                  reader = csv.reader(csvfile)
                  header = next(reader)  # Skip the header row

                  values = []
                  for row in reader:
                     values.append(row[1:]) # Append the second to the last value of the row to the values list

                  # For loop that runs trough the columns of the reader
                  for i in range(0, len(values[0])):
                     column_values = [float(row[i]) for row in values]
                     min_value = round(min(column_values), 3)
                     max_value = round(max(column_values), 3)
                     average = round(statistics.mean(column_values), 3)
                     median = round(statistics.median(column_values), 3)
                     third_quartile = round(statistics.median_high(column_values), 3)
                     writer.writerow([file_path, header[i + 1], min_value, max_value, average, median, third_quartile])
   print(f"{backgroundColors.OKGREEN}Successfully wrote the statistics to {backgroundColors.OKCYAN}{output_file}{Style.RESET_ALL}")

# @brief: This function creates the metrics evolution graphs fronm the RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH folder
# @param: repository_name: Name of the repository to be analyzed
# @param: id: ID of the method to be analyzed
# @param: clean_id: ID of the method to be analyzed without the / and the method name
# @return: None
def create_metrics_evolution_graphics(repository_name, id, clean_id):
   # Load the generated CSV files into a dataframe and save a plot of the evolution of the cbo, cboModified, wmc and rfc metrics
   df = pd.read_csv(RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH[1:] + "/" + repository_name + "-" + clean_id + ".csv")

   # Extract the metrics and commit hashes from the DataFrame
   commit_hashes = df["commit_hash"]
   metrics = ["cbo", "cboModified", "wmc", "rfc"]

   # Set color palette for the lines
   colors = ["blue", "red", "green", "black"]

   # Plotting the graph
   plt.figure(figsize=(10, 6))

   # Iterate over each metric and plot its evolution with a different color
   for i, metric in enumerate(metrics):
      plt.plot(commit_hashes, df[metric], marker="o", label=metric, color=colors[i])

   # Set the graph title and labels
   plt.title(f"Metrics Evolution of the {CK_CSV_FILE.replace('.csv', '')} named {id} in {repository_name} repository")
   plt.xlabel("Commit Hash")
   plt.ylabel("Metric Value")

   # Rotate the x-axis labels for better readability
   plt.xticks(rotation=0)

   # Add a legend
   plt.legend()

   # Add a grid
   plt.tight_layout()

   # Save the graph
   plt.savefig(FULL_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "-" + clean_id + ".png")

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
   create_directory(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH)

   # create the metrics_statistics directory
   create_directory(FULL_METRICS_STATISTICS_DIRECTORY_PATH, RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH)

   # Get the ids from the user
   ids = get_user_ids_input()

   # Make a for loop to run the search_id_metrics and calculate_statistics function for every method in the user input
   for id in ids: # Loop trough the ids items in the dictionary
      clean_id = id
      if "/" in id:
         clean_id = str(id.split("/")[0:-1])[2:-2]
      print(f"{backgroundColors.OKGREEN}Calculating metrics evolution for {backgroundColors.OKCYAN}{id} {backgroundColors.OKGREEN}{CK_CSV_FILE.replace('.csv', '')}{Style.RESET_ALL}")

      # Calculate the CBO and WMC metrics evolution for the given method
      search_id_metrics(repository_name, id)

      # Calculate the statistics for the CSV files in the metrics_evolution directory
      output_statistics_csv_file = RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH[1:] + "/" + repository_name + "-" + clean_id + ".csv"
      calculate_statistics(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, output_statistics_csv_file)

      # Create the metrics evolution graphs
      create_metrics_evolution_graphics(repository_name, id, clean_id)

   print(f"{backgroundColors.OKGREEN}Successfully calculated the metrics evolution for {backgroundColors.OKCYAN}{repository_name}->{list(ids.keys())}{Style.RESET_ALL}")

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function