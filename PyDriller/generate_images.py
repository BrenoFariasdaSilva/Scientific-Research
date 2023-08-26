import os # OS module in Python provides functions for interacting with the operating system
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
import matplotlib.pyplot as plt # Matplotlib is a comprehensive library for creating static, animated, and interactive visualizations in Python.
import atexit # For playing a sound when the program finishes
import platform # For getting the operating system name
import time # For displaying the execution time 
from colorama import Style # For coloring the terminal

# Import from the main.py file
from ck_metrics import backgroundColors
        
# Constants:
PATH = os.getcwd() # Get the current working directory
SOUND_COMMANDS = {"Darwin": "afplay", "Linux": "aplay", "Windows": "start"} # The sound commands for each operating system
SOUND_FILE = "../.assets/NotificationSound.wav" # The path to the sound file
MINIMUM_CHANGES = 1 # The minimum number of changes a method should have to be considered

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day

# Changable constants:
CLASS_CSV_FILE = "class.csv" # The name of the csv generated file from ck.
METHOD_CSV_FILE = "method.csv" # The name of the csv generated file from ck.
PROCESS_CLASSES = input(f"{backgroundColors.GREEN}Do you want to process the {backgroundColors.CYAN}class.csv{backgroundColors.GREEN} file {backgroundColors.RED}(True/False){backgroundColors.GREEN}? {Style.RESET_ALL}") == "True" # If True, then process the method.csv file. If False, then process the class.csv file
CK_CSV_FILE = CLASS_CSV_FILE if PROCESS_CLASSES else METHOD_CSV_FILE # The name of the csv generated file from ck.
CLASSES_OR_METHODS = "classes" if PROCESS_CLASSES else "methods" # The name of the csv generated file from ck.
OPPOSITE_CK_CSV_FILE = METHOD_CSV_FILE if PROCESS_CLASSES else CLASS_CSV_FILE # The name of the csv generated file from ck.
DEFAULT_REPOSITORY_NAME = ["commons-lang", "jabref", "kafka", "zookeeper"] # The default repository names
DEFAULT_CLASS_IDS = {"org.apache.commons.lang.StringUtils": "class"} # The default ids to be analyzed. It stores the class:type or class:method
DEFAULT_METHOD_IDS = {"org.apache.commons.lang3.AnnotationUtilsTest": "testBothArgsNull/0", "org.apache.commons.lang.LangTestSuite": "suite/0"} # The default ids to be analyzed. It stores the class:type or class:method
DEFAULT_IDS = DEFAULT_CLASS_IDS if PROCESS_CLASSES else DEFAULT_METHOD_IDS # The default ids to be analyzed. It stores the class:type or method:class
IMAGE_LABELS = [False, False]
 
# Relative paths:
RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH = "/metrics_evolution" # The relative path of the metrics_evolution directory
RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH = "/metrics_statistics" # The relative path of the metrics_statistics directory
RELATIVE_GRAPHICS_DIRECTORY_PATH = "/graphics" # The relative path of the graphics directory

# Default values:
FULL_METRICS_EVOLUTION_DIRECTORY_PATH = PATH + RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH # The full path of the metrics_evolution directory
FULL_GRAPHICS_DIRECTORY_PATH = PATH + RELATIVE_GRAPHICS_DIRECTORY_PATH # The full path of the graphics directory

# @brief: This function is used to verify if the PATH constant contain whitespaces
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
      print(f"{backgroundColors.YELLOW}The attribute is empty! Using the default value: {backgroundColors.CYAN}{default_attribute_value}{backgroundColors.YELLOW}.{Style.RESET_ALL}")
      attribute = default_attribute_value # Set the attribute to the default value
   return attribute # Return the attribute

# @brief: This function asks for the user input of the repository name
# @param: None
# @return: repository_name: Name of the repository to be analyzed
def get_repository_name_user():
   # Ask for user input of the repository name
   repository_name = input(f"{backgroundColors.GREEN}Enter the repository name {backgroundColors.RED}(String){backgroundColors.GREEN}: {Style.RESET_ALL}")

   return validate_attribute(repository_name, DEFAULT_REPOSITORY_NAME[0]) # Validate the repository name

