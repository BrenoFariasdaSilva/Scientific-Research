import os # OS module in Python provides functions for interacting with the operating system
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
import statistics # The statistics module provides functions for calculating mathematical statistics of numeric (Real-valued) data
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
OPPOSITE_CK_CSV_FILE = METHOD_CSV_FILE if PROCESS_CLASSES else CLASS_CSV_FILE # The name of the csv generated file from ck.
DEFAULT_REPOSITORY_NAME = "commons-lang"
DEFAULT_CLASS_IDS = {"org.apache.commons.lang.StringUtils": "class"} # The default ids to be analyzed. It stores the class:type or method:class
DEFAULT_METHOD_IDS = {"testBothArgsNull/0": "org.apache.commons.lang3.AnnotationUtilsTest", "suite/0": "org.apache.commons.lang.LangTestSuite"} # The default ids to be analyzed. It stores the class:type or method:class
DEFAULT_IDS = DEFAULT_CLASS_IDS if PROCESS_CLASSES else DEFAULT_METHOD_IDS # The default ids to be analyzed. It stores the class:type or method:class
 
# Relative paths:
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
      print (f"{backgroundColors.OKGREEN}Successfully created the {backgroundColors.OKCYAN}{relative_directory_path}{backgroundColors.OKGREEN} directory{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print(f"{backgroundColors.OKGREEN}The creation of the {backgroundColors.OKCYAN}{relative_directory_path}{backgroundColors.OKGREEN} directory failed{Style.RESET_ALL}")

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

# @brief: This verifies if all the metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: folder_path: The path of the folder to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @param: ids: The ids to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def check_metrics_files(folder_path, repository_name, ids):
   print(f"{backgroundColors.OKGREEN}Checking if all the {backgroundColors.OKCYAN}{folder_path.rsplit('/', 1)[-1]}{backgroundColors.OKGREEN} are already created.{Style.RESET_ALL}")
   # Change the current working directory to the repository folder
   os.chdir(folder_path)
   
   # Now, for every ids.keys() in the ids dictionary, check if there is a csv file with the name of the id
   for id in ids.keys():
      clean_id = get_clean_id(id) # Remove the slashes from the id, if it contains any
      evolution_file = f"{repository_name}-{clean_id}.csv"
      if not os.path.isfile(evolution_file):
         print(f"{backgroundColors.WARNING}The {backgroundColors.OKCYAN}{id}.csv{backgroundColors.WARNING} file does not exist{Style.RESET_ALL}")
         os.chdir(PATH)
         return False
   os.chdir(PATH)
   return True

# @brief: Main function
# @param: None
# @return: None
def main(): 
   # check if the path constant contains whitespaces
   if path_contains_whitespaces():
      print(f"{backgroundColors.FAIL}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
   
   print(f"{backgroundColors.OKGREEN}This script {backgroundColors.OKCYAN}generates the metrics statistics{backgroundColors.OKGREEN} for the {backgroundColors.OKCYAN}{CK_CSV_FILE.replace('.csv', '')} files{backgroundColors.OKGREEN} in the {backgroundColors.OKCYAN}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}{backgroundColors.OKGREEN} directory.{Style.RESET_ALL}")
   print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}source of the data{backgroundColors.OKGREEN} used to {backgroundColors.OKCYAN}calculate the metrics statistics{backgroundColors.OKGREEN} is the {backgroundColors.OKCYAN}{RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH}{backgroundColors.OKGREEN} directory.{Style.RESET_ALL}")

   # Get the name of the repository from the user
   repository_name = get_repository_name_user()

   # create the metrics_statistics directory if it does not exist
   create_directory(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, RELATIVE_METRICS_EVOLUTION_DIRECTORY_PATH)

   # Get the ids from the user
   ids = get_user_ids_input()

   # Validate the ids, if is related to a class or method
   if not validate_ids(ids, repository_name):
      print(f"{backgroundColors.FAIL}The {backgroundColors.OKCYAN}{', '.join(repository_name.keys())}{backgroundColors.FAIL} are {OPPOSITE_CK_CSV_FILE.replace('.csv', '')} instead of {CK_CSV_FILE.replace('.csv', '')} names. Please change them!{Style.RESET_ALL}")
      return
   
   # Check if the metrics evolution were already calculated
   if not check_metrics_files(FULL_METRICS_EVOLUTION_DIRECTORY_PATH, repository_name, ids):
      print(f"{backgroundColors.FAIL}The metrics evolution for {backgroundColors.OKCYAN}{', '.join(ids.keys())}{backgroundColors.FAIL} in {backgroundColors.OKCYAN}{repository_name}{backgroundColors.FAIL} were not created. Please run the {backgroundColors.OKCYAN}specific_files_statistics.py{backgroundColors.FAIL} file first{Style.RESET_ALL}")
      return
   

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function