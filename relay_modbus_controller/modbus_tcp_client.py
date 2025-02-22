"""
Classe cliente ModBus TCP.

Esta classe fornece uma interface para comunicação com dispositivos ModBus via TCP/IP,
permitindo leitura e escrita de bobinas (coils) e conexão/desconexão do servidor ModBus.

Exemplo de uso:

from pymodbus.client import ModbusTcpClient
modbus_client = ModbusClient(host='192.168.1.100', port=502)
modbus_client.connect()
status = modbus_client.read_relay_status(1, slave=1)
modbus_client.write_coil(1, True, slave=1)
modbus_client.close()
"""

from pymodbus.client import ModbusTcpClient

class ModbusClient:
    """
    Classe cliente ModBus TCP.

    Esta classe permite estabelecer uma conexão com um servidor ModBus TCP,
    ler o status de relés e escrever valores em bobinas específicas.
    """

    # https://pymodbus.readthedocs.io/en/latest/source/client.html#pymodbus.client.ModbusTcpClient
    def __init__(self, host, port=502, timeout=1):
        """
        Inicializa o cliente ModBus TCP.

        :param host: Endereço IP do servidor ModBus.
        :param port: Porta do servidor ModBus (padrão: 502).
        :param timeout: Tempo limite para conexões (padrão: 1 segundo).
        """
        self.client = ModbusTcpClient(
            host=host,
            port=port,
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
        result = self.client.read_coils(0x0, 8, slave)  # Lê 8 registros (bobinas)
        if result.isError():
            raise Exception(f"Erro ao ler o status do relé {relay_number}")
        return result.bits[relay_number-1]  # Retorna o valor lido

    def write_coil(self, address, value, slave):
        """
        Escreve um valor (True/False) em uma bobina específica.

        :param address: Endereço da bobina (1 baseado).
        :param value: Valor a ser escrito (True para ligar, False para desligar).
        :param slave: ID do escravo ModBus.
        :return: Resultado da operação de escrita.
        :raises Exception: Se houver erro ao escrever na bobina.
        """
        result = self.client.write_coil(address-1, value, slave)
        if result.isError():
            raise Exception(f"Erro ao escrever o coil no endereço {address}")
        return result

    def close(self):
        """
        Fecha a conexão com o servidor ModBus.
        """
        self.client.close()
