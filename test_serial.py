"""
Script de teste para comunicação Modbus Serial.

Este script realiza os seguintes passos:
  - Inicializa um cliente Modbus Serial e um controlador de relés.
  - Em um loop contínuo, tenta conectar ao dispositivo Modbus.
  - Alterna o estado de um conjunto de relés (liga e desliga) sequencialmente,
    registrando os estados via logger.
  - Permite interrupção pelo usuário (Ctrl+C), garantindo o fechamento da conexão.

Requisitos:
  - O dispositivo Modbus deve estar conectado à porta configurada (por exemplo, 'COM3').
  - O logger deve estar configurado no arquivo 'logger.py'.
  - Os módulos 'ModbusClient' e 'RelayController' devem estar implementados corretamente
    no pacote 'relay_modbus_controller'.
"""

from time import sleep
from relay_modbus_controller.modbus_serial_client import ModbusClient
from relay_modbus_controller.relay_controller import RelayController
from logger import logger

def main():
    """
    Função principal que executa o teste de comunicação via Modbus Serial.

    O procedimento realizado é:
      1. Inicializar o cliente Modbus Serial utilizando a porta especificada (por exemplo, 'COM3').
      2. Criar o controlador de relés com o cliente Modbus, definindo o ID do escravo como 1.
      3. Em loop:
         - Tentar conectar ao dispositivo Modbus. Se a conexão falhar, 
         aguarda 5 segundos e tenta novamente.
         - Para cada relé de 1 a 4, liga o relé e registra o estado.
         - Para cada relé de 1 a 4, desliga o relé e registra o estado.
         - Aguardar 1 segundo antes de reiniciar o ciclo.
      4. Interromper a execução com Ctrl+C e fechar a conexão.
    """
    # Inicializa o cliente Modbus para comunicação serial (ex.: porta 'COM3')
    client = ModbusClient(port='COM3')

    # Inicializa o controlador de relés utilizando o cliente Modbus e define o ID do escravo como 1
    relay_controller = RelayController(client, 1)

    try:
        while True:
            # Tenta conectar ao dispositivo Modbus; se falhar, aguarda 5 segundos e tenta novamente
            while not client.connect():
                logger.error("Erro ao conectar ao Modbus.")
                sleep(5)

            # Liga sequencialmente os relés de 1 a 4 e registra o estado.
            # Obs.: A mensagem de log indica "Estado do Relé 1" para todos os relés,
            # mas a função está sendo chamada para cada relé (1 a 4).
            for i in range(1, 5):
                status_relay = relay_controller.set_relay_status(True, i)
                logger.info("Estado do Relé 1: %s", 'Ligado' if status_relay else 'Desligado')
                sleep(0.1)

            # Desliga sequencialmente os relés de 1 a 4 e registra o estado.
            for i in range(1, 5):
                status_relay = relay_controller.set_relay_status(False, i)
                logger.info("Estado do Relé 1: %s", 'Ligado' if status_relay else 'Desligado')
                sleep(0.1)

            # Aguarda 1 segundo antes de reiniciar o ciclo
            sleep(1)
    except KeyboardInterrupt:
        # Interrompe o loop caso o usuário pressione Ctrl+C
        logger.info("Interrupção pelo usuário. Encerrando o script.")
    finally:
        # Assegura que a conexão Modbus seja fechada ao sair do loop
        client.close()

if __name__ == "__main__":
    main()
