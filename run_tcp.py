"""
Script de controle de relés com integração a calendário via API.

Este script realiza as seguintes operações:
  - Inicializa um cliente Modbus TCP para comunicação com o dispositivo.
  - Inicializa um controlador de relés a partir do cliente Modbus.
  - Obtém as URLs para verificar o status de eventos para cada relé a partir do arquivo .env.
  - Em um loop infinito, conecta ao dispositivo, consulta as APIs para determinar se há
    um evento ativo e, com base na resposta, liga ou desliga os relés.
  - Após cada verificação, a conexão é fechada e o script aguarda 30 segundos antes da próxima
    iteração.

Requisitos:
  - As variáveis de ambiente RELAY_1_STATUS_URL e RELAY_2_STATUS_URL devem estar definidas no .env.
  - O dispositivo Modbus deve estar acessível no endereço configurado.
  - Os módulos necessários (p.ex.: relay_modbus_controller, calendar_integration, logger) 
  devem estar corretamente instalados e configurados.
"""

import os
from time import sleep
from dotenv import load_dotenv

# Importa o cliente Modbus Serial, o controlador de relés e a função de verificação de eventos.
from relay_modbus_controller.modbus_tcp_client import ModbusClient
from relay_modbus_controller.relay_controller import RelayController
from calendar_integration.get_events import has_event
from logger import logger

# Carrega as variáveis de ambiente a partir do arquivo .env
load_dotenv()

# Obtém as URLs para consulta do status dos eventos para cada relé
relay_1_status_url = os.getenv("RELAY_1_STATUS_URL")
relay_2_status_url = os.getenv("RELAY_2_STATUS_URL")

def main():
    """
    Função principal para o controle dos relés.

    Esta função inicializa o cliente Modbus e o controlador de relés, obtém os estados iniciais
    dos relés e, em um loop infinito, realiza as seguintes ações:
      - Tenta conectar ao dispositivo Modbus.
      - Consulta a API para verificar se há eventos ativos para cada relé.
      - Atualiza o estado dos relés conforme o resultado da consulta.
      - Registra as alterações de estado através do logger.
      - Fecha a conexão Modbus e aguarda 30 segundos antes de repetir o processo.
    
    O loop pode ser interrompido pelo usuário (Ctrl+C), e a conexão Modbus será 
    fechada corretamente.
    """
    # Inicializa o cliente Modbus para comunicação TCP
    client = ModbusClient("192.168.0.7", port=502)

    # Inicializa o controlador de relés
    relay_controller = RelayController(client, 1)

    # Obtém e armazena os estados iniciais dos relés 1 e 2
    relay_1_status = relay_controller.read_relay_state(1)
    relay_2_status = relay_controller.read_relay_state(2)

    try:
        while True:
            # Tenta conectar ao dispositivo Modbus; se falhar, aguarda 5 segundos e tenta novamente
            if not client.connect():
                logger.error("Erro ao conectar ao Modbus.")
                sleep(5)
                continue

            # Verifica se há evento ativo para o relé 1 e atualiza seu estado
            status_relay1 = relay_controller.set_relay_status(has_event(relay_1_status_url), 1)
            if status_relay1 != relay_1_status:
                relay_1_status = status_relay1
                logger.info("Estado do Relé 1: %s", 'Ligado' if relay_2_status else 'Desligado')

            # Verifica se há evento ativo para o relé 2 e atualiza seu estado
            status_relay2 = relay_controller.set_relay_status(has_event(relay_2_status_url), 2)
            if status_relay2 != relay_2_status:
                relay_2_status = status_relay2
                logger.info("Estado do Relé 2: %s", 'Ligado' if relay_2_status else 'Desligado')

            # Fecha a conexão com o dispositivo Modbus
            client.close()

            # Aguarda 30 segundos antes da próxima verificação
            sleep(30)
    except KeyboardInterrupt:
        # Interrompe o loop caso o usuário pressione Ctrl+C
        logger.info("Interrupção pelo usuário. Encerrando o script.")
    finally:
        # Assegura que a conexão Modbus seja fechada ao sair do loop
        client.close()

if __name__ == "__main__":
    main()
