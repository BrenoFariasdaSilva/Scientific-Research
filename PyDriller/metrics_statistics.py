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

# @brief: This function asks for the user input of the repository name
# @param: None
# @return: repository_name: Name of the repository to be analyzed
def get_repository_name_user():
   # Ask for user input of the repository name
   repository_name = input(f"{backgroundColors.OKGREEN}Enter the repository name {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

   return validate_attribute(repository_name, DEFAULT_REPOSITORY_NAME) # Validate the repository name

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

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function