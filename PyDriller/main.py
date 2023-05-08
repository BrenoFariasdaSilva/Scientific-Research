import subprocess
from pydriller import Repository

# TODO: Criar o diretório antes
# TODO: Informar o último parâmetro o diretório de saída

# @brief: Main function
# @param: None
# @return: None
def main():
    for commit in Repository('commons-lang').traverse_commits():
        cmd = f"java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar {commit.project_path}" # TODO: Trocar o projectpath pelo SHA
        # TODO: Olhar como ele percorre a ´arvore dos commits
        # TODO: Variables and Metrics tentar desabilitar isso
        # TODO: Caminho do projet FALSE 0 FALSE directory
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        print(stdout.decode())
    
# @brief: This function is responsible for calling the main function at the start of the program
if __name__ == '__main__':
    main() 