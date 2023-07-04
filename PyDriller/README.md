# [PyDriller](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/PyDriller)
@TODO: Export the data of every commit in order to visualize it in a graph evolution of each metric.  
@TODO: Update README to explain the new features (top_changes.py).   
@TODO: Create a new file (metrics.py) that will store the metrics evolution of the given method or class.  
@TODO: Add the commit hash for the main.py code, where it generates the metrics evolution of the given method or class, so we can have the commit hash for every metric change.  
@TODO: Remove the main.py stuff related to the things that the specific_files_statistics.py does.

### Important Note: Make sure you don't have whitespaces in the path of the project, otherwise it will not work.

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
3. Then it will get the repository name, and create the following folders: ```ck_metrics```, ```metrics_evolution/```, ```metrics_statistics/``` and, lastly, a subfolder inside the ```ck_metrics/``` folder with the name of the repository, in order to store the ck metrics of the repository that ck will generate. 
4. Now, if the `check_metrics_folders` function notes that the ck output are not where it should, it will assume that ck never ran inside the repository you specified, it will run it. In order to to run the ck, it will clone the repository, check the number of commits in the repository in order for PyDriller to traverse commits tree, storing the commit hashes in a .txt file, so we can do a git branch checkout to run ck for every commit hash in the repository. Keep in mind that the execution of the ck tool will take a while, depending on the number of commits of the repository. Commons-lang, for example, has like 8000 commits, so it will take more than an hour to finish.
5. Now, the `search_method_metrics` function will be executed. This function will open the csv files in the ck_metrics and extract the `cbo`, `wmc`, `cboModified`, `rfc` of each occurrence of the specified method to be evaluated. Then, it will store the results inside the `metrics_evolution/methodName.csv` file.
6. Now that every occurrence of the specified method metrics have been compiled into the `metrics_evolution/methodName.csv` file, the function `calculate_statistics` is executed, in whicih will extract the `minimum`, `maximum`, `average` and `third quartile` of each metric (cbo, wmc, cboModified and rfc). It will also create a csv file with the metrics statistics of the repository inside the `metrics_statistics/reposotiryName.csv` file.
