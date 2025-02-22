import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

def run_pylint(file_path: Path) -> None:
    """
    Executa o pylint em um arquivo Python específico e exibe o resultado na tela.
    
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
        # Exibe a saída do pylint
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except Exception as e:
        print(f"Erro ao executar pylint em {file_path}: {e}")

def main():
    # Lista de diretórios a serem verificados
    directories = ['calendar_integration', 'relay_modbus_controller']
    
    # Coleta todos os arquivos .py dos diretórios especificados
    python_files = []
    for directory in directories:
        python_files.extend(Path(directory).rglob('*.py'))
    
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
