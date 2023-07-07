repositories_folder = repositories/
target_repository = commons-lang
target_repository_url = https://github.com/apache/commons-lang

all: clone_refactoring_miner install_refactoring_miner clone_target_repository execute_refactoring_miner

clone_refactoring_miner:
	git clone https://github.com/tsantalis/RefactoringMiner

install_refactoring_miner:
	cd RefactoringMiner && ./gradlew install

clone_target_repository:
	git clone $(target_repository_url) $(repositories_folder)$(target_repository)

execute_refactoring_miner:
	bin/RefactoringMiner -a $(repositories_folder)$(target_repository) main $(target_repository)-refactorings.json
	