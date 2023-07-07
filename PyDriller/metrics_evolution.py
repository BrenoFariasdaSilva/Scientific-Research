import os # OS module in Python provides functions for interacting with the operating system
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
from tqdm import tqdm # TQDM is a progress bar library with good support for nested loops and Jupyter/IPython notebooks.
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
from colorama import Style # For coloring the terminal

# Import from the main.py file
from ck_metrics import backgroundColors
        
# Constants:
PATH = os.getcwd() # Get the current working directory

# Changable constants:
CLASS_CSV_FILE = "class.csv" # The name of the csv generated file from ck.
METHOD_CSV_FILE = "method.csv" # The name of the csv generated file from ck.
PROCESS_CLASSES = input(f"{backgroundColors.OKGREEN}Do you want to process the {backgroundColors.OKCYAN}class.csv{backgroundColors.OKGREEN} file? {backgroundColors.OKCYAN}(True/False){backgroundColors.OKGREEN}: {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file
CK_CSV_FILE = CLASS_CSV_FILE if PROCESS_CLASSES else METHOD_CSV_FILE # The name of the csv generated file from ck.
CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # The name of the csv generated file from ck.
OPPOSITE_CK_CSV_FILE = METHOD_CSV_FILE if PROCESS_CLASSES else CLASS_CSV_FILE # The name of the csv generated file from ck.
DEFAULT_REPOSITORY_NAME = "commons-lang"
DEFAULT_CLASS_IDS = {"org.apache.commons.lang.StringUtils": "class"} # The default ids to be analyzed. It stores the class:type or method:class
DEFAULT_METHOD_IDS = {"testBothArgsNull/0": "org.apache.commons.lang3.AnnotationUtilsTest", "suite/0": "org.apache.commons.lang.LangTestSuite"} # The default ids to be analyzed. It stores the class:type or method:class
DEFAULT_IDS = DEFAULT_CLASS_IDS if PROCESS_CLASSES else DEFAULT_METHOD_IDS # The default ids to be analyzed. It stores the class:type or method:class
 
# Relative paths:
RELATIVE_CK_METRICS_DIRECTORY_PATH = "/ck_metrics"
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "/metrics_evolution"
RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH = "/metrics_statistics"

# Default values:
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = PATH + RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH

# @brief: This function is used to check if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Check if the PATH constant contains whitespaces
   if " " in PATH:
      return True
   return False

# @brief: Verifiy if the attribute is empty. If so, set it to the default value
# @param: attribute: The attribute to be checked
# @param: default_attribute_value: The default value of the attribute
# @return: The repository URL and the output directory
def validate_attribute(attribute, default_attribute_value):
   if not attribute:
      print(f"{backgroundColors.WARNING}The attribute is empty! Using the default value: {backgroundColors.OKCYAN}{default_attribute_value}{backgroundColors.WARNING}.{Style.RESET_ALL}")
      attribute = default_attribute_value
   return attribute

# @brief: This function asks for the user input of the repository name
# @param: None
# @return: repository_name: Name of the repository to be analyzed
def get_repository_name_user():
   # Ask for user input of the repository name
   repository_name = input(f"{backgroundColors.OKGREEN}Enter the repository name {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

   return validate_attribute(repository_name, DEFAULT_REPOSITORY_NAME) # Validate the repository name

# @brief: This verifies if all the metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: repository_name: Name of the repository to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def check_ck_metrics_folders(repository_name):
   print(f"{backgroundColors.OKGREEN}Checking if all the {backgroundColors.OKCYAN}CK metrics{backgroundColors.OKGREEN} are already calculated for the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository...{Style.RESET_ALL}")
   current_path = PATH
   data_path = os.path.join(current_path, RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]) # Join the current path with the relative path of the ck metrics directory
   repo_path = os.path.join(data_path, repository_name) # Join the data path with the repository name
   commit_file = f"commit_hashes-{repository_name}.txt" # The name of the commit hashes file
   commit_file_path = os.path.join(data_path, commit_file) # Join the data path with the commit hashes file

   # Check if the repository exists
   if not os.path.exists(commit_file_path):
      print(f"{backgroundColors.FAIL}File {backgroundColors.OKCYAN}{commit_file}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{data_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
      return False

   # Read the commit hashes file
   with open(commit_file_path, "r") as file:
      lines = file.readlines() # Read all the lines of the file and store them in a list

   # Check if the repository exists
   for line in lines:
      # Get the commit hash
      folder_name = line.strip() # Remove the \n from the line
      folder_path = os.path.join(repo_path, folder_name) # Join the repo path with the folder name

      if not os.path.exists(folder_path): # Check if the folder exists
         print(f"{backgroundColors.FAIL}Folder {backgroundColors.OKCYAN}{folder_name}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{repo_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
         return False
   return True

# @brief: Create a directory if it does not exist
# @param: full_directory_path: Name of the directory to be created
# @param: relative_directory_path: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_path, relative_directory_path):
   if os.path.isdir(full_directory_path): # Check if the directory already exists
      print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}{relative_directory_path}{backgroundColors.OKGREEN} directory already exists.{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_path)
      print (f"{backgroundColors.OKGREEN}Successfully created the {backgroundColors.OKCYAN}{relative_directory_path}{backgroundColors.OKGREEN} directory.{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print(f"{backgroundColors.OKGREEN}The creation of the {backgroundColors.OKCYAN}{relative_directory_path}{backgroundColors.OKGREEN} directory failed.{Style.RESET_ALL}")

# brief: Get user input of the name of the class or method to be analyzed
# param: None
# return: id: Name of the class or method to be analyzed
def get_user_ids_input():
   id = {}
   name = ""
   first_run = True
   while name == "" and first_run:
      first_run = False
      # Ask for user input of the class or method name
      name = input(f"{backgroundColors.OKGREEN}Enter the name of the {CK_CSV_FILE.replace('.csv', '')} {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")
      # if the CK_CSV_FILE is a class csv file, ask for the type of the class ('class' 'interface' 'innerclass' 'enum' 'anonymous')
      if CK_CSV_FILE == CLASS_CSV_FILE:
         value = input(f"{backgroundColors.OKGREEN}Enter the type of the {CK_CSV_FILE.replace('.csv', '')} {backgroundColors.OKCYAN}{id}{backgroundColors.OKGREEN} to be analyzed {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")
      # if the CK_CSV_FILE is a method csv file, ask for the name of the class of the method
      elif CK_CSV_FILE == METHOD_CSV_FILE:
         value = input(f"{backgroundColors.OKGREEN}Enter the {CK_CSV_FILE.replace('.csv', '')} name of the {backgroundColors.OKCYAN}{id}{backgroundColors.OKGREEN} to be analyzed {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

      # add the name and value to the id dictionary
      id[name] = value

   # If the id dictionary is empty, get from the DEFAULT_IDS constant
   if name == "" and not first_run:
      id = DEFAULT_IDS
      print(f"{backgroundColors.OKGREEN}Using the default stored {CK_CSV_FILE.replace('.csv', '')} names: {backgroundColors.OKCYAN}{', '.join(list(id.keys()))}{backgroundColors.OKGREEN}.{Style.RESET_ALL}")

   return id # Return the class or method name

# @brief: This function validates if the ids are as the same type as the files to be analyzed defined in CK_CSV_FILE according to PROCESS_CLASSES
# @param: ids: Dictionary containing the ids to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: True if the ids are valid, False otherwise
def validate_ids(ids, repository_name):
   # Get the path of the file containing the top changes of the classes
   repo_class_top_changes_file_path = RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH[1:] + "/" + repository_name + "-" + CK_CSV_FILE.replace('.csv', '').upper() + "-" + "sorted_changes.csv"
   # Check if the ids to be processed are classes
   if PROCESS_CLASSES:
      class_types = pd.read_csv(repo_class_top_changes_file_path)["Type"].unique()
      # Check if the ids are classes
      for id in ids.values():
         if id not in class_types:
            return False
   return True

# @brief: This function receives an id and verify if it contains slashes, if so, it returns the id without the slashes
# @param: id: ID of the class or method to be analyzed
# @return: ID of the class or method to be analyzed without the slashes
def get_clean_id(id):
   # If the id contains slashes, remove them
   if "/" in id:
      return str(id.split("/")[0:-1])[2:-2]
   else:
      return id

# @brief: This function is analyze the repository metrics evolution over time
# @param: repository_name: Name of the repository to be analyzed
# @param: id_key: Name of the class or method to be analyzed
# @param: clean_id: Name of the class or method to be analyzed without the slashes
# @return: True if the repository was analyzed successfully, False if the id_key was not found
def generate_metric_evolution_by_id(repository_name, id_key, clean_id):
   print(f"{backgroundColors.OKGREEN}Analyzing the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository for the {backgroundColors.OKCYAN}{id_key}{backgroundColors.OKGREEN} {CK_CSV_FILE.replace('.csv', '')}...{Style.RESET_ALL}")

   metrics_track_record = [] # Dictionary to store the metrics track records
   metrics_changes = [] # List to store the metrics of the class or method
   metrics_change_counter = 0 # Counter to store the number of times the metrics changed

   # Get the list of commit hashes
   commit_hashes = os.listdir(f"{RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]}/{repository_name}/")
   
   for commit_hash in tqdm(commit_hashes):
      file_path = f"{RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]}/{repository_name}/{commit_hash}/{CK_CSV_FILE}"

      # Check if the class or method file exists for the current commit hash
      if os.path.isfile(file_path):
         with open(file_path, "r") as file:
            reader = csv.DictReader(file) # Read the file
            get_metrics = False # Flag to get the metrics of the class or method
            # Search for the id_key in the CK_CSV_FILE file
            for row in reader:
               if (CK_CSV_FILE == CLASS_CSV_FILE) and (row["class"] == id_key and row["type"] == DEFAULT_IDS[id_key]):
                  get_metrics = True   
               elif (CK_CSV_FILE == METHOD_CSV_FILE) and (row["method"] == id_key and row["class"] == DEFAULT_IDS[id_key]):
                  get_metrics = True

               if get_metrics: # If the desired class or method was found
                  current_metrics = (float(row["cbo"]), float(row["cboModified"]), float(row["wmc"]), float(row["rfc"]))
                  current_attributes = (commit_hash, float(row["cbo"]), float(row["cboModified"]), float(row["wmc"]), float(row["rfc"]))

                  # Store the metrics if they aren't in the metrics_changes list
                  if current_metrics not in metrics_changes:
                     metrics_changes.append(current_metrics) # Store the metrics in the metrics_changes list
                     metrics_track_record.append(current_attributes) # Store the metrics in the metrics_track_record list
                     metrics_change_counter += 1 # Increment the metrics_change_counter
                  get_metrics = False

   # If the data is empty, then the class or method was not found
   if not metrics_track_record:
      return False
   
   print(f"{backgroundColors.OKGREEN}The {CK_CSV_FILE.replace('.csv', '')} {backgroundColors.OKCYAN}{id_key}{backgroundColors.OKGREEN} changed {backgroundColors.OKCYAN}{metrics_change_counter} of {metrics_change_counter}{backgroundColors.OKGREEN} time(s).{Style.RESET_ALL}")

   # Write the class or method_data to a file in the RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH folder
   output_file = f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH[1:]}/{repository_name}-{id_key}.csv" if PROCESS_CLASSES else f"{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH[1:]}/{repository_name}-{clean_id}.csv"
   with open(output_file, "w") as file:
      writer = csv.writer(file) # Create the writer
      writer.writerow([f"commit_hash", "cbo", "cboModified", "wmc", "rfc"]) # Write the header
      writer.writerows(metrics_track_record) # Write the metrics track record
   print(f"{backgroundColors.OKGREEN}Successfully wrote the {backgroundColors.OKCYAN}{id_key}{backgroundColors.OKGREEN} {CK_CSV_FILE.replace('.csv', '')} evolution to {backgroundColors.OKCYAN}{output_file}{backgroundColors.OKGREEN}.{Style.RESET_ALL}")

   return True

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
                  reader = csv.reader(csvfile) # Create a CSV reader
                  header = next(reader)  # Skip the header row

                  values = [] # List to store the values of the CSV file
                  for row in reader:
                     values.append(row[1:]) # Append the second to the last value of the row to the values list

                  # For loop that runs trough the columns of the reader. Each column represents a metric (cbo, cboModified, wmc, rfc)
                  for i in range(0, len(values[0])):
                     column_values = [float(row[i]) for row in values] # Get the values of the current column
                     min_value = round(min(column_values), 3) # Calculate the min value of the current column
                     max_value = round(max(column_values), 3) # Calculate the max value of the current column
                     average = round(statistics.mean(column_values), 3) # Calculate the average value of the current column
                     median = round(statistics.median(column_values), 3) # Calculate the median value of the current column
                     third_quartile = round(statistics.median_high(column_values), 3) # Calculate the third quartile value of the current column
                     writer.writerow([file_path, header[i + 1], min_value, max_value, average, median, third_quartile]) # Write the statistics to the output file
   print(f"{backgroundColors.OKGREEN}Successfully wrote the statistics to {backgroundColors.OKCYAN}{output_file}{Style.RESET_ALL}")

# @brief: This function asks if the user wants labels in the data points of the graphic image. If so, ask which one
# @param: None
# @return: labels: The desired option (y/n) and the type of label to be added to the data points
def insert_labels():
   # Ask the user if he wants to add labels to the data points
   labels = ["", ""] # The first position stores the desired option (y/n) and the second stores the type of label to be added to the data points
   first_run = [True, True] # List to store the first run of the while loops
   
   while labels[0] != "y" and labels[0] != "n":
      if not first_run[0]:
         print(f"{backgroundColors.FAIL}Invalid option!{Style.RESET_ALL}")
      first_run[0] = False
      labels[0] = input(f"{backgroundColors.OKGREEN}Do you want to add labels to the data points? {backgroundColors.OKCYAN}(y/n){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

   if labels[0] == "y":
      labels[0] = True
      while labels[1] != "1" and labels[1] != "2":
         if not first_run[1]:
            print(f"{backgroundColors.FAIL}Invalid option!{Style.RESET_ALL}")
         first_run[1] = False
         print(f"{backgroundColors.OKGREEN}Choose the type of label to be added to the data points: {Style.RESET_ALL}")
         print(f"{backgroundColors.OKCYAN}   1. Sequence of numbers \n   2. Value of the data point (y axis value){Style.RESET_ALL}")
         labels[1] = input(f"{backgroundColors.OKGREEN}Type the number of the label you want in your images plot: {Style.RESET_ALL}")
      
   return labels

# @brief: Add the desired label type to the data points of the graphic image
# @param: plt: plt object
# @param: df: DataFrame containing the metrics data
# @param: label_type: Type of label to be added to the data points of the graphic image
# @param: commit_hashes: List containing the commit hashes
# @param: metric_values: List containing the metric values
# @return: None
def add_labels_to_plot(plt, df, label_type, commit_hashes, metric_values):
   # Add the desired label type to the data points of the graphic image
   if label_type == "1":
      # Add labels to each data point
      for j, value in enumerate(metric_values):
         plt.text(commit_hashes[j], value, f"{j+1}º", ha="center", va="bottom", fontsize=12)
   elif label_type == "2":
      # Add labels to each data point
      for j, value in enumerate(metric_values):
         plt.text(commit_hashes[j], value, f"{value}", ha="center", va="bottom", fontsize=12)

# @brief: This function gets the plt object and add each metric first and last value to the plot
# @param: plt: plt object
# @param: df: DataFrame containing the metrics data
# @return: None
def add_first_and_last_values_to_plot(plt, df):
   # Add the first and last values of each metric (cbo, cboModified, wmc, rfc) to the graphic image
   plt.text(0.20, 0.97, f"CBO {df['cbo'].iloc[0]} -> {df['cbo'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.20, 0.92, f"CBOModified {df['cboModified'].iloc[0]} -> {df['cboModified'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.70, 0.97, f"WMC {df['wmc'].iloc[0]} -> {df['wmc'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.70, 0.92, f"RFC {df['rfc'].iloc[0]} -> {df['rfc'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)

# @brief: This function creates the metrics evolution graphs fronm the RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH folder
# @param: repository_name: Name of the repository to be analyzed
# @param: id: ID of the class or method to be analyzed
# @param: clean_id: ID of the class or method to be analyzed without the / and the class or method name
# @param: id_key: ID of the class or method to be analyzed without the class or method name
# @return: None
def create_metrics_evolution_graphic(repository_name, id, clean_id, id_key):
   # Load the generated CSV files into a dataframe and save a plot of the evolution of the cbo, cboModified, wmc and rfc metrics
   df = pd.read_csv(RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH[1:] + "/" + repository_name + "-" + clean_id + ".csv")

   # Extract the metrics and commit hashes from the DataFrame
   commit_hashes = df["commit_hash"]
   metrics = ["cbo", "cboModified", "wmc", "rfc"]

   # Set the attributes of the graph: colors, line styles and marker sizes
   colors = ["blue", "pink", "green", "orange"]
   line_styles = ["-", "--", "-.", ":"]
   marker_sizes = [5, 5, 5, 5] if PROCESS_CLASSES else [6, 10, 6, 10]

   # Plotting the graph
   plt.figure(figsize=(38.4, 21.6))

   labels = insert_labels() # Ask the user if he wants to add labels to the data points and which one

   # Iterate over each metric and plot its evolution with a different color
   for i, metric in enumerate(metrics):
      metric_values = df[metric]
      plt.plot(commit_hashes, df[metric], marker="o", label=metric, linestyle=line_styles[i], markersize=marker_sizes[i], color=colors[i])

      if labels[0]:
         add_labels_to_plot(plt, df, labels[1], commit_hashes, metric_values)

   # Set the graph title and labels according to the type of analysis (class or method)
   if PROCESS_CLASSES:
      plt.title(f"Metrics Evolution of the {CK_CSV_FILE.replace('.csv', '')} named {id} {id_key} in {repository_name} repository", color="red")
   else:
      plt.title(f"Metrics Evolution of the {CK_CSV_FILE.replace('.csv', '')} named {id_key} {id} in {repository_name} repository", color="red")
   plt.xlabel("Commit Hash")
   plt.ylabel("Metric Value")

   add_first_and_last_values_to_plot(plt, df)

   # Rotate the x-axis labels for better readability
   plt.xticks(rotation=0)
   plt.xticks([commit_hashes[0], commit_hashes.iloc[-1]], visible=True, rotation="horizontal")

   # Set the color of x-values (commit hashes) and y-values (metric values)
   plt.tick_params(axis="x", colors="red")
   plt.tick_params(axis="y", colors="red")

   # Add a legend
   plt.legend()

   # Add a grid
   plt.tight_layout()

   # Save the graph
   plt.savefig(FULL_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "-" + clean_id + ".png")

   print(f"{backgroundColors.OKGREEN}Successfully created the metrics evolution graphic for {backgroundColors.OKCYAN}{id}{Style.RESET_ALL}")

# @brief: Main function
# @param: None
# @return: None
def main(): 
   # check if the path constant contains whitespaces
   if path_contains_whitespaces():
      print(f"{backgroundColors.FAIL}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
   
   # Get the name of the repository from the user
   repository_name = get_repository_name_user()

   # Check if the metrics were already calculated
   if not check_ck_metrics_folders(repository_name):
      print(f"{backgroundColors.FAIL}The metrics for {backgroundColors.OKCYAN}{repository_name}{backgroundColors.FAIL} were not calculated. Please run the main.py file first{Style.RESET_ALL}")
      return
   
   # create the metrics_evolution directory
   create_directory(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH)

   # Get the ids from the user
   ids = get_user_ids_input()

   # Validate the ids, if is related to a class or method
   if not validate_ids(ids, repository_name):
      print(f"{backgroundColors.FAIL}The {backgroundColors.OKCYAN}{repository_name.keys()}{backgroundColors.FAIL} are {OPPOSITE_CK_CSV_FILE.replace('.csv', '')} instead of {CK_CSV_FILE.replace('.csv', '')} names. Please change them!{Style.RESET_ALL}")
      return
   
   # Make a for loop to run the generate_metric_evolution_by_id and calculate_statistics function for every class or method in the user input
   for id in ids: # Loop trough the ids items in the dictionary
      clean_id = get_clean_id(id) # Get the clean id (without the / and the class or method name)
      print(f"{backgroundColors.OKGREEN}Calculating metrics evolution for {backgroundColors.OKCYAN}{id} {backgroundColors.OKGREEN}{CK_CSV_FILE.replace('.csv', '')}{Style.RESET_ALL}")

      # Calculate the CBO, CBOModified, WMC and RFC metrics evolution for the given class or method
      if not generate_metric_evolution_by_id(repository_name, id):
         print(f"{backgroundColors.FAIL}The metrics for {backgroundColors.OKCYAN}{id} {backgroundColors.FAIL}were not found{Style.RESET_ALL}")
         print(f"{backgroundColors.FAIL}Skipping {backgroundColors.OKCYAN}{id} {backgroundColors.FAIL}metrics evolution{Style.RESET_ALL}")
         continue

      # Calculate the statistics for the CSV files in the metrics_evolution directory
      output_statistics_csv_file = RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH[1:] + "/" + repository_name + "-" + clean_id + ".csv"
      calculate_statistics(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, output_statistics_csv_file)

      # Create the metrics evolution graphs
      create_metrics_evolution_graphic(repository_name, id, clean_id, ids[id])

   print(f"{backgroundColors.OKGREEN}Successfully calculated the metrics evolution for {backgroundColors.OKCYAN}{repository_name}->{list(ids.keys())}{Style.RESET_ALL}")

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function