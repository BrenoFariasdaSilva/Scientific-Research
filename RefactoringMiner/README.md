<div align="center">
  
# [Refactoring Miner.](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/RefactoringMiner) <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to the Refactoring Miner folder, in which you will find the scripts used to generate the refactoring miner refactoring scripts of the metrics evolution of a class or method of the repositories of interest.  
RefactoringMiner is a valuable tool for software maintenance and evolution analysis, helping developers and researchers understand how code evolves over time through refactorings.
  
---

</div> 

- [Refactoring Miner. ](#refactoring-miner-)
  - [Important Notes](#important-notes)
  - [Setup](#setup)
    - [Python and Pip](#python-and-pip)
      - [Linux](#linux)
      - [MacOS](#macos)
      - [Windows](#windows)
    - [Requirements](#requirements)
    - [Cleaning Up](#cleaning-up)
  - [Usage](#usage)
    - [Repositories Refactors](#repositories-refactors)
    - [Metrics Evolution Refactors](#metrics-evolution-refactors)
    - [Cleaning Up](#cleaning-up-1)
  - [Workflow](#workflow)
  - [Python Scripts](#python-scripts)
    - [Metrics Evolution Refactors](#metrics-evolution-refactors-1)
    - [Repositories Refactors](#repositories-refactors-1)
    - [RefactoringMiner JSON Output](#refactoringminer-json-output)
  - [Troubleshooting](#troubleshooting)
  - [Contributing](#contributing)
  - [License](#license)

## Important Notes
- Make sure you don't have whitespaces in the path of the project, otherwise it will not work.
- All of the Scripts have a `VERBOSE` constant, which is set to `False` by default, so it will only print the progress bar of the script execution. If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`.
- All of the Scripts have a `Makefile`that handles virtual environment creation, dependencies installation and script execution. You can run the scripts by using the `make` command, as shown in the `How to use` section.

## Setup

This section provides instructions for installing the Python Language and Pip Python package manager, as well as the project's dependencies. It also explains how to run the scripts using the provided `makefile`. The `makefile` automates the process of creating a virtual environment, installing dependencies, and running the scripts.

### Python and Pip

In order to run the scripts, you must have python3 and pip installed in your machine. If you don't have it installed, you can use the following commands to install it:

#### Linux

In order to install python3 and pip in Linux, you can use the following commands:

```
sudo apt install python3 -y
sudo apt install python3-pip -y
```

#### MacOS

In order to install python3 and pip in MacOS, you can use the following commands:

```
brew install python3
```

#### Windows

In order to install python3 and pip in Windows, you can use the following commands in case you have `choco` installed:

```
choco install python3
```

Or just download the installer from the [official website](https://www.python.org/downloads/).

Great, you now have python3 and pip installed. Now, we need to install the project requirements/dependencies.

### Requirements

This project depends on the following libraries:

- [NumPy](https://numpy.org/) -> NumPy is used to generate the linear prediction of the linear regression and to many operations in the list of the metrics.
- [Pandas](https://pandas.pydata.org/) -> Pandas is used maintly to read and write the csv files.
- [TQDM](https://tqdm.github.io/) -> TQDM is used to show the progress bar of the scripts.

Futhermore, this project requires a virtual environment to ensure all dependencies are installed and managed in an isolated manner. A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Using a virtual environment helps avoid conflicts between project dependencies and system-wide Python packages. 

To set up and use a virtual environment for this project, we leverage Python's built-in `venv` module. The `makefile` included with the project automates the process of creating a virtual environment, installing the necessary dependencies, and running scripts within this environment.

Follow these steps to prepare your environment:

1. **Create and Activate the Virtual Environment:** 
   
   The project uses a `makefile` to streamline the creation and activation of a virtual environment named `venv`. This environment is where all required packages, such as `numpy`, `pandas` and `tqdm`, will be installed.
This will also be handled by the `Makefile` during the dependencies installation process, so no command must be executed in order to create the virtual environment.

1. **Install Dependencies:** 
   
   Run the following command to set up the virtual environment and install all necessary dependencies on it:

      ```
      make dependencies
      ```

   This command performs the following actions:
   - Initializes a new virtual environment by running `python3 -m venv venv`.
   - Installs the project's dependencies within the virtual environment using `pip` based on the `requirements.txt` file. The `requirements.txt` file contains a list of all required packages and their versions. This is the recommended way to manage dependencies in Python projects, as it allows for consistent and reproducible installations across different environments.

3. **Running Scripts:**
   
   The `makefile` also defines commands to run every script with the virtual environment's Python interpreter. For example, to run the `repositories_refactors.py` file, use:

  ```
  make repositories_refactors_script
  ```

  This ensures that the script runs using the Python interpreter and packages installed in the `venv` directory.

### Cleaning Up

To clean your project directory from the virtual environment and Python cache files, use the `clean` rule defined in the `makefile`:

```
make clean
```

This command removes the `venv` directory and deletes all compiled Python files in the project directory, helping maintain a clean workspace.

By following these instructions, you'll ensure that all project dependencies are correctly managed and isolated, leading to a more stable and consistent development environment.

## Usage

### Repositories Refactors

To use the script for repositories refactor analysis, follow these steps:

1. Open a terminal in the `RefactoringMiner` directory.

2. Run the script using the following command:

  ```shell
  make repositories_refactors_script
  ```

### Metrics Evolution Refactors

In order to use the script for the analysis of the metrics evolution of a class or method, follow these steps:

1. Make sure you have the PyDriller Metrics Evolution files that should be located as follows, otherwise it will not work:
  ```shell
  Scientific-Research/PyDriller/metrics_evolution
  ```
2. If you have the PyDriller Metrics Evolution files, simply open a terminal in the `RefactoringMiner` directory and run the script using the following command:

  ```shell
  make metrics_evolution_refactors_script
  ```

**Running Scripts:** The `makefile` handles for each of the python code to run with the virtual environment's Python interpreter. So, this ensures that the script runs using the Python interpreter and packages installed in the `venv` directory.

### Cleaning Up

To clean your project directory from the virtual environment and Python cache files, use the `clean` rule defined in the `makefile`:
```shell
make clean
```
This command removes the `venv` directory and deletes all compiled Python files in the project directory, helping maintain a clean workspace.

By following these instructions, you'll ensure that all project dependencies are correctly managed and isolated, leading to a more stable and consistent development environment.

## Workflow

Here's a brief overview of how the script works:

1. It defines several constants, paths, and default values used throughout the script.

2. The script checks for prerequisites and directory structures.

3. It clones or updates a specified GitHub repository using Git or opens the generated files by PyDriller.

4. For each class or method specified in `FILES_TO_ANALYZE`, it generates refactoring data for commits in the repository concurrently, using multiple threads.

5. Refactoring data is stored in JSON files in the `json_files` directory.

## Python Scripts

In this section, we provide explanations for each function in the provided Python script and introduce RefactoringMiner, an essential tool used by the script.

### Metrics Evolution Refactors
Before running the script, be sure to modify the following variables to suit your needs:  
`DESIRED_REFACTORING_TYPES` - The refactoring types to be analyzed. Must names of the refactorings detected by RefactoringMiner. See more [here](https://github.com/tsantalis/RefactoringMiner#general-info).  
`DEFAULT_REPOSITORY` - The default repository to clone or update. Must be a value that is in the DEFAULT_REPOSITORIES dictionary.  
`FILES_TO_ANALYZE` - The files to analyze in the repository must be names of classes or methods that were generated by PyDriller.  

1. The first thing this script does is verify  if the path contains whitespace, if so, it will not work, so it will ask the user to remove the whitespace from the path and then run the script again.
2. Now it will create the json output directory and the repository directory if they don't exist.
3. Now it calls `process_repository(DEFAULT_REPOSITORY, DEFAULT_REPOSITORIES[DEFAULT_REPOSITORY])`, which will do the following steps:
   1. Clone or update the repository, depending on whether it already exists or not.
   2. Then, it calls `generate_refactorings_concurrently(repository_name)` where, for each of the items in the `FILES_TO_ANALYZE` dictionary, creating a thread for handling the analysis of each file.
        1. In this function, it will loop through each of the commit hashes in the csv from the `PyDriller/metrics_evolution` directory and generate the refactorings for that commit hash using the `-c` parameter of the `RefactoringMiner` tool and save the output in the `json_files` directory.
        2. Lastly, it calls the `filter_json_file(classname, json_filepath, json_filtered_filepath)` that will read the generated json file and filter the refactorings by the `DESIRED_REFACTORING_TYPES` variable and save the filtered refactorings in the `json_files` directory.
4. Lastly, it will output the execution time of the script.

### Repositories Refactors
Before running the script, be sure to modify the following variables to suit your needs:  
`DEFAULT_REPOSITORIES` - The repositories to be analyzed. Must be a dictionary with the name of the repository as the key and the URL of the repository as the value.  
`COMMITS_NUMBER` - The number of commits that the corresponding repository have. It is useful for calculing the estimated time of the script.  
`ITERATIONS_PER_SECOND` - The number of iterations per second that the script will do. It is useful for calculing the estimated time of the script. Usually, it is 4, but it can be more or less, depending on the machine that you are running the script and the size commits of the repository.  

1. The first thing this script does is verify  if the path contains whitespace, if so, it will not work, so it will ask the user to remove the whitespace from the path and then run the script again.
2. Now it calls the `verify_refactorings()` to verify if the RefactoringMiner refactorings for the DEFAULT_REFACTORINGS were already generated. If not, it will generate them.
3. will create the json output directory and the repository directory if they don't exist.
4. Now it calls `process_repositories_concurrently(repositories)`, which will do the following steps:
   1. This function will loop through each of the repositories in the `DEFAULT_REPOSITORIES` dictionary and create a thread for handling the analysis of each repository.
   2. Inside the thread, it will clone or update the repository, depending on whether it already exists or not.
   3. After that, the thread will generate the refactorings for each of the commits in the repository using the `-a` parameter of the `RefactoringMiner` tool and save the output in the `json_files` directory.
5. Lastly, it will output the execution time of the script.

### RefactoringMiner JSON Output

The script generates JSON files containing refactoring data for commits in the specified classes or methods of the repository. These files are organized in the `json_files` directory, following the repository's structure.

## Troubleshooting

If you encounter any issues while using the script, consider the following:

- Ensure that you have the required prerequisites installed and available in your system.

- Check the repository URL and make sure it is accessible.

- Verify that the paths specified in the script are correct, and the necessary directories exist.

- Verify if you have the PyDriller Metrics Evolution files that should be located as follows, otherwise it will not work:
  ```shell
  Scientific-Research/PyDriller/metrics_evolution
  ```

## Contributing

If you want to contribute to this project, please read the Contributing section of the [Main README](../README.md) file, as well as the [CONTRIBUTING](../CONTRIBUTING.md) file in this repository.

## License

This project is licensed under the [Apache License 2.0](../LICENSE). This license permits use, modification, distribution, and sublicense of the code for both private and commercial purposes, provided that the original copyright notice and a disclaimer of warranty are included in all copies or substantial portions of the software. It also requires a clear attribution back to the original author(s) of the repository. For more details, see the [LICENSE](../LICENSE) file in this repository.
