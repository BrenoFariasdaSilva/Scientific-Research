# [PyDriller](https://github.com/BrenoFariasdaSilva/Scientific-Research/tree/main/PyDriller)
### ToDo: Create complete README.md
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
3. Then it will get the repository name, create a folder with that name and clone the repository in that folder.
