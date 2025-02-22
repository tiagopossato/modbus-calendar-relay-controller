# Modbus Relay Controller with Calendar Integration

Este projeto controla relés de um dispositivo via Modbus (Serial e TCP) com base em eventos obtidos de uma API integrada à Agenda do Google. Em resumo, o sistema lê eventos em tempo real e liga ou desliga os relés conforme a presença de um evento na agenda.

## Recursos

- **Comunicação Modbus:**  
  - Suporte para Modbus Serial (RTU) e Modbus TCP.
  - Leitura e escrita de bobinas (coils) para controle de relés.

- **Integração com Calendário:**  
  - Consulta uma API para verificar se há um evento ativo. A documentação da API pode ser encontrada em [calendar_integration](./calendar_integration).
  - Atualiza o estado dos relés com base na resposta da API.

- **Configuração via Variáveis de Ambiente:**  
  - Utiliza um arquivo `.env` para armazenar URLs sensíveis e outras configurações.

- **Logging:**  
  - Registra erros críticos, alterações de estado e informações relevantes para monitoramento.

## Requisitos

- **Python:** 3.12 ou superior.
- **Bibliotecas Python:**
  - `pymodbus` - para comunicação Modbus.
  - `requests` - para realizar chamadas HTTP.
  - `pyserial` - para comunicação via porta serial.
  - `python-dotenv` - para carregar as variáveis do arquivo `.env`.
  - `pylint` - para verificação do código
- **Outros:**  
  - Um dispositivo Modbus (Serial ou TCP) configurado corretamente.
  - Um módulo de logging (arquivo `logger.py`), que deve ser configurado conforme as necessidades do projeto.

## Instalação

1. **Clone o repositório:**
```bash
git clone https://github.com/tiagopossato/modbus-calendar-relay-controller.git
cd modbus-calendar-relay-controller
```

2. **Crie e ative um ambiente virtual:**
```bash
python -m venv venv
# Linux/Mac
source venv/bin/activate
# Windows
venv\Scripts\activate
```

3. **Instale as dependências:**
```bash
pip install -r requirements.txt
```

4. **Configure as variáveis de ambiente:**

Crie um arquivo .env na raiz do projeto e defina as URLs de status dos relés:
```bash
RELAY_1_STATUS_URL=https://api.exemplo.com/relay1/status
RELAY_2_STATUS_URL=https://api.exemplo.com/relay2/status
```

# Estrutura do Projeto

    modbus-calendar-relay-controller/
    ├── calendar_integration/        # Integração com a API do calendário
    │   └── get_events.py            # Função para verificar eventos (has_event)
    ├── relay_modbus_controller/     # Módulos para comunicação Modbus e controle de relés
    │   ├── modbus_serial_client.py  # Cliente Modbus Serial
    │   ├── modbus_tcp_client.py     # Cliente Modbus TCP
    │   └── relay_controller.py      # Lógica de controle dos relés
    ├── logger.py                    # Configuração do logger
    ├── run_serial.py                # Script principal que executa o controle dos relés via Serial
    ├── run_tcp.py                   # Script principal que executa o controle dos relés via TCP
    ├── .env                         # Arquivo de variáveis de ambiente (não versionado)
    └── README.md                    # Este arquivo


# Uso

Execute o script principal para iniciar a monitorização dos eventos e controlar os relés:

```bash
python run_tcp.py
```
ou 

```bash
python run_serial.py
```

# Funcionamento

O script principal realiza as seguintes ações:

1. Inicialização:
    - Carrega as variáveis de ambiente do arquivo .env.
    - Inicializa o cliente Modbus (por exemplo, utilizando a porta 'COM3' para Modbus Serial).
    - Cria um controlador de relés utilizando o cliente Modbus.

2. Loop de Verificação:
    - Conecta ao dispositivo Modbus.
    - Consulta a API para cada relé (usando as URLs configuradas) para verificar se há um evento ativo.
    - Atualiza o estado dos relés conforme o resultado da consulta.
    - Registra as mudanças de estado e erros via logger.
    - Fecha a conexão e aguarda 30 segundos para a próxima verificação.

3. Encerramento:
    - O script pode ser interrompido com Ctrl+C, garantindo que a conexão Modbus seja fechada corretamente.

# Qualidade de Código e Linting

Para garantir a qualidade do código, utilize o pylint para verificar todos os arquivos Python. Um script de verificação `pylint-analyser.py` percorre os diretórios relevantes e executa o pylint em cada arquivo:
```bash
python pylint-analyser.py
```
Este script foi otimizado para rodar em paralelo e exibir os resultados na tela.

# Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests para melhorias, correções de bugs ou novas funcionalidades.

# Licença

Este projeto está licenciado sob a MIT License.
