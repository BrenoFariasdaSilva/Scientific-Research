import os # OS module in Python provides functions for interacting with the operating system
import csv # CSV (Comma Separated Values) is a simple file format used to store tabular data, such as a spreadsheet or database
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
import statistics # The statistics module provides functions for calculating mathematical statistics of numeric (Real-valued) data
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from tqdm import tqdm # TQDM is a progress bar library with good support for nested loops and Jupyter/IPython notebooks.
from colorama import Style # For coloring the terminal

# Macros:
class backgroundColors: # Colors for the terminal
	OKCYAN = "\033[96m" # Cyan
	OKGREEN = "\033[92m" # Green
	WARNING = "\033[93m" # Yellow
	FAIL = "\033[91m" # Red
 
# Relative paths:
RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH = "/ck_metrics"
RELATIVE_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH = "/metrics_evolution"
RELATIVE_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH = "/metrics_statistics"
RELATIVE_REPOSITORY_DIRECTORY_PATH = "/repositories"
RELATIVE_CK_JAR_PATH = "/ck/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

# Default values:
DEFAULT_FOLDER = os.getcwd() # Get the current working directory
DEFAULT_REPOSITORY_URL = "https://github.com/apache/commons-lang"
FULL_CK_METRICS_OUTPUT_DIRECTORY_PATH = os.getcwd() + RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH
FULL_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH = os.getcwd() + RELATIVE_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH
FULL_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH = os.getcwd() + RELATIVE_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH
FULL_REPOSITORY_DIRECTORY_PATH = os.getcwd() + RELATIVE_REPOSITORY_DIRECTORY_PATH
FULL_CK_JAR_PATH = os.getcwd() + RELATIVE_CK_JAR_PATH

# Default Method Names:
METHODS_NAME = ["isNumericSpace", "isNullOrZero", "CharSequenceUtils"]

# @brief: This verifies if all the metrics are already calculated
# @param: repository_name: Name of the repository to be analyzed
# @return: True if all the metrics are already calculated, False otherwise
def check_metrics_folders(repository_name):
    print(f"{backgroundColors.OKGREEN}Checking if all the metrics are already calculated{Style.RESET_ALL}")
    current_path = os.getcwd()
    data_path = os.path.join(current_path, 'ck_metrics')
    repo_path = os.path.join(data_path, repository_name)
    commit_file = f'commit_hashes-{repository_name}.txt'
    commit_file_path = os.path.join(data_path, commit_file)

    if not os.path.exists(commit_file_path):
        print(f"{backgroundColors.FAIL}File '{commit_file}' does not exist inside '{data_path}'.{Style.RESET_ALL}")
        return

    with open(commit_file_path, 'r') as file:
        lines = file.readlines()

    for line in lines:
        folder_name = line.strip()
        folder_path = os.path.join(repo_path, folder_name)

        if not os.path.exists(folder_path):
            print(f"{backgroundColors.FAIL}Folder '{folder_name}' does not exist inside '{repo_path}'.{Style.RESET_ALL}")
            return False
    return True

# @brief: This function checks if there is any whitespace current working directory
# @param: None
# @return: None
def check_whitespace():
    if ' ' in os.getcwd():
        print(f"{backgroundColors.FAIL}The current working directory contains whitespace{Style.RESET_ALL}")
        print(f"{backgroundColors.FAIL}Please remove the whitespace and try again{Style.RESET_ALL}")
        exit()

# @brief: Get the user input and check if they are empty
# @param: None
# @return: repository_url: URL of the repository to be analyzed
def get_user_input():
    # Ask for user input of the repository URL
    repository_url = input(f"Enter the repository URL: ")

    # Return the repository URL
    return check_url_input(repository_url)

# brief: Get user method name input
# param: None
# return: method_name: Name of the method to be analyzed
def get_user_method_input():
    # Ask for user input of the method name
    method_name = input(f"Enter the method name: ")

    # If empty, get from the method_names list
    if not method_name:
        method_name = METHODS_NAME[0]
        print(f"{backgroundColors.OKGREEN}Using the default method name: {backgroundColors.OKCYAN}{method_name}{Style.RESET_ALL}")

    # Return the method name
    return method_name

# @brief: If inputs are empty, use the default values
# @param: repository_url: URL of the repository to be analyzed
# @param: output_directory: Directory to save the output files
# @return: The repository URL and the output directory
def check_url_input(repository_url):
    if not repository_url:
        repository_url = DEFAULT_REPOSITORY_URL
    return repository_url

# @brief: Get the string after the last slash
# @param: url: URL of the repository to be analyzed
# @return: The name of the repository
def get_repository_name(url):
    return url.split("/")[-1]

