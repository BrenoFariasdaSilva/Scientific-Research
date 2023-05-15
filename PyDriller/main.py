# TODO: Olhar como ele percorre a árvore dos commits
# TODO: Informar o último parâmetro o diretório de saída

import os # OS module in Python provides functions for interacting with the operating system
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 
from colorama import Style # For coloring the terminal

# Macros:
class backgroundColors: # Colors for the terminal
	OKCYAN = "\033[96m" # Cyan
	OKGREEN = "\033[92m" # Green
	WARNING = "\033[93m" # Yellow
	FAIL = "\033[91m" # Red
 
# Relative paths:
RELATIVE_OUTPUT_DIRECTORY_PATH = "/data"
RELATIVE_REPOSITORY_DIRECTORY_PATH = "/repositories"
RELATIVE_CK_JAR_PATH = "/ck/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

# Default values:
DEFAULT_FOLDER = os.getcwd() # Get the current working directory
DEFAULT_REPOSITORY_URL = "https://github.com/apache/commons-lang"
FULL_OUTPUT_DIRECTORY_PATH = os.getcwd() + RELATIVE_OUTPUT_DIRECTORY_PATH
FULL_REPOSITORY_DIRECTORY_PATH = os.getcwd() + RELATIVE_REPOSITORY_DIRECTORY_PATH
FULL_CK_JAR_PATH = os.getcwd() + RELATIVE_CK_JAR_PATH

# @brief: Get the user input and check if they are empty
# @param: None
# @return: repository_url: URL of the repository to be analyzed
def get_user_input():
    # Ask for user input of the repository URL
    repository_url = input("Enter the repository URL: ")

    # Return the repository URL
    return check_url_input(repository_url)

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
        print(f"The {backgroundColors.OKCYAN}{relative_directory_name}{Style.RESET_ALL} directory already exists")
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

# @brief: Main function
# @param: None
# @return: None
def main():
    # Get the user input
    repository_url = get_user_input()

    # Get the name of the repository
    repository_name = get_repository_name(repository_url)

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
        output_directory = FULL_OUTPUT_DIRECTORY_PATH + '/' + repository_name + '/' + commit.hash + '/'
        relative_output_directory = RELATIVE_OUTPUT_DIRECTORY_PATH + '/' + repository_name + '/' + commit.hash + '/'
        create_directory(output_directory, relative_output_directory)

        # change working directory to the repository directory
        os.chdir(output_directory)

        # Run ck metrics for every commit hash
        cmd = f"java -jar {FULL_CK_JAR_PATH} {workdir_directory} false 0 false {output_directory}"
        relative_cmd = f"{backgroundColors.OKGREEN}java -jar {backgroundColors.OKCYAN}{RELATIVE_CK_JAR_PATH} {RELATIVE_REPOSITORY_DIRECTORY_PATH}/{repository_name}{backgroundColors.OKGREEN} false 0 false {backgroundColors.OKCYAN}{RELATIVE_OUTPUT_DIRECTORY_PATH}/{repository_name}/{commit.hash}/"
        
        print(f"{backgroundColors.OKCYAN}{i} of {number_of_commits}{Style.RESET_ALL} - Running CK: {relative_cmd}{Style.RESET_ALL}")
        
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())
        
        i += 1

    with open(FULL_OUTPUT_DIRECTORY_PATH + '/' + 'commit_hashes-' + repository_name + '.txt', 'w') as file:
        file.write(commit_hashes)

    checkout_branch("main")

if __name__ == '__main__':
    main() 