# @brief: Create a directory if it does not exist
# @param: full_directory_path: Name of the directory to be created
# @param: relative_directory_path: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_path, relative_directory_path):
   if os.path.isdir(full_directory_path): # Verify if the directory already exists
      print(f"{backgroundColors.GREEN}The {backgroundColors.CYAN}{relative_directory_path}{backgroundColors.GREEN} directory already exists.{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_path)
      print(f"{backgroundColors.GREEN}Successfully created the {backgroundColors.CYAN}{relative_directory_path}{backgroundColors.GREEN} directory.{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print(f"{backgroundColors.GREEN}The creation of the {backgroundColors.CYAN}{relative_directory_path}{backgroundColors.GREEN} directory failed.{Style.RESET_ALL}")

# @brief: Get user input of the name of the class or method to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: id: Name of the class or method to be analyzed
def get_user_ids_input(repository_name):
   ids = {} # Dictionary that stores the ids to be analyzed
   name = ""
   first_run = True
   csv_file = CK_CSV_FILE.replace('.csv', '') # The name of the csv generated file from ck.
   while name == "" and first_run:
      first_run = False
      # Ask for user input of the class or method name
      name = input(f"{backgroundColors.GREEN}Enter the name of the {csv_file} {backgroundColors.RED}(String/*){backgroundColors.GREEN}: {Style.RESET_ALL}")
      # if the CK_CSV_FILE is a class csv file, ask for the type of the class ('class' 'interface' 'innerclass' 'enum' 'anonymous')
      if CK_CSV_FILE == CLASS_CSV_FILE:
         value = input(f"{backgroundColors.GREEN}Enter the type of the {csv_file} {backgroundColors.CYAN}{ids}{backgroundColors.GREEN} to be analyzed {backgroundColors.RED}(String){backgroundColors.GREEN}: {Style.RESET_ALL}")
      # if the CK_CSV_FILE is a method csv file, ask for the name of the class of the method
      elif CK_CSV_FILE == METHOD_CSV_FILE:
         value = input(f"{backgroundColors.GREEN}Enter the {csv_file} name of the {backgroundColors.CYAN}{ids}{backgroundColors.GREEN} to be analyzed {backgroundColors.RED}(String){backgroundColors.GREEN}: {Style.RESET_ALL}")

      # add the name and value to the id dictionary
      ids[name] = value

   # If the name is "*", them do for every Class/Method in the Repository.
   if name == "*" and not first_run:
      variable_attribute = "Type" if PROCESS_CLASSES else "Method"
      top_changes_csv_path = RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH[1:] + "/" + repository_name + "/" + CK_CSV_FILE.replace('.csv', '') + "-" + "sorted_changes.csv"
      result_dict = {} # Create a dictionary with the class name as the key and the type or method as the value, but the "Changed" column must be at least 2.
      with open(top_changes_csv_path, "r") as file:
         csv_reader = csv.DictReader(file)
         for row in csv_reader:
            if int(row["Changed"]) > MINIMUM_CHANGES:
               class_key = row["Class"]
               variable_attribute_value = row[variable_attribute]
               result_dict[class_key] = variable_attribute_value
      return result_dict # Return the class or method name

   # If the id dictionary is empty, get from the DEFAULT_IDS constant
   if name == "" and not first_run:
      ids = DEFAULT_IDS
      print(f"{backgroundColors.GREEN}Using the default stored {CK_CSV_FILE.replace('.csv', '')} names: {backgroundColors.CYAN}{', '.join(ids.keys())}{backgroundColors.GREEN}.{Style.RESET_ALL}")

   return ids # Return the class or method name

# @brief: This function validates if the ids are as the same type as the files to be analyzed defined in CK_CSV_FILE according to PROCESS_CLASSES
# @param: ids: Dictionary containing the ids to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: True if the ids are valid, False otherwise
def validate_ids(ids, repository_name):
   # Get the path of the file containing the top changes of the classes
   repo_top_changes_file_path = RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH[1:] + "/" + repository_name + "/" + CK_CSV_FILE.replace('.csv', '') + "-" + "sorted_changes.csv"

   classnames = pd.read_csv(repo_top_changes_file_path)["Class"].unique()
   attribute = "Type" if PROCESS_CLASSES else "Method"
   variable_attributes = pd.read_csv(repo_top_changes_file_path)[attribute].unique()
   # Verify if the ids are as the same type as the files to be analyzed defined in CK_CSV_FILE according to PROCESS_CLASSES
   for key, value in ids.items():
      if key not in classnames or value not in variable_attributes: # If the id is not a class or the value is not in the attribute field
         return False # Return False because the id is not a class
   return True # Return True because the ids are valid

# @brief: This function receives an id and verify if it contains slashes, if so, it returns the id without the slashes
# @param: id: ID of the class or method to be analyzed
# @return: ID of the class or method to be analyzed without the slashes
def get_clean_id(id):
   if "/" in id: # If the id contains slashes, remove them
      return str(id.split("/")[0:-1])[2:-2]
   else:
      return id

# @brief: This verifies if all the metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: folder_path: The path of the folder to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @param: ids: The ids to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def check_metrics_files(folder_path, repository_name, ids):
   print(f"{backgroundColors.GREEN}Checking if all the {backgroundColors.CYAN}{folder_path.rsplit('/', 1)[-1]}{backgroundColors.GREEN} are already created.{Style.RESET_ALL}")
   # Change the current working directory to the repository folder
   os.chdir(folder_path)
   
   # Now, for every ids.keys() in the ids dictionary, verify if there is a csv file with the name of the id
   for id in ids.keys():
      file_name = f"{id} {ids[id]}" if PROCESS_CLASSES else f"{id} {get_clean_id(ids[id])}"
      evolution_file = f"{repository_name}/{CLASSES_OR_METHODS}/{file_name}.csv"
      if not os.path.isfile(evolution_file): # If the file does not exist
         print(f"{backgroundColors.YELLOW}The {backgroundColors.CYAN}{id}.csv{backgroundColors.YELLOW} file does not exist.{Style.RESET_ALL}")
         os.chdir(PATH) # Change the current working directory to the original path
         return False
   os.chdir(PATH) # Change the current working directory to the original path
   return True

# @brief: This function asks if the user wants labels in the data points of the graphic image. If so, ask which one
# @param: None
# @return: labels: The desired option (y/n) and the type of label to be added to the data points
def insert_labels():
   # Ask the user if he wants to add labels to the data points
   labels = ["", ""] # The first position stores the desired option (y/n) and the second stores the type of label to be added to the data points
   first_run = [True, True] # List to store the first run of the while loops
   
   while labels[0] != "y" and labels[0] != "n" and labels[0] != "y*" and labels[0] != "n*":
      if not first_run[0]:
         print(f"{backgroundColors.RED}Invalid option!{Style.RESET_ALL}")
      first_run[0] = False
      labels[0] = input(f"{backgroundColors.GREEN}Do you want to add labels to the data points {backgroundColors.RED}(y*/n*/y/n){backgroundColors.GREEN}? {Style.RESET_ALL}")

   if labels[0] == "y*":
      IMAGE_LABELS[0] = True
      labels[0] = "y"
   elif labels[0] == "n*":
      IMAGE_LABELS[0] = False
      labels[0] = "n"

   if labels[0] == "y":
      labels[0] = True 
      while labels[1] != "1" and labels[1] != "2":
         if not first_run[1]:
            print(f"{backgroundColors.RED}Invalid option!{Style.RESET_ALL}")
         first_run[1] = False
         print(f"{backgroundColors.GREEN}Choose the type of label to be added to the data points: {Style.RESET_ALL}")
         print(f"{backgroundColors.CYAN}   1. Sequence of numbers \n   2. Value of the data point (y axis value){Style.RESET_ALL}")
         labels[1] = input(f"{backgroundColors.GREEN}Type the number of the label you want in your images plot {backgroundColors.RED}(1/2){backgroundColors.GREEN}: {Style.RESET_ALL}")
         if IMAGE_LABELS[0]:
            IMAGE_LABELS[1] = labels[1]
      
   return labels

# @brief: Add the desired label type to the data points of the graphic image
# @param: df: DataFrame containing the metrics data
# @param: label_type: Type of label to be added to the data points of the graphic image
# @param: commit_hashes: List containing the commit hashes
# @param: metric_values: List containing the metric values
# @return: None
def add_labels_to_plot(plt, label_type, commit_hashes, metric_values):
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
   # Add the first and last values of each metric (CBO, CBO Modified, WMC, RFC) to the graphic image
   plt.text(0.20, 0.97, f"CBO {df['CBO'].iloc[0]} -> {df['CBO'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.20, 0.92, f"CBOModified {df['CBO Modified'].iloc[0]} -> {df['CBO Modified'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.70, 0.97, f"WMC {df['WMC'].iloc[0]} -> {df['WMC'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)
   plt.text(0.70, 0.92, f"RFC {df['RFC'].iloc[0]} -> {df['RFC'].iloc[-1]}", fontsize=12, color="red", transform=plt.gcf().transFigure)

# @brief: This function creates the metrics evolution graphs fronm the RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH folder
# @param: repository_name: Name of the repository to be analyzed
# @param: id: ID of the class or method to be analyzed
# @param: clean_id_key: Clean ID of the class or method to be analyzed
# @return: None
def create_metrics_evolution_graphic(repository_name, id, clean_id_key):
   # Load the generated CSV files into a dataframe and save a plot of the evolution of the CBO, CBO Modified, WMC and RFC metrics
   df = pd.read_csv(PATH + RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + id + " " + clean_id_key + ".csv")

   # Extract the metrics and commit hashes from the DataFrame
   commit_hashes = df["Commit Hash"]
   metrics = ["CBO", "CBO Modified", "WMC", "RFC"]

   # Set the attributes of the graph: colors, line styles and marker sizes
   colors = ["blue", "pink", "green", "orange"]
   line_styles = ["-", "--", "-.", ":"]
   marker_sizes = [5, 5, 5, 5] if PROCESS_CLASSES else [6, 10, 6, 10]

   # Plotting the graph
   plt.figure(figsize=(38.4, 21.6))

   if not IMAGE_LABELS[0]:
      labels = insert_labels() # Ask the user if he wants to add labels to the data points and which one
   else:
      labels = IMAGE_LABELS

   # Iterate over each metric and plot its evolution with a different color
   for i, metric in enumerate(metrics):
      metric_values = df[metric]
      plt.plot(commit_hashes, df[metric], marker="o", label=metric, linestyle=line_styles[i], markersize=marker_sizes[i], color=colors[i])

      if labels[0]:
         add_labels_to_plot(plt, labels[1], commit_hashes, metric_values)

   # Set the graph title and labels according to the type of analysis (class or method)
   if PROCESS_CLASSES:
      plt.title(f"Metrics Evolution of the {CK_CSV_FILE.replace('.csv', '')} named {id} {clean_id_key} in {repository_name} repository", color="red")
   else:
      plt.title(f"Metrics Evolution of the {CK_CSV_FILE.replace('.csv', '')} named {clean_id_key} {id} in {repository_name} repository", color="red")
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

   # create the graphics directory if it doesn't exist
   create_directory(FULL_GRAPHICS_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + id, RELATIVE_GRAPHICS_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + id)

   # Save the graph
   plt.savefig(FULL_GRAPHICS_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + id + "/" + clean_id_key + ".png")

   # Close the plot
   plt.close()

   object_reference = f"{clean_id_key}" if PROCESS_CLASSES else f"{clean_id_key} {CK_CSV_FILE.replace('.csv', '')}"
   print(f"{backgroundColors.CYAN}Successfully{backgroundColors.GREEN} created the {backgroundColors.CYAN}metrics evolution graphic {backgroundColors.GREEN}for {backgroundColors.CYAN}{id} {object_reference}{backgroundColors.GREEN} from the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository.{Style.RESET_ALL}")
   print()

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

# @brief: Main function
# @param: None
# @return: None
def main():
   start_time = time.time() # Start the timer
   
   # Verify if the path constant contains whitespaces
   if path_contains_whitespaces():
      print(f"{backgroundColors.RED}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
   
   print(f"{backgroundColors.GREEN}This script {backgroundColors.CYAN}generates the images{backgroundColors.GREEN} from the {backgroundColors.CYAN}metrics evolution{backgroundColors.GREEN} of the {CK_CSV_FILE.replace('.csv', '')} of a {backgroundColors.CYAN}specific repository{backgroundColors.GREEN}.{Style.RESET_ALL}")
   print(f"{backgroundColors.GREEN}The {backgroundColors.CYAN}source of the data{backgroundColors.GREEN} used to {backgroundColors.CYAN}generate the images{backgroundColors.GREEN} is the {backgroundColors.CYAN}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}{backgroundColors.GREEN} directory.{Style.RESET_ALL}")

   # Get the name of the repository from the user
   repository_name = get_repository_name_user()

   # Get the ids from the user
   ids = get_user_ids_input(repository_name)

   # Validate the ids, if is related to a class or method
   if not validate_ids(ids, repository_name):
      print(f"{backgroundColors.RED}The {backgroundColors.CYAN}{', '.join(ids.keys())}{backgroundColors.RED} are {OPPOSITE_CK_CSV_FILE.replace('.csv', '')} instead of {CK_CSV_FILE.replace('.csv', '')} names. Please change them!{Style.RESET_ALL}")
      return
   
   # Verify if the metrics evolution were already calculated
   if not check_metrics_files(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, repository_name, ids):
      print(f"{backgroundColors.RED}The metrics evolution for {backgroundColors.CYAN}{', '.join(ids.keys())}{backgroundColors.RED} in {backgroundColors.CYAN}{repository_name}{backgroundColors.RED} were not created. Please run the {backgroundColors.CYAN}metrics_changes.py{backgroundColors.RED} file first.{Style.RESET_ALL}")
      return
   
   number_of_ids = len(ids.keys())
   # Make a for loop to run the create_metrics_evolution_graphic function for each id
   for index, id in enumerate(ids): # Loop trough the ids items in the dictionary
      print(f"{backgroundColors.GREEN}Generating Image {backgroundColors.CYAN}{index+1} of {number_of_ids}{backgroundColors.GREEN} for the {backgroundColors.CYAN}{id} {CK_CSV_FILE.replace('.csv', '')}{backgroundColors.GREEN} inside the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository.{Style.RESET_ALL}")

      # Create the metrics evolution graphs
      create_metrics_evolution_graphic(repository_name, id, get_clean_id(ids[id]))

   print(f"{backgroundColors.CYAN}Successfully created the metrics evolution graphics{backgroundColors.GREEN} for the {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN} repository inside the {backgroundColors.CYAN}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH[1:]}{backgroundColors.GREEN} directory.{Style.RESET_ALL}")

   elapsed_time = time.time() - start_time
   elapsed_time_string = f"Time taken to generate the {backgroundColors.CYAN}images{backgroundColors.GREEN} for the {backgroundColors.CYAN}{CLASSES_OR_METHODS}{backgroundColors.GREEN} in {backgroundColors.CYAN}{repository_name}{backgroundColors.GREEN}: "
   output_time(elapsed_time_string, round(elapsed_time, 2))

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function