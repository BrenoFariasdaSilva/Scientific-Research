<div align="center">

# [PyDriller.](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/PyDriller)  <img src="https://github.com/devicons/devicon/blob/master/icons/python/python-original.svg"  width="3%" height="3%">

</div>

TODO: Verify why the things of not repeating the metrics values in the metrics_track_record dictionary in the metrics_changes.py script, cause it might be making a problem that we have less metrics evolution than the number of commits of that file?  Lines 243 and 244

TODO: Clean the metrics_changes.py outputs. Add progress bar and make it as clean as possible.  

TODO: Update the README.md file about what the scripts do after the new changes. 

<div align="center">
  
---

Welcome to the PyDriller folder, in which you will find the scripts used to generate the ck metrics, metrics changes, metrics evolution, metrics linear predictions, graphics and commit files diff of the repositories of interest.

---

</div>

- [PyDriller.  ](#pydriller--)
    - [Important Notes:](#important-notes)
  - [Installation:](#installation)
    - [Requirements:](#requirements)
  - [How to use:](#how-to-use)
    - [Main Scripts:](#main-scripts)
      - [CK\_Metrics](#ck_metrics)
      - [Metrics\_Changes](#metrics_changes)
    - [Auxiliar Scripts:](#auxiliar-scripts)
      - [Empty Folders](#empty-folders)
      - [Extract Zip Files](#extract-zip-files)
      - [Generate Zip Files](#generate-zip-files)
      - [Move Extracted Files](#move-extracted-files)
  - [Dependencies:](#dependencies)
  - [Contributing:](#contributing)
  - [License:](#license)


### Important Notes:
- Make sure you don't have whitespaces in the path of the project, otherwise it will not work.
- The execution of this scripts will take a long time and store a lot of data, so make sure you have enough space in your disk and be patient. Example: Running all the scrips only for `Apache Kafka` generates a total of 115 GB.
- Why is it not parallelized? Because, for example, the first script (ck_metrics.py), which is the one who takes the most time to execute (could be days easily depending on the size of the repository of interest), the result of the iteration x depends on the result since the first iteration until x-1, so it is not possible to parallelize it. The other scripts, for example, actually could have some room for parallelization, but as all those scripts depends on file reading and writing (which generates a race condition), so I decided to not parallelize it. If you want to parallelize it, feel free to do it, i'll be glad aproving your pull request.

## Installation:
You need to install python3. If you are using Linux, you (must likely) can install it by just running the following commands:
```
sudo apt install python3 -y
sudo apt install python3-pip -y
```
Great, you now have python3 and pip installed. Now, we need to install the project requirements/dependencies.

### Requirements:
Run the following command to install the requirements, like ```matplotlib```, ```numpy```, ```pandas```, ```pydriller``` and ```tqdm```:  
```
make dependencies
```
	
## How to use: 
### Main Scripts:
First, you must run the following command to execute the `ck_metrics.py` file:
#### CK_Metrics
```
make ck_metrics_script
```
1. As for every file in this project, the first thing it will do is verify if you don't have whitespaces in the path of the project, if you have, it will not work.  
2. Then it will ask you to enter the url of the repository you want to analyze, for example: ```https://github.com/apache/commons-lang```. If you simply press enter, it will get the first url from the ```DEFAULT_REPOSITORY_URL``` constant inside the ```ck_metrics.py``` file.
3. Then it will get the repository name from the url you entered, for example: ```commons-lang```.
4. Now, the `verify_ck_metrics_folder` function  will verify if the ck metrics are already calculated. That verification is done by:
   1. Verifying if the repository commits list csv file exists inside the `CK_METRICS_DIRECTORY_PATH` directory, which should be named as `repository_name-commit_hashes.csv`, for example: `commons-lang-commit_hashes.csv`;
   2. If the csv file exists, it will, for every commit hash in the csv file, verify if there is a subdirectory inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, which should be named as `commit_hash` and contains all the ck metrics generated files, which are defined in the `CK_METRICS_FILES` constant;  
   
   If those verifications are all true, it stops executing, due to the fact that the ck metrics are already calculated. If not, it will continue executing.
5. Now, as the ck metrics are not calculated, it will call `create_directory` twice, one for the `FULL_CK_METRICS_DIRECTORY_PATH` directory and another for the `FULL_REPOSITORY_DIRECTORY_PATH` directory.
6. With all the subfolders created, we must call `clone_repository` function, which will clone the repository to the `FULL_REPOSITORY_DIRECTORY_PATH` directory.
7. As now we have the repository cloned, we must call `traverse_repository` function, in which will loop through the repository commits tree with the use of `PyDriller.traverse_commits()` to go through all the commit hashes of the repository and do the following for each commit in the repository: 
   1. Get the tuple containing the `commit.hash`, `commit.msg` and `commit.author_date` and store these commit data in the `commit_hashes` list, in order to, later on, store them inside the `CK_METRICS_DIRECTORY_PATH/repository_name-commit_hashes.csv` file;  
   2. Call `generate_diffs(repository_name, commit_hash, commit_number)`, which will fo through all the modified files of the current commit and store the diffs of the files in the `{cwd}{DEFAULT_DIFFS_DIRECTORY}/{repository_name}/{commit_number}-{commit_hash.hash}/{modified_file.filename}{DIFF_FILE_EXTENSION}` folder;
   3. Checkout to the `commit.hash` branch;  
   4. Create a subfolder inside the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name` with the name of the `commit.hash` value;  
   5. Lastly, with the call of the `run_ck_metrics_generator(cmd)` to execute the `cmd` command, which is a command defined to run ck for the current commit.hash and store the files that it generates in the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name/commit.hash` folder;  
8. Now that we have the list of tuples containing the commit hashe, commit message and commit date for each commit, we must store those values in the `CK_METRICS_DIRECTORY_PATH/repository_name-commit_hashes.csv` file, with the call of `write_commit_hashes_to_csv` function.
9.  And lastly, we must call `checkout_branch` function passing the `main` branch as parameter, in order to return to the main branch of the repository.
10. After everything is done, the `ck_metrics.py` script will be done and play a sound to notify you that it is done.

#### Metrics_Changes
Considering that you now have the ck metrics calculated, you are able to run the following command to execute the `metrics_changes.py` file:
```
make metrics_changes_script
```
1. The first thing it will do is ask you if you want to process classes or methods, if you want to process classes, type ```True```, if you want to process methods, type ```False```. Note that it is case sensitive, so make sure you type it correctly.
2. The second thing it will do is verify if you don't have whitespaces in the path of the project by calling the `path_contains_whitespaces` function. If you have, it will not work.
3. Then, the main function will call `get_directory_path`, which will ask you the repository name, for example: ```commons-lang```. If you simply press enter, it will get the first repository name from the ```DEFAULT_REPOSITORY_NAME``` constant list inside the ```metrics_changes.py``` file.
4. Now, it calls `verify_ck_metrics_folders` function, as the code must verify if you have already executed the `ck_metrics.py` file. If they aren't, it will tell you to run the `ck_metrics.py` file, which will generate the ck metrics. This verification is done by:
   1. Verifying if the repository commit hash csv file exists inside the `CK_METRICS_DIRECTORY_PATH` directory, which should be named as `repository_name-commit_hashes.csv`, for example: `commons-lang-commit_hashes.csv`. If it doesn't exist, it will return false;  
   2. If the csv file exists, it will, for every commit hash, which is inside the `commit hash`column in the csv file, verify if there is a subdirectory inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, which should be named as the value in the current `commit_hash` and contains all the ck metrics generated files, which are defined in the `CK_METRICS_FILES` constant. If it doesn't exist, it will return false;

   If those verifications are all true, the function exists, due to the fact that the ck metrics are already calculated.
5. Now it will call the `create_directory`to create the `RELATIVE_METRICS_STATISTICS_DIRECTORY_PATH` output directory, which will be, later on, be used to store the top changes csv file(s).
6. With the output directory created, we get into the most important step, in which the `traverse_directory` will be executed. This function will get the path of every subfolder inside the `CK_METRICS_DIRECTORY_PATH/repository_name` directory, where each subfolder should contain the `class.csv` and `method.csv` files, For each subfolder path, it calls the `process_csv_file` function, giving it the csv `file_path` string and `metrics_track_record` dictionary. With that in mind, the `process_csv_file` does the following:
   1. It will open file and get the values of the desired columns, them being the `class`, the variable attribute, which could be the `type` or the `method` values, depending if it is the classes or methods to be processed. Also, it gets the values in the `cbo`, `cboModified`, `wmc` and `rfc` values, which are metrics generated by ck. For that four metrics, it creates a tuple to store them and create a identifier, being the combination of the `class_name` and the `variable attribute`;  
   2. Now, it verifies if that identifier is not already in the `metrics_track_record` dictionary. If not, in the `identifier` position of the dictionary, it starts two fields, the `metrics` list and the `changed` value, in which stores the number of times that the tuple (containing the combination of the cbo, cboModified, wmc and rfc) changes;  
   3. Now it gets the metrics values list in the identifier position of the dictionary and verify if the current metrics combination aren't inside that metrics values list. If it ain't, it means that those metrics combination haven't appeared yet, so we can add it to the list and increment the value of times that this class or method changed. If they are in, we won't add them to the list, as those values would be repeated;  
     
   Now that the `metrics_track_record` dictionary is filled with the metrics evolution of every class or method, the `traverse_directory` function will return the `metrics_track_record` dictionary, in order for the metrics be processed to generate statistics.
1. Now its time to write those `metrics_track_record`to the `metrics_evolution`folder with the call of the `write_metrics_track_record_to_csv` function, which will write the `metrics_track_record` dictionary to the `FULL_METRICS_EVOLUTION_DIRECTORY_PATH + "/" + repository_name + "/" + CLASSES_OR_METHODS + "/" + class_name + "-" + variable_attribute + CSV_FILE_EXTENSION` csv file.
2. Now that we have the record of the times the metrics changed and it's values for every class or method, the main function calls the `process_metrics_track_record(repository_name, metrics_track_record)`, which will generate the metrics statistics (`Minimum`, `Maximum`, `Average` and `Third Quartile`) for every metric (`cbo`, `cboModified`, `wmc` and `rfc`), which allow us to have a better understanding of the metrics behavior over time. Those statistics will be stored in the `METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "-" + CHANGED_METHODS_CSV_FILENAME` file.
3. Finally, with those statistics generated and stored in the `METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "-" + CHANGED_METHODS_CSV_FILENAME` csv file, the main funcion call the `sort_csv_by_changes(repository_name)` function that is going to sort the lines of the metrics statistics csv file by the `Changed` column, which is the number of times the metrics changed. The top changes will be stored in the `METRICS_STATISTICS_DIRECTORY_PATH + "/" + repository_name + "-" + SORTED_CHANGED_METHODS_CSV_FILENAME` csv file.  
4. Now, that we have the sorted csv file, the main function will call the `os.remove` to delete the old, unsorted csv file.
5. After everything is done, the `metrics_changes.py` script will be done and play a sound to notify you that it is done.

### Auxiliar Scripts:
There are also some auxiliar scripts, which are stored in the `Scripts/` folder, which are this ones:

#### Empty Folders
This script is used to verify if there are empty folders inside a specified directory. It is really usefull to make sure your files where processed or extracted correctly. To execute it, you must run the following command:
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