# @brief: Update the repository using "git pull"
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def update_repository(repository_name):
    print(f"Updating the {backgroundColors.OKGREEN}{repository_name}{Style.RESET_ALL} repository using {backgroundColors.OKGREEN}git pull{Style.RESET_ALL}.")
    os.chdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name)
    # Create a thread to update the repository located in RELATIVE_REPOSITORY_DIRECTORY + '/' + repository_name
    update_thread = subprocess.Popen(["git", "pull"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for the thread to finish
    update_thread.wait()
    os.chdir(DEFAULT_FOLDER)

# @brief: Clone the repository to the repository directory
# @param: repository_url: URL of the repository to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def clone_repository(repository_url, repository_name):
    # Check if the repository directory already exists and if it is not empty
    if os.path.isdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name) and os.listdir(FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name):
        print(f"The {backgroundColors.OKGREEN}{repository_name}{Style.RESET_ALL} repository is already cloned!")
        update_repository(repository_name)
        return
    else:
        print(f"Cloning the {backgroundColors.OKGREEN}{repository_name}{Style.RESET_ALL} repository...")
        # Create a thread to clone the repository
        thread = subprocess.Popen(["git", "clone", repository_url, FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for the thread to finish
        thread.wait()
        print(f"Successfully cloned the {backgroundColors.OKGREEN}{repository_name}{Style.RESET_ALL} repository")

# @brief: Create a subdirectory
# @param: full_directory_name: Name of the directory to be created
# @param: relative_directory_name: Relative name of the directory to be created that will be shown in the terminal
# @return: None
def create_directory(full_directory_name, relative_directory_name):
    if os.path.isdir(full_directory_name): # Check if the directory already exists
        # print(f"The {backgroundColors.OKCYAN}{relative_directory_name}{Style.RESET_ALL} directory already exists")
        return
    try: # Try to create the directory
        os.makedirs(full_directory_name)
        print (f"Successfully created the {backgroundColors.OKCYAN}{relative_directory_name}{Style.RESET_ALL} directory")
    except OSError: # If the directory cannot be created
        print (f"The creation of the {backgroundColors.OKCYAN}{relative_directory_name}{Style.RESET_ALL} directory failed")

# @brief: This function is used to checkout a specific branch
# @param: branch_name: Name of the branch to be checked out
# @return: None
def checkout_branch(branch_name):
    # Create a thread to checkout the branch
    checkout_thread = subprocess.Popen(["git", "checkout", branch_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for the thread to finish
    checkout_thread.wait()

# @brief: This function is analyze the repository metrics evolution over time
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def analyze_method_evolution(repository_name, method_name):
    print(f"{backgroundColors.OKGREEN}Analyzing the {backgroundColors.OKCYAN}{repository_name}{backgroundColors.OKGREEN} repository for the {backgroundColors.OKCYAN}{method_name}{backgroundColors.OKGREEN} method...{Style.RESET_ALL}")

    last_metrics = None
    method_data = []
    method_variables_counter = [0, 0]

    # Get the list of commit hashes
    commit_hashes = os.listdir(f"ck_metrics/{repository_name}/")
    
    for commit_hash in tqdm(commit_hashes):
        method_path = f"ck_metrics/{repository_name}/{commit_hash}/method.csv"

        # Check if the method file exists for the current commit hash
        if os.path.isfile(method_path):
            with open(method_path, "r") as file:
                reader = csv.DictReader(file) # Read the method.csv file
                
                # Search for the method in the current commit's method.csv file
                for row in reader:
                    if row["method"].split('/')[0] == method_name:
                        method_variables_counter[0] += 1
                        cbo = int(row["cbo"])
                        wmc = int(row["wmc"])
                        cboModified = int(row["cboModified"])
                        rfc = int(row["rfc"])
                        metrics = (cbo, wmc, cboModified, rfc)
                        data = (commit_hash, cbo, wmc, cboModified, rfc)
                        
                        # Store the metrics if they are different from the last recorded metrics
                        if metrics != last_metrics:
                            method_data.append(data)
                            last_metrics = metrics
                            method_variables_counter[1] += 1
                        break

    # If the method_data is empty, then the method was not found
    if not method_data:
        print(f"{backgroundColors.FAIL}Method {backgroundColors.OKCYAN}{method_name}{backgroundColors.FAIL} not found{Style.RESET_ALL}")
        return
    
    print(f"{backgroundColors.OKGREEN}The method {backgroundColors.OKCYAN}{method_name}{backgroundColors.OKGREEN} changed {backgroundColors.OKCYAN}{method_variables_counter[1]} of {method_variables_counter[0]}{backgroundColors.OKGREEN} time(s){Style.RESET_ALL}")

    # Write the method_data to a file in the /metrics_evolution folder
    output_file = f"metrics_evolution/{method_name}.csv"
    with open(output_file, 'w') as file:
        writer = csv.writer(file)
        writer.writerow([f"{method_name}", "cbo", "wmc", "cboModified", "rfc"])
        writer.writerows(method_data)
    print(f"{backgroundColors.OKGREEN}Successfully wrote the method evolution to {backgroundColors.OKCYAN}{output_file}{Style.RESET_ALL}")
    print()

# @brief: This function is used to analyze the repository metrics evolution over time for the CSV files in the given directory
# @param: directory: Directory containing the CSV files to be analyzed
# @return: None
def calculate_statistics(directory, output_file):
    print(f"{backgroundColors.OKGREEN}Calculating statistics for CSV files in {backgroundColors.OKCYAN}{directory}{Style.RESET_ALL}")

    # Create the output file
    with open(output_file, "w", newline='') as csvfile:
        writer = csv.writer(csvfile) # Create a CSV writer
        # Write the header row
        writer.writerow(["File", "Metric", "Min", "Max", "Average", "Median", "Third Quartile"])

        # Iterate through the CSV files in the directory RELATIVE_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH
        for root, dirs, files in os.walk(directory):
            # Iterate through the files in the current directory 
            for file in files:
                # Check if the file is a CSV file
                if file.endswith(".csv"):
                    file_path = os.path.join(root, file) # Get the full path of the file
                    print(f"{backgroundColors.OKGREEN}Calculating statistics for {backgroundColors.OKCYAN}{file_path}{Style.RESET_ALL}")
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

# @brief: Main function
# @param: None
# @return: None
def main():
    # Check if the current working directory contains whitespace
    check_whitespace()

    # Get the user input
    repository_url = get_user_input()

    # Get the name of the repository
    repository_name = get_repository_name(repository_url)

    # create the metrics_evolution directory
    create_directory(FULL_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH, RELATIVE_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH)

    # create the metrics_statistics directory
    create_directory(FULL_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH, RELATIVE_METRICS_STATISTICS_OUTPUT_DIRECTORY_PATH)

    # Check if the metrics were already calculated
    if not check_metrics_folders(repository_name):
        # Create the repositories directory
        create_directory(FULL_REPOSITORY_DIRECTORY_PATH, RELATIVE_REPOSITORY_DIRECTORY_PATH)

        # Clone the repository
        clone_repository(repository_url, repository_name)
        
        i = 1
        commit_hashes = ""
        
        number_of_commits = len(list(Repository(repository_url).traverse_commits()))
        print(f"Total number of commits: {backgroundColors.OKGREEN}{number_of_commits}{Style.RESET_ALL}")
        
        for commit in Repository(repository_url).traverse_commits():
            commit_hashes += f"{commit.hash}\n"

            workdir_directory = FULL_REPOSITORY_DIRECTORY_PATH + '/' + repository_name
            os.chdir(workdir_directory)        
            checkout_branch(commit.hash)

            # Create the output directory
            output_directory = FULL_CK_METRICS_OUTPUT_DIRECTORY_PATH + '/' + repository_name + '/' + commit.hash + '/'
            relative_output_directory = RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH + '/' + repository_name + '/' + commit.hash + '/'
            create_directory(output_directory, relative_output_directory)

            # change working directory to the repository directory
            os.chdir(output_directory)

            # Run ck metrics for every commit hash
            cmd = f"java -jar {FULL_CK_JAR_PATH} {workdir_directory} false 0 false {output_directory}"
            relative_cmd = f"{backgroundColors.OKGREEN}java -jar {backgroundColors.OKCYAN}{RELATIVE_CK_JAR_PATH} {RELATIVE_REPOSITORY_DIRECTORY_PATH}/{repository_name}{backgroundColors.OKGREEN} false 0 false {backgroundColors.OKCYAN}{RELATIVE_CK_METRICS_OUTPUT_DIRECTORY_PATH}/{repository_name}/{commit.hash}/"
            
            print(f"{backgroundColors.OKCYAN}{i} of {number_of_commits}{Style.RESET_ALL} - Running CK: {relative_cmd}{Style.RESET_ALL}")
            
            process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()
            print(stdout.decode())
            
            i += 1

        with open(FULL_CK_METRICS_OUTPUT_DIRECTORY_PATH + '/' + 'commit_hashes-' + repository_name + '.txt', 'w') as file:
            file.write(commit_hashes)

        checkout_branch("main")

    # Calculate the CBO and WMC metrics evolution for the given method
    analyze_method_evolution(repository_name, get_user_method_input())

    # Calculate the statistics for the CSV files in the metrics_evolution directory
    calculate_statistics(FULL_METRICS_EVOLUTION_OUTPUT_DIRECTORY_PATH, 'metrics_statistics' + '/' + repository_name + '.csv')

# Directly run the main function if the script is executed
if __name__ == '__main__':
    main() # Run the main function