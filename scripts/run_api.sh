#!/bin/bash

# Ativa o ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Carrega as variáveis do arquivo .env
if [ -f ".env" ]; then
    # Lê o arquivo .env e exporta as variáveis
    export $(cat .env | grep -v '^#' | xargs)
    
    # Verifica se API_HOST existe no .env
    if [ -z "$API_HOST" ]; then
        echo "Warning: API_HOST não encontrado no arquivo .env. Usando localhost como padrão."
        API_HOST="localhost"
    fi
    
    # Verifica se API_PORT existe no .env
    if [ -z "$API_PORT" ]; then
        echo "Warning: API_PORT não encontrado no arquivo .env. Usando 8000 como padrão."
        API_PORT="8000"
    fi
else
    echo "Warning: Arquivo .env não encontrado. Usando configurações padrão."
    API_HOST="localhost"
    API_PORT="8000"
fi

# Configura PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/.."

# Executa o projeto com as variáveis do .env
echo "Starting server on ${API_HOST}:${API_PORT}"
python -m uvicorn api.main:app --host $API_HOST --reload --port $API_PORT