"""
Classe para controle de relés via Modbus.

Esta classe permite controlar relés utilizando comunicação Modbus RTU (serial) 
ou Modbus TCP.

Exemplos de uso:

# Criando um cliente Modbus RTU e controlando um relé:
from relay_modbus_controller.modbus_serial_client import ModbusClient as ModbusClientSerial
modbus_client = ModbusClientSerial(port='/dev/ttyUSB0', baudrate=9600)
relay_controller = RelayController(modbus_client, slave=1)
relay_controller.set_relay_status(True, 1)  # Liga o relé no endereço 1

# Criando um cliente Modbus TCP e controlando um relé:
from relay_modbus_controller.modbus_tcp_client import ModbusClient as ModbusClientTCP
modbus_client = ModbusClientTCP(host='192.168.1.100', port=502)
relay_controller = RelayController(modbus_client, slave=1)
relay_controller.set_relay_status(False, 1)  # Desliga o relé no endereço 1
"""
class RelayController:
    """
    Classe para controle de relés via Modbus.

    Esta classe fornece métodos para ligar, desligar e ler o estado de um relé
    através de um cliente Modbus, que pode ser serial (RTU) ou TCP/IP.
    """

    def __init__(self, modbus_client, slave):
        """
        Inicializa o controlador de relés.

        :param modbus_client: Instância de um cliente Modbus (RTU ou TCP).
        :param slave: ID do escravo Modbus.
        """
        self.modbus_client = modbus_client
        self.slave = slave

    def set_relay_status(self, relay_status, relay_address):
        """
        Define o estado do relé especificado.

        :param relay_status: Estado desejado para o relé (True para ligado, False para desligado).
        :param relay_address: Endereço do relé no barramento Modbus.
        :return: Estado atualizado do relé após a operação.
        """
        current_relay_state = self.read_relay_state(relay_address)
        if relay_status and not current_relay_state:
            self.turn_on_relay(relay_address)
        elif not relay_status and current_relay_state:
            self.turn_off_relay(relay_address)
        return self.read_relay_state(relay_address)

    def turn_on_relay(self, relay_address):
        """
        Liga o relé no endereço especificado.

        :param relay_address: Endereço do relé no barramento Modbus.
        :return: Estado atualizado do relé após a operação.
        """
        self.modbus_client.write_coil(relay_address, True, self.slave)
        return self.read_relay_state(relay_address)

    def turn_off_relay(self, relay_address):
        """
        Desliga o relé no endereço especificado.

        :param relay_address: Endereço do relé no barramento Modbus.
        :return: Estado atualizado do relé após a operação.
        """
        self.modbus_client.write_coil(relay_address, False, self.slave)
        return self.read_relay_state(relay_address)

    def read_relay_state(self, relay_address):
        """
        Lê o estado atual do relé no endereço especificado.

        :param relay_address: Endereço do relé no barramento Modbus.
        :return: Estado atual do relé (True para ligado, False para desligado).
        """
        return self.modbus_client.read_relay_status(relay_address, self.slave)
