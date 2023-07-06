# [PyDriller](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/PyDriller)
@TODO: Update README to explain the new features (specific_files_statistics.py, top_changes.py).   
@TODO: Create a new file (metrics.py) that will store the metrics evolution of the given method or class.  
@TODO: Add the commit hash for the main.py code, where it generates the metrics evolution of the given method or class, so we can have the commit hash for every metric change.  
@TODO: Generate the graphics metrics evolution comparison for specified commit hashes.  
@TODO: Create classes for the constants, functions and variables that are used in multiple files. be careful that some constants might include '/' or not. So, make sure you use the correct one.  
@TODO: Update the main.py main function. It is very big and kinda messy.   
@TODO: FEAT top_changes.py -> Line 70 call "validate_class_name" which will see if the class_name has a package (which means, if it has dots .), if it does not, get the file column and get the substring starting from "org" to the end, then replace the "/" for ".".  
@TODO: Create new code that, for a specified name of the class or method and the values of the cbo, cboModified, rfc and wmc, it will get the commit hash of the commit that introduced the change.

### Important Note: Make sure you don't have whitespaces in the path of the project, otherwise it will not work.

## Installation
You need to install python3.  
```
sudo apt install python3 -y
```
	
### Requirements
Run the following command to install the requirements, like ```matplotlib```, ```numpy```, ```pandas```, ```pydriller``` and ```tqdm```:  
```
make dependencies
```
	
## How to use  
Run the following command to execute the `main.py` file:
```
make
```
1. The first thing it will do is check if you don't have whitespaces in the path of the project, if you have, it will not work.  
2. Then it will ask you to enter the url of the repository you want to analyze, for example: ```https://github.com/apache/commons-lang```.
3. Then it will get the repository name, and create the following folders: ```ck_metrics```, ```metrics_evolution/```, ```metrics_statistics/``` and, lastly, a subfolder inside the ```ck_metrics/``` folder with the name of the repository, in order to store the ck metrics of the repository that ck will generate. 
4. Now, if the `check_metrics_folders` function notes that the ck output are not where it should, it will assume that ck never ran inside the repository you specified, it will run it. In order to to run the ck, it will clone the repository, check the number of commits in the repository in order for PyDriller to traverse commits tree, storing the commit hashes in a .txt file, so we can do a git branch checkout to run ck for every commit hash in the repository. Keep in mind that the execution of the ck tool will take a while, depending on the number of commits of the repository. Commons-lang, for example, has like 8000 commits, so it will take more than an hour to finish.
5. Now, the `search_method_metrics` function will be executed. This function will open the csv files in the ck_metrics and extract the `cbo`, `wmc`, `cboModified`, `rfc` of each occurrence of the specified method to be evaluated. Then, it will store the results inside the `metrics_evolution/methodName.csv` file.
6. Now that every occurrence of the specified method metrics have been compiled into the `metrics_evolution/methodName.csv` file, the function `calculate_statistics` is executed, in which will extract the `minimum`, `maximum`, `average` and `third quartile` of each metric (`cbo, wmc, cboModified and rfc`). It will also create a csv file with the metrics statistics of the repository inside the `metrics_statistics/repositoryName.csv` file.

Run the following command to execute the `top_changes.py` file:
```
make top_changes
```
1. The first thing it will do is check if you don't have whitespaces in the path of the project, if you have, it will not work.

Run the following command to execute the `specific_files_statistics.py` file:
```
make specific_files_statistics
```
1. The first thing the code will do it ask you if you want to process a class or a method, if you want to process a class, type ```True```, if you want to process a method, type ```False```. Note that it is case sensitive, so make sure you type it correctly.
2. Now, it will run the `path_contains_whitespaces` function, which will do is check if you don't have whitespaces in the path of the project, if you have, it will not work, so it will stop the execution.
3. In this step, the function `get_repository_name_user` will be executed and it will ask you for the repository name, for example ```commons-lang``` or ```jabref```. If you just press enter, it will get the repository name from the ```DEFAULT_REPOSITORY_NAME``` constant inside the ```specific_files_statistics.py``` file.
4. After that, it will call the `check_metrics_folders(repository_name)` function, which will check if the metrics are already calculated by opening the commit hashes file that is stored inside the `ck_metrics/REPOSITORY_NAME/commit_hashes-REPOSITORY_NAME` and checking if every commit hash in the file is a folder in the repository folder.
5. Now, it will call `create_directory(full_directory_path, relative_directory_path)` function, which will create the following folders: ```metrics_evolution/``` and ```metrics_statistics/``` folders, if they don't exist.
6. With the folders created, it will run the `get_user_ids_input` which will ask you for the user the name(s) of class(es) or method(s) you want to analyze. For example: 
   1. If you had chosen to analyse a class, you would type the name of a class that is inside the `/metrics_statistics/REPOSITORY_NAME-sorted_top_changed_class.csv` in the column named `Class` (example: org.apache.commons.lang.StringUtils class), but only type, then it will ask for the type of the class located in the `type` column of the previous file (which could be `class`, `innerclass`, `interface`, and `anonymous`).
   2. If you had chosen to analyse a method, you would type the name of a method that is inside the `/metrics_statistics/REPOSITORY_NAME-sorted_top_changed_method.csv` (example: testBothArgsNull/0), then it will ask for the class in which that method is located in the `Method` column but is the (example: org.apache.commons.lang3.AnnotationUtilsTest).