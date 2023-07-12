# [PyDriller](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/PyDriller)
@TODO 1: Update README to explain all the features (ck_metrics.py, metrics_changes.py and generate_images.py).   
@TODO 2: Create classes for the constants, functions and variables that are used in multiple files. Be careful that might be some constants might include '/' or not. So, make sure you use the correct one. Save those classes in a new file called main.py.  
@TODO 3: Create code that generates the graphics metrics evolution comparison for specified commit hashes.  Use args.  
@TODO 4: Create new code that, for a specified name of the class or method and the values of the cbo, cboModified, rfc and wmc, it will return you the commit hash of the commit that introduced the changes value.    
@TODO 5: Remove most of the prints to make the code execution more clean. Remove most of the sucessfull prints, as they are not necessary. Keep only the error prints and final prints.  
@TODO 6: Change `ck_metrics.py` creation of the commit hash list file. Make it use a csv file and not a txt file. Also, add the following fields: `commit.msg`, `commit.committer_date`, and `commit.modified_files`.  
@TODO 7: Verify the folder creation of each python file. Metrics statistics seems to be creating the metrics_evolution folder, but not the metrics_statistics folder.  
@TODO 8: Make the `metrics_changes.py` file generated files to be differentiated from classes or methods by using subfolders, like, `repository_name/class/class_name/` or `repository_name/method/method_name/`.  

### Important Note: Make sure you don't have whitespaces in the path of the project, otherwise it will not work.

## Installation
You need to install python3. If you are using Linux, you (must likely) can install it by just running the following commands:
```
sudo apt install python3 -y
sudo apt install python3-pip -y
```
Great, you now have python3 and pip installed. Now, we need to install the project requirements/dependencies.

### Requirements
Run the following command to install the requirements, like ```matplotlib```, ```numpy```, ```pandas```, ```pydriller``` and ```tqdm```:  
```
make dependencies
```
	
## How to use  
First, you must run the following command to execute the `ck_metrics.py` file:
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
   2. Checkout to the `commit.hash` branch;  
   3. Create a subfolder inside the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name` with the name of the `commit.hash` value;  
   4. Lastly, with the call of the `run_ck_metrics_generator(cmd)` to execute the `cmd` command, which is a command defined to run ck for the current commit.hash and store the files that it generates in the `FULL_REPOSITORY_DIRECTORY_PATH/repository_name/commit.hash` folder;  
8. Now that we have the list of tuples containing the commit hashe, commit message and commit date for each commit, we must store those values in the `CK_METRICS_DIRECTORY_PATH/repository_name-commit_hashes.csv` file, with the call of `write_commit_hashes_to_csv` function.
9.  And lastly, we must call `checkout_branch` function passing the `main` branch as parameter, in order to return to the main branch of the repository.

Considering that you now have the ck metrics calculated, you are able to run the following command to execute the `top_changes.py` file:
```
make metrics_changes_script
```
1. The first thing it will do is ask you if you want to process classes or methods, if you want to process classes, type ```True```, if you want to process methods, type ```False```. Note that it is case sensitive, so make sure you type it correctly.
2. The second thing it will do is verify if you don't have whitespaces in the path of the project by calling the `path_contains_whitespaces` function. If you have, it will not work.
3. Then, the main function will call `get_directory_path`, which will ask you the repository name, for example: ```commons-lang```. If you simply press enter, it will get the first repository name from the ```DEFAULT_REPOSITORY_NAME``` constant inside the ```top_changes.py``` file.
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

Run the following command to execute the `specific_files_statistics.py` file:
```
make specific_files_statistics_script
``` 
1. The first thing the code will do it ask you if you want to process a class or a method, if you want to process a class, type ```True```, if you want to process a method, type ```False```. Note that it is case sensitive, so make sure you type it correctly.
2. Now, it will run the `path_contains_whitespaces` function, which will do is verify if you don't have whitespaces in the path of the project, if you have, it will not work, so it will stop the execution.
3. In this step, the function `get_repository_name_user` will be executed and it will ask you for the repository name, for example ```commons-lang``` or ```jabref```. If you just press enter, it will get the repository name from the ```DEFAULT_REPOSITORY_NAME``` constant inside the ```specific_files_statistics.py``` file.
4. After that, it will call the `check_metrics_folders(repository_name)` function, which will check if the metrics are already calculated by opening the commit hashes file that is stored inside the `ck_metrics/REPOSITORY_NAME/commit_hashes-REPOSITORY_NAME` and checking if every commit hash in the file is a folder in the repository folder.
5. Now, it will call `create_directory(full_directory_path, relative_directory_path)` function, which will create the following folders: ```metrics_evolution/``` and ```metrics_statistics/``` folders, if they don't exist.
6. With the folders created, it will run the `get_user_ids_input` which will ask you for the user the name(s) of class(es) or method(s) you want to analyze. For example: 
   1. If you had chosen to analyse a class, you would type the name of a class that is inside the `/metrics_statistics/REPOSITORY_NAME-sorted_top_changed_class.csv` in the column named `Class` (example: org.apache.commons.lang.StringUtils class), but only type, then it will ask for the type of the class located in the `type` column of the previous file (which could be `class`, `innerclass`, `interface`, and `anonymous`).
   2. If you had chosen to analyse a method, you would type the name of a method that is inside the `/metrics_statistics/REPOSITORY_NAME-sorted_top_changed_method.csv` (example: testBothArgsNull/0), then it will ask for the class in which that method is located in the `Method` column but is the (example: org.apache.commons.lang3.AnnotationUtilsTest).