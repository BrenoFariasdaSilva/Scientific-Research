# [PyDriller](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/PyDriller)
***@TODO***: Make the code run for lots of methods names, and not just one. Do this by changing the methods input (get_user_method_input) and calling the search_method_metrics and calculate_statistics functions for each method name.
***@TODO***: Update the README.md file with the new changes and add use cases.

### Important Note: Make sure you doesn't have whitespaces in the path of the project, otherwise it will not work.

## Installation
You need to install python3.  
```
sudo apt install python3 -y
```
	
### Requirements
Run the following command to install the requirements, like ```pydriller``` and ```tqdm```:  
```
make setup
```
	
## How to use  
Run the following command to execute the project:
```
make
```
1. The first thing it will do is check if you don't have whitespaces in the path of the project, if you have, it will not work.  
2. Then it will ask you to enter the url of the repository you want to analyze, for example: ```https://github.com/apache/commons-lang```.
   If you just press enter, it will use the default repository url, which is stored in the ```DEFAULT_REPOSITORY_URL``` constant defined in the top of the ```main.py``` file. In that case, the default repository is commons-lang.
3. After that, it will ask you to type the method name you want to analyze, for example: ```isNullOrZero```. If you just press enter, it will use the default method name, which is stored in the ```DEFAULT_METHODS_NAME``` constant defined in the top of the ```main.py``` file. In that case, the default method name is `isNumericSpace`.
4. Then it will get the repository name, and create the following folders: ```ck_metrics```, ```metrics_evolution/```, ```metrics_statistics/``` and, lastly, a subfolder inside the ```ck_metrics/``` folder with the name of the repository, in order to store the ck metrics of the repository that ck will generate. 
5. Now, if the `check_metrics_folders` function notes that the ck output are not where it should, it will assume that ck never ran inside the repository you specified, it will run it. In order to to run the ck, it will clone the repository, check the number of commits in the repository in order for PyDriller to traverse commits tree, storing the commit hashes in a .txt file, so we can do a git branch checkout to run ck for every commit hash in the repository. Keep in mind that the execution of the ck tool will take a while, depending on the number of commits of the repository. Commons-lang, for example, has like 8000 commits, so it will take more than an hour to finish.
6. Now, the `search_method_metrics` function will be executed. This function will open the csv files in the ck_metrics and extract the `cbo`, `wmc`, `cboModified`, `rfc` of each occurrence of the specified method to be evaluated. Then, it will store the results inside the `metrics_evolution/methodName.csv` file.
7. Now that every occurrence of the specified method metrics have been compiled into the `metrics_evolution/methodName.csv` file, the function `calculate_statistics` is executed, in whicih will extract the `minimum`, `maximum`, `average` and `third quartile` of each metric (cbo, wmc, cboModified and rfc). It will also create a csv file with the metrics statistics of the repository inside the `metrics_statistics/repositoryName.csv` file.
