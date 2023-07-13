import os # OS module in Python provides functions for interacting with the operating system
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
import pandas as pd # Pandas is a fast, powerful, flexible and easy to use open source data analysis and manipulation tool,
import time # This module provides various time-related functions
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from colorama import Style # For coloring the terminal

# Macros:
class backgroundColors: # Colors for the terminal
	OKCYAN = "\033[96m" # Cyan
	OKGREEN = "\033[92m" # Green
	WARNING = "\033[93m" # Yellow
	FAIL = "\033[91m" # Red
        
# Default paths:
PATH = os.getcwd() # Get the current working directory
DEFAULT_FOLDER = PATH # Get the current working directory

# Extensions:
COMMIT_HASHES_FILE_EXTENSION = ".csv" # The extension of the file that contains the commit hashes

# CK Generated Files:
CK_METRICS_FILES = ["class.csv", "method.csv"] # The files that are generated by CK

# Time units:
TIME_UNITS = [60, 3600, 86400] # Seconds in a minute, seconds in an hour, seconds in a day
 
# Relative paths:
RELATIVE_CK_METRICS_DIRECTORY_PATH = "/ck_metrics" # The relative path of the directory that contains the CK generated files
RELATIVE_REPOSITORY_DIRECTORY_PATH = "/repositories" # The relative path of the directory that contains the repositories
RELATIVE_CK_JAR_PATH = "/ck/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar" # The relative path of the CK JAR file

# Default values:
DEFAULT_REPOSITORY_URL = ["https://github.com/apache/commons-lang", "https://github.com/JabRef/jabref"] # The default repository URL
FULL_CK_METRICS_DIRECTORY_PATH = PATH + RELATIVE_CK_METRICS_DIRECTORY_PATH # The full path of the directory that contains the CK generated files
FULL_REPOSITORY_DIRECTORY_PATH = PATH + RELATIVE_REPOSITORY_DIRECTORY_PATH # The full path of the directory that contains the repositories
FULL_CK_JAR_PATH = PATH + RELATIVE_CK_JAR_PATH # The full path of the CK JAR file

# @brief: This function is used to verify if the PATH constant contain whitespaces
# @param: None
# @return: True if the PATH constant contain whitespaces, False otherwise
def path_contains_whitespaces():
   # Verify if the PATH constant contains whitespaces
   if " " in PATH: # If the PATH constant contains whitespaces
      return True # Return True if the PATH constant contains whitespaces
   return False # Return False if the PATH constant does not contain whitespaces

# @brief: Verifiy if the attribute is empty. If so, set it to the default value
# @param: attribute: The attribute to be checked
# @param: default_attribute_value: The default value of the attribute
# @return: The repository URL and the output directory
def validate_attribute(attribute, default_attribute_value):
   if not attribute: # Verify if the attribute is empty
      print(f"{backgroundColors.WARNING}The attribute is empty! Using the default value: {backgroundColors.OKCYAN}{default_attribute_value}{Style.RESET_ALL}")
      attribute = default_attribute_value # Set the attribute to the default value
   return attribute

# @brief: Get the user input of the repository URL
# @param: None
# @return: repository_url: URL of the repository to be analyzed
def get_user_repository_url():
   # Ask for user input of the repository URL
   repository_url = input(f"{backgroundColors.OKGREEN}Enter the repository URL {backgroundColors.OKCYAN}(String){backgroundColors.OKGREEN}: {Style.RESET_ALL}")

   # Return the repository URL
   return validate_attribute(repository_url, DEFAULT_REPOSITORY_URL[0])

# @brief: Get the string after the last slash
# @param: url: URL of the repository to be analyzed
# @return: The name of the repository
def get_repository_name(url):
   # Return the string after the last slash
   return url.split("/")[-1]

# @brief: Update the repository using "git pull"
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def update_repository(repository_name):
   print(f"{backgroundColors.OKGREEN}Updating the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository using {backgroundColors.OKCYAN}git pull{backgroundColors.OKGREEN}.{Style.RESET_ALL}")
   os.chdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name)
   # Create a thread to update the repository located in RELATIVE_REPOSITORY_DIRECTORY + '/' + repository_name
   update_thread = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   update_thread.wait() # Wait for the thread to finish
   os.chdir(DEFAULT_FOLDER) # Change the current working directory to the default one

