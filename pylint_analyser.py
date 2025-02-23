"""
Script para análise de código com Pylint.

Este script percorre os diretórios especificados e também a pasta onde o script está localizado,
executando o Pylint em todos os arquivos Python encontrados e exibindo os resultados na tela. 
Para otimizar a execução, o script utiliza paralelização através do ThreadPoolExecutor.
"""

import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_pylint(file_path: Path) -> None:
    """
    Executa o Pylint em um arquivo Python específico e exibe o resultado na tela.
    
    :param file_path: Caminho para o arquivo Python a ser verificado.
    """
    print(f"Verificando {file_path}")
    try:
        result = subprocess.run(
            ['pylint', '--py-version=3.12', str(file_path)],
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Exibe a saída do Pylint (stdout e stderr) se houver
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except Exception as e:
        print(f"Erro ao executar pylint em {file_path}: {e}")

def main():
    """
    Função principal que realiza as seguintes etapas:
      - Define os diretórios onde os arquivos Python serão verificados.
      - Coleta todos os arquivos com extensão '.py' de forma recursiva dos diretórios especificados,
        bem como os arquivos Python localizados na mesma pasta deste script.
      - Executa o Pylint em cada arquivo de forma paralela utilizando ThreadPoolExecutor.
    """
    # Lista de diretórios a serem verificados
    directories = ['calendar_integration', 'relay_modbus_controller']

    # Coleta todos os arquivos Python dos diretórios especificados
    python_files = []
    for directory in directories:
        python_files.extend(Path(directory).rglob('*.py'))

    # Adiciona todos os arquivos Python que estão na mesma pasta deste script
    current_dir = Path(__file__).parent
    python_files.extend(current_dir.glob('*.py'))

    # Executa as verificações em paralelo (ajuste o número de workers se necessário)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(run_pylint, file): file for file in python_files}
        for future in as_completed(futures):
            file = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"Erro na verificação do arquivo {file}: {e}")

if __name__ == '__main__':
    main()
