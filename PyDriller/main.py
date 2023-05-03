import subprocess
from pydriller import Repository
# TODO: Criar o diretório antews
# TODO: Informar o último parâmetro o diretório de saída

for commit in Repository('commons-lang').traverse_commits():
    cmd = f"java -jar ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar {commit.project_path}"# Trocar o projectpath pelo SHA
    # Olhar como ele percorre a ´arvore dos commits
    # Variables and Metrics tentar desabilitar isso
    # Caminho do projet FALSE 0 FALSE directory
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()
    print(stdout.decode())
    