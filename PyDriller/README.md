<div align="center">

# [PyDriller.](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/PyDriller)  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

<div align="center">
  
---

Welcome to the PyDriller folder, in which you will find the scripts used to generate the ck metrics, metrics changes, metrics evolution, metrics linear predictions, graphics and commit files diff of the repositories of interest.

---

</div>

- [PyDriller.  ](#pydriller--)
    - [Important Notes:](#important-notes)
  - [Installation:](#installation)
    - [Requirements and Setup](#requirements-and-setup)
    - [Cleaning Up](#cleaning-up)
  - [How to use:](#how-to-use)
    - [Main Scripts:](#main-scripts)
      - [Code\_Metrics](#code_metrics)
      - [Metrics\_Changes](#metrics_changes)
    - [Auxiliar Scripts:](#auxiliar-scripts)
      - [Empty Folders](#empty-folders)
      - [Extract Zip Files](#extract-zip-files)
      - [Generate Zip Files](#generate-zip-files)
      - [Move Extracted Files](#move-extracted-files)
      - [Track Files:](#track-files)
  - [Dependencies:](#dependencies)
  - [Contributing:](#contributing)
  - [License:](#license)

### Important Notes:
- Make sure you don't have whitespaces in the path of the project, otherwise it will not work.
- All of the Scripts have a `VERBOSE` constant, which is set to `False` by default, so it will only print the progress bar of the script execution. If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`.
- All of the Scripts have a `Makefile`that handles virtual environment creation, dependencies installation and script execution. You can run the scripts by using the `make` command, as shown in the `How to use` section.
- The execution of this scripts will take a long time and store a lot of data, so make sure you have enough space in your disk and be patient. Example: Running all the scrips only for `Apache Kafka` generates a total of 115 GB of data.
- Why is `metrics_changes.py` not parallelized? Because, for example, for running for `Apache Kafka` it uses so much CPU and RAM that it crashed in my Ryzen 7 3800X with 32GB of RAM and there is also a lot of I/O to the disk. I tried creating a thread for process each repository, just like i did for `code_metrics.py`, but most of the times it just crashes after a minute running. Talking about the `code_metrics.py`, the most performance i could take from it was, as said, to create a thread to process each repository, therefore it isn't possible to parallelize inside the processing of the repository, as the result of the iteration number `x` depends on the result since the `first iteration until x-1`. If you want to parallelize something in order to improve performance, feel free to do it, i'll be glad aproving your pull request. Also, if the `code_metrics.py` crashes in the middle of the execution, you can just run it again, as it will verify if the ck metrics are already calculated and where it stopped, so it will continue from where it stopped.

## Installation:
You need to install python3. If you are using Linux, you (must likely) can install it by just running the following commands:
```
sudo apt install python3 -y
sudo apt install python3-pip -y
```
Great, you now have python3 and pip installed. Now, we need to install the project requirements/dependencies.

### Requirements and Setup

This project requires a virtual environment to ensure all dependencies are installed and managed in an isolated manner. A virtual environment is a self-contained directory tree that contains a Python installation for a particular version of Python, plus a number of additional packages. Using a virtual environment helps avoid conflicts between project dependencies and system-wide Python packages. 

To set up and use a virtual environment for this project, we leverage Python's built-in `venv` module. The `makefile` included with the project automates the process of creating a virtual environment, installing the necessary dependencies, and running scripts within this environment.

Follow these steps to prepare your environment:

1. **Create and Activate the Virtual Environment:** The project uses a `makefile` to streamline the creation and activation of a virtual environment named `venv`. This environment is where all required packages, such as `matplotlib`, `numpy`, `pandas`, `pydriller`, `scikit-learn` and `tqdm`, will be installed.
This will also be handled by the `Makefile` during the dependencies installation process, so no command must be executed in order to create the virtual environment.

2. **Install Dependencies:** Run the following command to set up the virtual environment and install all necessary dependencies on it:

  ```
  make dependencies
  ```

  This command performs the following actions:
  - Initializes a new virtual environment by running `python3 -m venv venv`.
  - Installs the project's dependencies within the virtual environment using `pip` based on the `requirements.txt` file.

3. **Running Scripts:** The `makefile` also defines commands to run every script with the virtual environment's Python interpreter. For example, to run the `code_metrics_script`, use:

  ```
  make code_metrics_script
  ```

  This ensures that the script runs using the Python interpreter and packages installed in the `venv` directory.

### Cleaning Up

To clean your project directory from the virtual environment and Python cache files, use the `clean` rule defined in the `makefile`:

```
make clean
```

This command removes the `venv` directory and deletes all compiled Python files in the project directory, helping maintain a clean workspace.

By following these instructions, you'll ensure that all project dependencies are correctly managed and isolated, leading to a more stable and consistent development environment.
	
## How to use: 
### Main Scripts:
#### Code_Metrics
To run this code as you want, you must modify the following constants:
1. `VERBOSE`: If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.
2. `DEFAULT_REPOSITORIES` dictionary in the `code_metrics.py` file, in which you must specify the repository name and the repository url. 
3. `ITERATIONS_DURATION` constant, which represents a simbolic time duration of the iterations of the `code_metrics.py` script for each repository. It is used to calculate the estimated time of the script execution. If you don't know, just kinda ignore it, but be aware that the bigger the repository is, the longer it will take to execute the script.
```
make code_metrics_script
```

Great now that you have set the constants, you can run the `code_metrics.py` file. The following steps will be executed by the `code_metrics.py` file:

1. As for every file in this project, the first thing it will do is verify if you don't have whitespaces in the path of the project, if you have, it will not work.  
2. Next, it will also verify if the `ck` file exists in the `FULL_CK_JAR_PATH` directory.
3. Now, it calls `process_repositories_concurrently()` which will create a thread for each of the repositories inside the `DEFAULT_REPOSITORIES` dictionary and process it's ck metrics and save each commit file diff. Each thread has as it's target the `process_repository(repository_name, repository_url)` function.
4. Now, the `verify_ck_metrics_folder(repository_name)` function  is called to verify if the ck metrics are already calculated. That verification is done by:
   1. Verifying if the repository commits list csv file exists inside the `CK_METRICS_DIRECTORY_PATH` directory, which should be named as `repository_name-commits_list.csv`, for example: `commons-lang-commits_list.csv`;
   2. If the csv file exists, it will, for every commit hash in the csv file, verify if there is a subdirectory inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, which should be named as `commit_hash` and contains all the ck metrics generated files, which are defined in the `CK_METRICS_FILES` constant;  
   
   If any of those verifications are false, it stops executing, due to the fact that the ck metrics weren't calculated. If not, it will continue executing until the end and return true, meaning that the ck metrics are already calculated.
5. Now, as the ck metrics are not calculated, it will call `create_directory(absolute path, relative_path)` twice, one for the `FULL_CK_METRICS_DIRECTORY_PATH` directory and another for the `FULL_REPOSITORY_DIRECTORY_PATH` directory.
6.  With all the subfolders created, we must call `clone_repository(repository_name, repository_url)` function, which will clone the repository to the `FULL_REPOSITORY_DIRECTORY_PATH` directory.
7. In this step, we must calculate the number of commit in the current repository in order to be able to call the `traverse_repository(repository_name, repository_url, number_of_commits)` function.
8. As now we have the repository cloned, we must call `traverse_repository` function, in which will loop through the repository commits tree with the use of `PyDriller.traverse_commits()` to go through all the commit hashes of the repository and do the following for each commit in the repository: 
   1. Get the tuple containing the `commit.hash`, `commit.msg` and `commit.author_date` and append those commit's data in the `commit_hashes` list, in order to, later on, store them inside the `CK_METRICS_DIRECTORY_PATH/repository_name-commit_hashes.csv` file;  
   2. Call `generate_diffs(repository_name, commit_hash, commit_number)`, which will fo through all the modified files of the current commit and store the diffs of the files in the `{cwd}{DEFAULT_DIFFS_DIRECTORY}/{repository_name}/{commit_number}-{commit_hash}/{modified_file.filename}{DIFF_FILE_EXTENSION}` folder;
   3. Now it must change the working directory to the `{FULL_REPOSITORIES_DIRECTORY_PATH}/{repository_name}` directory.
   4. Checkout to the `commit.hash` branch;  
   5. Create a subfolder inside the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name` named as `commit_number-commit.hash`;  
   6. Now it changes the working directory again to the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name/commit_number-commit.hash` directory, which is the output for the execution of the `ck` command for the current commit.hash;
   7. Lastly, with the call of the `run_ck_metrics_generator(cmd)` to execute the `cmd` command, which is a command defined to run ck for the current commit.hash and store the files that it generates in the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name/commit.hash` folder;  
9. Now that we have the list of tuples containing the commit hashes, commit message and commit date for each commit, we must store those values in the `CK_METRICS_DIRECTORY_PATH/repository_name-commits_list.csv` file, with the call of `write_commit_hashes_to_csv` function.
10. And lastly, we must call `checkout_branch` function passing the `main` branch as parameter, in order to return to the main branch of the repository.
11. After everything is done, the `code_metrics.py` script will be done and play a sound to notify you that the script has finished.

#### Metrics_Changes
To run this code as you want, you must modify the following constants:
1. `VERBOSE`: This is imported from the `code_metrics.py`file, in which you must specify if you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.
2. `DEFAULT_REPOSITORIES`: This is imported from the `code_metrics.py`file, in which you must specify the repository name and the repository url.
3. `MINIMUM_CHANGES`: This constant is used to specify the minimum number of changes that a class or method must have in order to be processed. If the class or method didn't have at least `MINIMUM_CHANGES` changes, it will not be processed.
4. `NUMBER_OF_METRIC`: This constant is used to specify the number of CK metrics that will be processed, in that case, it is set to 3 as we're using the `cbo`, `wmc` and `rfc` ck metrics.
5. `DESIRED_DECREASE`: This constant is used to specify the desired percentual of decrease of the metrics values in order to be considered a substantial change.
6. `IGNORE_CLASS_NAME_KEYWORDS`: This constant is used to specify the keywords that might be found in the class name that will be ignored in the substantial change verification. For example, if you want to ignore the classes that have the `Test` keyword in the class name, you must add it to the `IGNORE_CLASS_NAME_KEYWORDS` constant.
7. `IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS`: This constant is used to specify the keywords that might be found in the variable attribute that will be ignored in the substantial change verification. For example, if you want to ignore the classes of an specific type, like `anonymous`, `class`, `innerclasse`, `enum`, `interface`, `abstract`, you must add it to the `IGNORE_VARIABLE_ATTRIBUTE_KEYWORDS` list.
8. `SUBSTANTIAL_CHANGE_METRIC`: This constant is used to specify the metric that will be used to verify if the current metrics values of the current class or method had a substantial decrease. In that case, it is set to `CBO`, which is the metric that can indicate the level of complexity of a class or method.
9. `METRICS_POSITION`: This constant is used to specify the position of each used metric in the `metrics` list, which is used to generate the linear prediction of the linear regression. In that case, it is set to `0` for `CBO`, `1` for `WMC` and `2` for `RFC`.
10. `DESIRED_REFACTORINGS_ONLY`: This constant is used to specify if you want to store only the substantial changes that are of any of the specified refactorings in the `DESIRED_REFACTORINGS` list. If you want to store all the substantial changes, you must set it to `False`.
11. `DESIRED_REFACTORINGS`: This constant is used to specify the desired refactorings that you want to store in the `substantial_changes.csv` file. If you want to store all the substantial changes of any type, you must set the `DESIRED_REFACTORINGS_ONLY` constant to `False`.

Considering that you now have the ck metrics calculated and the constants set, you are able to run the following command to execute the `metrics_changes.py` file:
```
make metrics_changes_script
```
1. The first thing it will do is ask you if you want to process classes or methods, if you want to process classes, type ```True```, if you want to process methods, type ```False```. Note that it is case sensitive, so make sure you type it correctly.
2. The second thing it will do is verify if you don't have whitespaces in the path of the project by calling the `path_contains_whitespaces` function. If you have, it will not work.
3. Next, it will call the `process_all_repositories()` function, which will loop through the `DEFAULT_REPOSITORIES` dictionary and call the `process_repository(repository_name)` function for each repository name.
4. In this step, the `process_repository` function will call the `verify_ck_metrics_folder(repository_name)` function imported from `code_metrics.py`, as the code must verify if you have already executed the `code_metrics.py` file. If they aren't, it will tell you to run the `code_metrics.py` file, which will generate the ck metrics. This verification is done by:
   1. Verifying if the repository commit hash csv file exists inside the `CK_METRICS_DIRECTORY_PATH` directory, which should be named as `repository_name-commits_list.csv`, for example: `commons-lang-commits_list.csv`. If it doesn't exist, it will return false;  
   2. If the csv file exists, it will, for every commit hash, which is inside the `commit hash` column in the csv file, verify if there is a subdirectory inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, which should be named as the value in the current `commit_hash` and contains all the ck metrics generated files, which are defined in the `CK_METRICS_FILES` constant. If it doesn't exist, it will return false;

   If those verifications are all true, the function exists, due to the fact that the ck metrics are already calculated.
5. Now it will call the `create_directories` to create the `RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH` output directory, which will be, later on, be used to store the `metrics evolution`, `metrics_predictions` and`metrics statistics`.
6. With the output directories created, we get into the most important step, in which the `traverse_directory` will be executed. This function will get the path of every subfolder inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, where each subfolder should contain the `class.csv` and `method.csv` files, For each subfolder path, it calls the `process_csv_file` function, giving it the csv `file_path` string and `metrics_track_record` dictionary. With that in mind, the `process_csv_file` does the following:
   1. It will open file and get the values of the desired columns, them being the `class`, the variable attribute, which could be the `type` or the `method` values, depending if it is the classes or methods to be processed. Also, it gets the values in the `cbo`, `wmc` and `rfc` values, which are metrics generated by ck. For that four metrics, it creates a tuple to store them and create a identifier, being the combination of the `class_name` and the `variable attribute`;  
   2. Now, it verifies if that identifier is not already in the `metrics_track_record` dictionary. If not, in the `identifier` position of the dictionary, it starts two fields, the `metrics` list and the `changed` value, in which stores the number of times that the tuple (containing the combination of the cbo, wmc and rfc) changes;  
   3. Now it gets the metrics values list in the identifier position of the dictionary and verify if the current metrics combination aren't inside that metrics values list. If it ain't, it means that those metrics combination haven't appeared yet, so we can add it to the list and increment the value of times that this class or method changed. If they are in, we won't add them to the list, as those values would be repeated;  
     
   Now that the `metrics_track_record` dictionary is filled with the metrics evolution of every class or method, the `traverse_directory` function will return the `metrics_track_record` dictionary, in order for the metrics be processed to generate statistics.
7. Now its time to write those `metrics_track_record` to the `metrics_evolution` folder with the call of the `write_metrics_track_record_to_csv` function. This function will, for each class or method in the repository, write it's values inside the `metrics_track_record` dictionary to the `{FULL_METRICS_EVOLUTION_DIRECTORY_PATH}/{repository_name}/{CLASSES_OR_METHODS}/{class_name}/{variable_attribute}{CSV_FILE_EXTENSION}` csv file and call the `linear_regression_graphics(metrics, class_name, variable_attribute, repository_name)` function to generate the linear regression graphics that same class or method. Inside the `linear_regression_graphics` function, it calls the `verify_substantial_metric_decrease` function for the specified metric name in the `SUBSTANTIAL_CHANGE_METRIC` constant, which will verify if the current metrics values of the current class or method had a substantial decrease, defined in the `DESIRED_DECREASED` constant. There are restrictions, for example, keywords that might be found in the class name or variable attributeIf it had any decrease equal or higher than the `DESIRED_DECREASED`, it will add the `class_name`, `variable_attribute`, `metric[i - 1]`, `metric[i]`, `percentual_variation`, `commit number` and `commit hash` to a csv file stored in the `{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME}` file.  
8. Now that we have the record of the times the metrics changed and it's values for every class or method, the main function calls the `generate_metrics_track_record_statistics(repository_name, metrics_track_record)`, which will generate the metrics statistics (`Minimum`, `Maximum`, `Average` and `Third Quartile`) for every metric (`cbo`, `wmc` and `rfc`), which allow us to have a better understanding of the metrics behavior over time. Those statistics will be stored in the `METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "-" + CHANGED_METHODS_CSV_FILENAME` file.
9. In this step, with those statistics generated and stored in the `METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "-" + CHANGED_METHODS_CSV_FILENAME` csv file, the main funcion call the `sort_csv_by_changes(repository_name)` function that is going to sort the lines of the metrics statistics csv file by the `Changed` column, which is the number of times the metrics changed. The top changes will be stored in the `METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "-" + SORTED_CHANGED_METHODS_CSV_FILENAME` csv file.  
10. Now, that we have the sorted csv file, the main function will call the `os.remove` to delete the old, unsorted csv file.
11. Finally, the main function will call the `sort_csv_by_percentual_variation(repository_name)` function to sort the substantial changes csv file named as `{FULL_METRICS_STATISTICS_DIRECTORY_PATH}/{repository_name}/{SUBSTANTIAL_CHANGES_FILENAME}` by the `Percentual Variation` column, which is the percentual variation of the metrics values.  
12. After all the processing is done, the `metrics_changes.py` script will output the elapsed execution time and play a sound to notify you that the script has finished.

### Auxiliar Scripts:
There are also some auxiliar scripts, which are stored in the `Scripts/` folder, which are this ones:

#### Empty Folders
This script is used to verify if there are empty folders inside a specified directory. It is really usefull to make sure your files where processed or extracted correctly. 
To run this code as you want, you must modify the following constants:
1. `VERBOSE`: If you want to see the progress bar and the print statements, you must set the `VERBOSE` constant to `True`. If not, then a more clean output will be shown, with only the progress bar of the script execution, which is the default value of the `VERBOSE` constant.

Now that you have set the constants, you can run the following command to execute the following command:
```
make empty_folders_script
```

#### Extract Zip Files
 This script is used to extract the zip files of the repositories. It is really usefull as i didn't want to reprocess the files, so i just packed them in zip files using the `generateZipFiles.sh`. To execute it, you must run the following command:
```
make extract_zip_files_script
```

#### Generate Zip Files
This script is used to generate the zip files of the repositories. As mentioned in the script above, tt is really usefull as i didn't want to reprocess the files, so i just packed them in zip files using this script. To execute it, you must run the following command:
```
make generate_zip_files_script
```

#### Move Extracted Files
This is a really simple script, which is used to run after you execute the `extractZipFiles.sh` script, as it will move the extracted files to the right directory, for example, the extracted `/kafka/ck_metrics` will be placed in `/ck_metrics/kafka`. To execute it, you must run the following command:
```
make move_extracted_files_script
```

#### Track Files:
This script searches for files in the `PyDriller/diffs/` folder for any file defined in `TARGET_FILENAMES` constant for the repositories specified in the `REPOSITORIES` constant and write the list of found files to a txt file in `/PyDriller/metrics_data/repository_name/track_files_list.txt`. To execute it, you must run the following command:
```
make track_files_script
```

## Dependencies:
This project depends on the following libraries:
- [PyDriller](https://pydriller.readthedocs.io/en/latest/) -> PyDriller is the core of this project, as it is used to traverse the commits tree of the repositories and get many informations about it, like the commit hash, commit message, commit date and many other things.
- [MatPlotLib](https://matplotlib.org/) -> MatPlotLib is used to generate the graphics of the metrics evolution and the linear prediction.
- [NumPy](https://numpy.org/) -> NumPy is used to generate the linear prediction of the linear regression and to many operations in the list of the metrics.
- [Pandas](https://pandas.pydata.org/) -> Pandas is used maintly to read and write the csv files.
- [SciKit-Learn](https://scikit-learn.org/stable/) -> SciKit-Learn is used to generate the linear prediction of the linear regression.
- [TQDM](https://tqdm.github.io/) -> TQDM is used to show the progress bar of the scripts.

## Contributing:
Feel free to contribute to this project, as it is open source and i'll be glad to accept your pull request.  
If you have any questions, feel free to contact me at any of my Social Networks in my [GitHub Profile](https://github.com/BrenoFariasdaSilva).

## License:
This project is licensed under the [Creative Commons Zero v1.0 Universal](../LICENSE) License. So, for those who want to use this project for study, commercial use or any other thing, feel free to use it, as you want, as long as you don't claim that you made this project and remember to give the credits to the original creator.