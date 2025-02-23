"""
Classe cliente ModBus Serial.

Esta classe fornece uma interface para comunicação com dispositivos ModBus via RS-485/RS-232,
permitindo leitura e escrita de bobinas (coils) e conexão/desconexão do servidor ModBus.

Exemplo de uso:

from pymodbus.client import ModbusSerialClient
modbus_client = ModbusClient(port='/dev/ttyUSB0', baudrate=9600)
modbus_client.connect()
status = modbus_client.read_relay_status(1)
modbus_client.write_coil(1, True)
modbus_client.close()
"""

from pymodbus.client import ModbusSerialClient

class ModbusClient:
    """
    Classe cliente ModBus Serial.

    Esta classe permite estabelecer uma conexão com um servidor ModBus RTU,
    ler o status de relés e escrever valores em bobinas específicas.
    """

    def __init__(self, port, baudrate=9600, stopbits=1, parity='N', bytesize=8, timeout=1):
        """
        Inicializa o cliente ModBus Serial.

        :param port: Porta serial utilizada para comunicação (ex: '/dev/ttyUSB0' ou 'COM3').
        :param baudrate: Taxa de transmissão em bits por segundo (padrão: 9600).
        :param stopbits: Número de bits de parada (padrão: 1).
        :param parity: Paridade ('N' para nenhuma, 'E' para par, 'O' para ímpar, padrão: 'N').
        :param bytesize: Número de bits por byte de dados (padrão: 8).
        :param timeout: Tempo limite para resposta do dispositivo (padrão: 1 segundo).
        """
        self.client = ModbusSerialClient(
            port=port,
            baudrate=baudrate,
            stopbits=stopbits,
            parity=parity,
            bytesize=bytesize,
            timeout=timeout
        )

    def connect(self):
        """
        Conecta ao servidor ModBus.
        
        :return: True se a conexão for bem-sucedida, False caso contrário.
        """
        return self.client.connect()

    def read_relay_status(self, relay_number, slave):
        """
        Lê o status de um relé específico.

        :param relay_number: Número do relé a ser lido (1 baseado).
        :param slave: ID do escravo ModBus.
        :return: Estado do relé (True para ligado, False para desligado).
        :raises Exception: Se houver erro na leitura do relé.
        """
        result = self.client.read_coils(0x0, 8, slave=slave)  # Lê 8 registros (bobinas)
        if result.isError():
            raise Exception(f"Erro ao ler o status do relé {relay_number}")
        return result.bits[relay_number-1]  # Retorna o valor lido

    def write_coil(self, address, value, slave):
        """
        Escreve um valor (True/False) em uma bobina específica.

        :param address: Endereço da bobina (1 baseado).
        :param slave: ID do escravo ModBus.
        :param value: Valor a ser escrito (True para ligar, False para desligar).
        :return: Resultado da operação de escrita.
        :raises Exception: Se houver erro ao escrever na bobina.
        """
        result = self.client.write_coil(address-1, value, slave=slave)
        if result.isError():
            raise Exception(f"Erro ao escrever o coil no endereço {address}")
        return result

    def close(self):
        """
        Fecha a conexão com o servidor ModBus.
        """
        self.client.close()
