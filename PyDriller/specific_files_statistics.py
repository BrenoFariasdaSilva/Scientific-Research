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

# @brief: Main function
# @param: None
# @return: None
def main(): 
   # check if the path constants contains whitespaces
   if path_contains_whitespaces():
      return
   
   # Get the name of the repository from the user
   repository_name = get_repository_name_user()

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function