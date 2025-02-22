"""
Módulo para integração com eventos via API.

Este módulo contém funções para consultar uma API e verificar se há um evento
ocorrendo no momento.
"""

import requests
from logger import logger

def has_event(api_url: str) -> bool:
    """
    Verifica se há um evento atual consultando uma API.

    Esta função realiza uma requisição HTTP GET para a URL especificada e 
    interpreta a resposta JSON.
    Caso a resposta contenha a chave "hasEventNow", retorna seu valor; 
    caso contrário, retorna False.
    Se a requisição falhar (status diferente de 200), 
    registra um erro crítico e retorna False.

    :param api_url: URL da API que retorna informações sobre eventos.
    :return: True se houver um evento no momento (conforme indicado pela API), 
    False caso contrário.
    """
    # Adicionado timeout para evitar bloqueio indefinido na requisição
    response = requests.get(api_url, timeout=10)

    if response.status_code == 200:
        data = response.json()
        return data.get("hasEventNow", False)

    logger.critical("Erro ao acessar a API: %s", response.status_code)
    return False
