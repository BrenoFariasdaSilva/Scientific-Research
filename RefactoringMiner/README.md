<div align="center">
  
# [Refactoring Miner.](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/RefactoringMiner) <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to the Refactoring Miner folder, in which you will find the scripts used to generate the refactoring miner refactoring scripts of the metrics evolution of a class or method of the repositories of interest.
  
---

</div>

@TODO: Format  
@TODO: Add a section explaining the files and the directory structure  
@TODO: Add a section explaining the output  

- [Refactoring Miner. ](#refactoring-miner-)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Function Explanations and RefactoringMiner](#function-explanations-and-refactoringminer)
  - [Function Explanations](#function-explanations)
    - [1. `path_contains_whitespaces()`](#1-path_contains_whitespaces)
    - [2. `create_directory(full_directory_name, relative_directory_name)`](#2-create_directoryfull_directory_name-relative_directory_name)
    - [3. `process_repository(repository_name, repository_url)`](#3-process_repositoryrepository_name-repository_url)
    - [4. `clone_repository(repository_name, repository_url)`](#4-clone_repositoryrepository_name-repository_url)
    - [5. `update_repository(repository_name)`](#5-update_repositoryrepository_name)
    - [6. `generate_refactorings_concurrently(repository_name)`](#6-generate_refactorings_concurrentlyrepository_name)
    - [7. `generate_commit_refactors_for_class_or_methods(repository_name, classname, variable_attribute)`](#7-generate_commit_refactors_for_class_or_methodsrepository_name-classname-variable_attribute)
    - [8. `output_time(output_string, time)`](#8-output_timeoutput_string-time)
    - [9. `play_sound()`](#9-play_sound)
    - [10. `main()`](#10-main)
  - [RefactoringMiner](#refactoringminer)
    - [Purpose](#purpose)
    - [Usage in the Script](#usage-in-the-script)
    - [Output](#output)
    - [Integration](#integration)
- [Output](#output-1)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)

# Prerequisites

Before using this script, ensure you have the following prerequisites installed:
- Python 3.x
- Git
- RefactoringMiner tool (included in the project)
- PyDriller library (not included in the project)
- Pandas library (not included in the project)
- Colorama library (not included in the project)

# Installation

To install and set up the required environment for the script, follow these steps:

1. Clone this repository to your local machine:
   
   ```shell
  git clone https://github.com/BrenoFariasdaSilva/Scientific-Research
   ```

2. Navigate to the `RefactoringMiner` directory:
   
   ```shell
  cd Scientific-Research/RefactoringMiner
   ```

3. Install the necessary Python libraries using pip:

  ```shell
  make dependencies
  ```

1. Run the desired scripts using the following command:

  ```shell
  make repositories_refactors_script
  ```
  or 
  ```shell
  make metrics_evolution_refactors_script
  ```


# Usage

To use the script for repository analysis, follow these steps:

1. Open a terminal.

2. Navigate to the directory where the script is located.

3. Run the script using the following command:

   ```shell
   python script.py

# Workflow

Here's a brief overview of how the script works:

1. It defines several constants, paths, and default values used throughout the script.

2. The script checks for prerequisites and directory structures.

3. It clones or updates a specified GitHub repository using Git.

4. For each class or method specified in `FILES_TO_ANALYZE`, it generates refactoring data for commits in the repository concurrently, using multiple threads.

5. Refactoring data is stored in JSON files in the `json_files` directory.

# Function Explanations and RefactoringMiner

In this section, we provide explanations for each function in the provided Python script and introduce RefactoringMiner, an essential tool used by the script.

## Function Explanations

### 1. `path_contains_whitespaces()`
- **Purpose**: Checks if the `START_PATH` constant contains whitespaces.
- **Return**: `True` if `START_PATH` contains whitespaces, `False` otherwise.

### 2. `create_directory(full_directory_name, relative_directory_name)`
- **Purpose**: Creates a directory with the given name.
- **Parameters**:
  - `full_directory_name`: Name of the directory to be created (full path).
  - `relative_directory_name`: Relative name of the directory shown in the terminal.
- **Return**: None

### 3. `process_repository(repository_name, repository_url)`
- **Purpose**: Analyzes a specified repository.
- **Parameters**:
  - `repository_name`: Name of the repository to be analyzed.
  - `repository_url`: URL of the repository to be analyzed.
- **Return**: None

### 4. `clone_repository(repository_name, repository_url)`
- **Purpose**: Clones or updates a GitHub repository.
- **Parameters**:
  - `repository_name`: Name of the repository to be cloned or updated.
  - `repository_url`: URL of the repository to be cloned or updated.
- **Return**: None

### 5. `update_repository(repository_name)`
- **Purpose**: Updates an existing GitHub repository using `git pull`.
- **Parameters**:
  - `repository_name`: Name of the repository to be updated.
- **Return**: None

### 6. `generate_refactorings_concurrently(repository_name)`
- **Purpose**: Generates refactoring data concurrently for multiple classes or methods in a repository.
- **Parameters**:
  - `repository_name`: Name of the repository to be analyzed.
- **Return**: None

### 7. `generate_commit_refactors_for_class_or_methods(repository_name, classname, variable_attribute)`
- **Purpose**: Generates refactoring data for a specific class or method in a repository.
- **Parameters**:
  - `repository_name`: Name of the repository to be analyzed.
  - `classname`: Name of the class to be analyzed.
  - `variable_attribute`: Name of the variable or attribute to be analyzed.
- **Return**: None

### 8. `output_time(output_string, time)`
- **Purpose**: Outputs time considering the appropriate time unit (e.g., seconds, minutes, hours, or days).
- **Parameters**:
  - `output_string`: String to be displayed.
  - `time`: Time value to be displayed.
- **Return**: None

### 9. `play_sound()`
- **Purpose**: Defines the command to play a sound when the program finishes.
- **Parameters**: None
- **Return**: None

### 10. `main()`
- **Purpose**: Main function that coordinates the script's execution.
- **Parameters**: None
- **Return**: None

## RefactoringMiner

### Purpose
RefactoringMiner is a Java-based tool designed to detect refactorings in the commit history of Git repositories. It identifies refactorings like method extractions, renames, and more.

### Usage in the Script
In this script, RefactoringMiner is invoked through subprocess calls to analyze commits and generate refactoring data in JSON format.

### Output
RefactoringMiner generates JSON files containing information about detected refactorings, which are then processed by this script.

### Integration
The script runs RefactoringMiner by specifying the repository path, commit hash, and output JSON file path. It uses the extracted refactoring data for further analysis.

RefactoringMiner is a valuable tool for software maintenance and evolution analysis, helping developers and researchers understand how code evolves over time through refactorings.
- [Refactoring Miner. ](#refactoring-miner-)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Workflow](#workflow)
- [Function Explanations and RefactoringMiner](#function-explanations-and-refactoringminer)
  - [Function Explanations](#function-explanations)
    - [1. `path_contains_whitespaces()`](#1-path_contains_whitespaces)
    - [2. `create_directory(full_directory_name, relative_directory_name)`](#2-create_directoryfull_directory_name-relative_directory_name)
    - [3. `process_repository(repository_name, repository_url)`](#3-process_repositoryrepository_name-repository_url)
    - [4. `clone_repository(repository_name, repository_url)`](#4-clone_repositoryrepository_name-repository_url)
    - [5. `update_repository(repository_name)`](#5-update_repositoryrepository_name)
    - [6. `generate_refactorings_concurrently(repository_name)`](#6-generate_refactorings_concurrentlyrepository_name)
    - [7. `generate_commit_refactors_for_class_or_methods(repository_name, classname, variable_attribute)`](#7-generate_commit_refactors_for_class_or_methodsrepository_name-classname-variable_attribute)
    - [8. `output_time(output_string, time)`](#8-output_timeoutput_string-time)
    - [9. `play_sound()`](#9-play_sound)
    - [10. `main()`](#10-main)
  - [RefactoringMiner](#refactoringminer)
    - [Purpose](#purpose)
    - [Usage in the Script](#usage-in-the-script)
    - [Output](#output)
    - [Integration](#integration)
- [Output](#output-1)
- [Customization](#customization)
- [Troubleshooting](#troubleshooting)


# Output

The script generates JSON files containing refactoring data for commits in the specified classes or methods of the repository. These files are organized in the `json_files` directory, following the repository's structure.

# Customization

You can customize the script's behavior by modifying the constants defined at the beginning of the script, such as `DEFAULT_REPOSITORY`, `FILES_TO_ANALYZE`, and others. These constants control which repository is analyzed and which classes or methods are considered for refactoring data generation.

# Troubleshooting

If you encounter any issues while using the script, consider the following:

- Ensure that you have the required prerequisites installed and available in your system.

- Check the repository URL and make sure it is accessible.

- Verify that the paths specified in the script are correct, and the necessary directories exist.

If you encounter any unexpected errors or issues, please consult the script's author or project documentation for further assistance.

Feel free to customize and extend the script to suit your specific needs. Happy analyzing!

