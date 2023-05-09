# TODO: Olhar como ele percorre a árvore dos commits
# TODO: Color the output messages
# TODO: Informar o último parâmetro o diretório de saída
# TODO: Pegar o número total de commits
# TODO: Criar progress bar para o for dos commits

import os # OS module in Python provides functions for interacting with the operating system
import subprocess # The subprocess module allows you to spawn new processes, connect to their input/output/error pipes, and obtain their return codes
from pydriller import Repository # PyDriller is a Python framework that helps developers in analyzing Git repositories. 

DEFAULT_REPOSITORY_URL = "https://github.com/apache/commons-lang"
DEFAULT_OUTPUT_DIRECTORY = os.getcwd() + "/data"
DEFAULT_REPOSITORY_DIRECTORY = os.getcwd() + "/repositories"
CK_JAR = os.getcwd() + "/ck/ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar"

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

# @brief: Clone the repository to the repository directory
# @param: repository_url: URL of the repository to be analyzed
# @param: repository_name: Name of the repository to be analyzed
# @return: None
def clone_repository(repository_url, repository_name):
    # Check if the repository directory already exists and if it is not empty
    if os.path.isdir(DEFAULT_REPOSITORY_DIRECTORY + '/' + repository_name) and os.listdir(DEFAULT_REPOSITORY_DIRECTORY + '/' + repository_name):
        print(f"The {repository_name.upper()} repository is already cloned!")
        return
    else:
        print(f"Cloning the {repository_name.upper()} repository...")
        # Create a thread to clone the repository
        thread = subprocess.Popen(["git", "clone", repository_url, DEFAULT_REPOSITORY_DIRECTORY + '/' + repository_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # Wait for the thread to finish
        thread.wait()
        print(f"Successfully cloned the {repository_name.upper()} repository")

# @brief: Create a subdirectory
# @param: directory_name: Name of the directory to be created
# @return: None
def create_directory(directory_name):
    if os.path.isdir(directory_name): # Check if the directory already exists
        print(f"The {directory_name.upper()} directory already exists")
        return
    try: # Try to create the directory
        os.makedirs(directory_name)
        print (f"Successfully created the {directory_name.upper()} directory")
    except OSError: # If the directory cannot be created
        print (f"The creation of the {directory_name.upper()} directory failed")

# @brief: This function is used to checkout a specific branch
# @param: branch_name: Name of the branch to be checked out
# @return: None
def checkout_branch(branch_name):
    # Create a thread to checkout the branch
    thread = subprocess.Popen(["git", "checkout", branch_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # Wait for the thread to finish
    thread.wait()

# @brief: Main function
# @param: None
# @return: None
def main():
    # Get the user input
    repository_url = get_user_input()

    # Get the name of the repository
    repository_name = get_repository_name(repository_url)

    # Create the repositories directory
    create_directory(DEFAULT_REPOSITORY_DIRECTORY)

    # Clone the repository
    clone_repository(repository_url, repository_name)
    
    i = 1
    file_data = ""
    for commit in Repository(repository_url).traverse_commits():
        file_data += f"{commit.hash}\n"

        workdir_directory = DEFAULT_REPOSITORY_DIRECTORY + '/' + repository_name
        os.chdir(workdir_directory)        
        checkout_branch(commit.hash)

        # Create the output directory
        output_directory = DEFAULT_OUTPUT_DIRECTORY + '/' + repository_name + '/' + commit.hash + '/'
        create_directory(output_directory)

        # change working directory to the repository directory
        os.chdir(output_directory)

        print("{i}ª - Running CK:", cmd)
         
        # Run ck metrics for every commit hash
        cmd = f"java -jar {CK_JAR} {workdir_directory} false 0 false {output_directory}"
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())
        
        i += 1

    with open(DEFAULT_OUTPUT_DIRECTORY + '/' + repository_name + '.txt', 'w') as file:
        file.write(file_data)

    checkout_branch("main")

if __name__ == '__main__':
    main() 