# @brief: Clone the repository to the repository directory
# @param: repository_name: Name of the repository to be analyzed
# @param: repository_url: URL of the repository to be analyzed
# @return: None
def clone_repository(repository_name, repository_url):
   # Verify if the repository directory already exists and if it is not empty
   if os.path.isdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name) and os.listdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name):
      print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository is already cloned!{Style.RESET_ALL}")
      update_repository(repository_name) # Update the repository
      return
   else:
      print(f"{backgroundColors.OKGREEN}Cloning the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository...{Style.RESET_ALL}")
      # Create a thread to clone the repository
      thread = subprocess.Popen(["git", "clone", repository_url, FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
      # Wait for the thread to finish
      thread.wait()
      print(f"{backgroundColors.OKGREEN}Successfully cloned the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository{Style.RESET_ALL}")

# @brief: Create a directory
# @param: full_directory_name: Name of the directory to be created
# @param: relative_directory_name: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_name, relative_directory_name):
   if os.path.isdir(full_directory_name): # Verify if the directory already exists
      print(f"{backgroundColors.OKGREEN}The {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory already exists{Style.RESET_ALL}")
      return
   try: # Try to create the directory
      os.makedirs(full_directory_name)
      print (f"{backgroundColors.OKGREEN}Successfully created the {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory{Style.RESET_ALL}")
   except OSError: # If the directory cannot be created
      print (f"{backgroundColors.OKGREEN}The creation of the {backgroundColors.OKCYAN}{relative_directory_name}{backgroundColors.OKGREEN} directory failed{Style.RESET_ALL}")

# @brief: This verifies if all the metrics are already calculated by opening the commit hashes file and checking if every commit hash in the file is a folder in the repository folder
# @param: repository_name: Name of the repository to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def verify_ck_metrics_folder(repository_name):
   print(f"{backgroundColors.OKGREEN}Checking if all the {backgroundColors.OKCYAN}CK metrics{backgroundColors.OKGREEN} are already calculated for the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository...{Style.RESET_ALL}")
   data_path = os.path.join(PATH, RELATIVE_CK_METRICS_DIRECTORY_PATH[1:]) # Join the PATH with the relative path of the ck metrics directory
   repo_path = os.path.join(data_path, repository_name) # Join the data path with the repository name
   commit_file = f"{repository_name}-commit_hashes{COMMIT_HASHES_FILE_EXTENSION}" # The name of the commit hashes file
   commit_file_path = os.path.join(data_path, commit_file) # Join the data path with the commit hashes file

   # Verify if the repository exists
   if not os.path.exists(commit_file_path):
      print(f"{backgroundColors.FAIL}File {backgroundColors.OKCYAN}{commit_file}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{data_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
      return False # Return False because the repository does not exist

   # Read the commit hashes csv file and get the commit_hashes column, but ignore the first line
   commit_hashes = pd.read_csv(commit_file_path, sep=",", usecols=["commit hash"], header=0).values.tolist()

   # Verify if the repository exists
   for commit_hash in commit_hashes:
      commit_hash = commit_hash[0] # This removes the [] and the '' from the commit hash
      folder_path = os.path.join(repo_path, commit_hash) # Join the repo path with the folder name

      if os.path.exists(folder_path): # Verify if the folder exists
         for ck_metric_file in CK_METRICS_FILES: # Verify if all the ck metrics files exist inside the folder
            ck_metric_file_path = os.path.join(folder_path, ck_metric_file)
            if not os.path.exists(ck_metric_file_path): # If the file does not exist
               print(f"{backgroundColors.FAIL}The file {backgroundColors.OKCYAN}{ck_metric_file}{backgroundColors.FAIL} does not exist inside {backgroundColors.OKCYAN}{folder_path}{backgroundColors.FAIL}.{Style.RESET_ALL}")
               return False # If the file does not exist, then the metrics are not calculated
   return True # If all the metrics are already calculated

# @brief: This function is used to checkout a specific branch
# @param: branch_name: Name of the branch to be checked out
# @return: None
def checkout_branch(branch_name):
   # Create a thread to checkout the branch
   checkout_thread = subprocess.Popen(["git", "checkout", branch_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   # Wait for the thread to finish
   checkout_thread.wait()

# @brief: This function is used to run the command that runs the CK metrics generator in a subprocess
# @param: cmd: Command to be executed
# @return: None
def run_ck_metrics_generator(cmd):
   # Create a thread to run the cmd command
   thread = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   stdout, stderr = thread.communicate()
   print(f"{backgroundColors.OKGREEN}{stdout.decode('utf-8')}{Style.RESET_ALL}")

# @brief: This function generates the output directory path for the CK metrics generator
# @param: repository_name: Name of the repository to be analyzed
# @param: commit_hash: Commit hash of the commit to be analyzed
# @return: The output_directory and relative_output_directory paths
def generate_output_directory_paths(repository_name, commit_hash):
   output_directory = FULL_CK_METRICS_DIRECTORY_PATH + "/" + repository_name + "/" + commit_hash + "/"
   relative_output_directory = RELATIVE_CK_METRICS_DIRECTORY_PATH + "/" + repository_name + "/" + commit_hash + "/"
   return output_directory, relative_output_directory

# @brief: This function outputs the progress of the analyzed commit
# @param: repository_name: Name of the repository to be analyzed
# @param: commit_hash: Commit hash of the commit to be analyzed
# @param: commit_number: Number of the commit to be analyzed
# @param: number_of_commits: Number of commits to be analyzed
# @return: None
def output_commit_progress(repository_name, commit_hash, commit_number, number_of_commits):
   relative_cmd = f"{backgroundColors.OKGREEN}java -jar {backgroundColors.OKCYAN}{RELATIVE_CK_JAR_PATH} {RELATIVE_REPOSITORY_DIRECTORY_PATH}/{repository_name}{backgroundColors.OKGREEN} false 0 false {backgroundColors.OKCYAN}{RELATIVE_CK_METRICS_DIRECTORY_PATH}/{repository_name}/{commit_hash}/"
   print(f"{backgroundColors.OKCYAN}{commit_number} of {number_of_commits}{backgroundColors.OKGREEN} - Running CK: {relative_cmd}{Style.RESET_ALL}")

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
   print(f"{backgroundColors.OKGREEN}{output_string}{backgroundColors.OKCYAN}{rounded_time} {time_unit}{Style.RESET_ALL}")

# @brief: This function outputs the execution time of the CK metrics generator
# @param: first_iteration_duration: Duration of the first iteration
# @param: elapsed_time: Elapsed time of the execution
# @param: number_of_commits: Number of commits to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def show_execution_time(first_iteration_duration, elapsed_time, number_of_commits, repository_name):
   first_iteration_time_string = f"Time taken to generate {backgroundColors.OKCYAN}CK metrics{backgroundColors.OKGREEN} for the first commit in {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN}: "
   output_time(first_iteration_time_string, round(first_iteration_duration, 2))
   estimated_time_string = f"Estimated time for the rest of the iterations in {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN}: "
   output_time(estimated_time_string, round(first_iteration_duration * number_of_commits, 2))
   time_taken_string = f"Time taken to generate CK metrics for {backgroundColors.OKCYAN}{number_of_commits}{backgroundColors.OKGREEN} commits in {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository: "
   output_time(time_taken_string, round(elapsed_time, 2))

# @brief: This function traverses the repository
# @param: repository_name: Name of the repository to be analyzed
# @param: repository_url: URL of the repository to be analyzed
# @param: number_of_commits: Number of commits to be analyzed
# @return: The commit hashes of the repository
def traverse_repository(repository_name, repository_url, number_of_commits):
   start_time = time.time()  # Start measuring time
   i = 1
   traversed_first_commit = False
   commit_hashes = []

   for commit in Repository(repository_url).traverse_commits():
      # Store the commit hash, commit message and commit date in one line of the list, separated by commas
      current_tuple = (commit.hash, commit.msg.split('\n')[0], commit.committer_date)
      commit_hashes.append(current_tuple)

      # Change working directory to the repository directory
      workdir_directory = FULL_REPOSITORY_DIRECTORY_PATH + "/" + repository_name
      os.chdir(workdir_directory)        

      # Checkout the commit hash branch to run ck
      checkout_branch(commit.hash)

      # Create the output directory paths
      output_directory, relative_output_directory = generate_output_directory_paths(repository_name, commit.hash)
      # Create the output directory
      create_directory(output_directory, relative_output_directory)

      # Change working directory to the repository directory
      os.chdir(output_directory)

      # Output the progress of the analyzed commit
      output_commit_progress(repository_name, commit.hash, i, number_of_commits)

      # Run ck metrics for the current commit hash
      cmd = f"java -jar {FULL_CK_JAR_PATH} {workdir_directory} false 0 false {output_directory}"
      run_ck_metrics_generator(cmd)

      if i == 1:
         traversed_first_commit = True
         first_iteration_time_string = f"Time taken to generate {backgroundColors.OKCYAN}CK metrics{backgroundColors.OKGREEN} for the first commit in {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN}: "
         first_iteration_duration = time.time() - start_time
         output_time(first_iteration_time_string, round(first_iteration_duration, 2))

      i += 1

   if traversed_first_commit:
      elapsed_time = time.time() - start_time  # Calculate elapsed time
      show_execution_time(first_iteration_duration, elapsed_time, number_of_commits, repository_name)
      
   return commit_hashes

# @brief: This function writes the commit hashes to a csv file
# @param: repository_name: Name of the repository to be analyzed
# @param: commit_hashes: List of tuples containing the commit hashes, commit messages and commit dates
# @return: None
def write_commit_hashes_to_csv(repository_name, commit_hashes):
   file_path = f"{FULL_CK_METRICS_DIRECTORY_PATH}/{repository_name}-commit_hashes{COMMIT_HASHES_FILE_EXTENSION}"
   with open(file_path, "w", newline='') as csv_file:
      writer = csv.writer(csv_file)
      # Write the header
      writer.writerow(["commit hash", "commit message", "commit date"])
      # Write the commit hashes
      writer.writerows(commit_hashes)

# @brief: Main function
# @param: None
# @return: None
def main():
   # Verify if the path constants contains whitespaces
   if path_contains_whitespaces():
      print(f"{backgroundColors.FAIL}The PATH constant contains whitespaces. Please remove them!{Style.RESET_ALL}")
      return
   
   # Get the user input
   repository_url = get_user_repository_url()
   # Get the name of the repository
   repository_name = get_repository_name(repository_url)

   # Verify if the metrics were already calculated
   if verify_ck_metrics_folder(repository_name):
      print(f"{backgroundColors.OKGREEN}The metrics for {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} were already calculated{Style.RESET_ALL}")
      return
   
   # Create the ck metrics directory
   create_directory(FULL_CK_METRICS_DIRECTORY_PATH, RELATIVE_CK_METRICS_DIRECTORY_PATH)
   # Create the repositories directory
   create_directory(FULL_REPOSITORY_DIRECTORY_PATH, RELATIVE_REPOSITORY_DIRECTORY_PATH)

   # Clone the repository
   clone_repository(repository_name, repository_url)
   
   # Get the number of commits, which is needed to traverse the repository
   number_of_commits = len(list(Repository(repository_url).traverse_commits()))
   # Traverse the repository to run ck for every commit hash in the repository 
   commit_hashes = traverse_repository(repository_name, repository_url, number_of_commits)

   # Write the commit hashes to a csv file
   write_commit_hashes_to_csv(repository_name, commit_hashes)

   # Checkout the main branch
   checkout_branch("main")

# Directly run the main function if the script is executed
if __name__ == '__main__':
   main() # Run the main function