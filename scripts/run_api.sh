#!/bin/bash

# Cores para melhor visualização
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para log de mensagens
log_message() {
    local level=$1
    local message=$2
    case $level in
        "INFO")
            echo -e "${GREEN}[INFO]${NC} $message"
            ;;
        "WARN")
            echo -e "${YELLOW}[WARN]${NC} $message"
            ;;
        "ERROR")
            echo -e "${RED}[ERROR]${NC} $message"
            ;;
    esac
}

# Verifica se o Python está instalado
if ! command -v python3 &> /dev/null; then
    log_message "ERROR" "Python 3 não está instalado."
    exit 1
fi

# Ativa o ambiente virtual se existir
if [ -d "venv" ]; then
    log_message "INFO" "Ativando ambiente virtual..."
    source venv/bin/activate
else
    log_message "WARN" "Ambiente virtual não encontrado."
fi

# Verifica se o uvicorn está instalado
if ! python3 -c "import uvicorn" &> /dev/null; then
    log_message "ERROR" "Uvicorn não está instalado. Execute: pip install uvicorn"
    exit 1
fi

# Configurações padrão
DEFAULT_HOST="127.0.0.1"
DEFAULT_PORT="8000"

# Carrega as variáveis do arquivo .env
if [ -f ".env" ]; then
    log_message "INFO" "Carregando configurações do arquivo .env..."
    # Lê o arquivo .env, ignora comentários e linhas vazias
    while IFS='=' read -r key value; do
        # Remove espaços em branco e aspas
        key=$(echo "$key" | tr -d '[:space:]' | tr -d '"' | tr -d "'")
        value=$(echo "$value" | tr -d '[:space:]' | tr -d '"' | tr -d "'")
        
        # Ignora linhas vazias e comentários
        if [ ! -z "$key" ] && [[ ! "$key" =~ ^#.* ]]; then
            export "$key=$value"
        fi
    done < .env
    
    # Verifica e configura o host
    if [ -z "$API_HOST" ]; then
        log_message "WARN" "API_HOST não encontrado no arquivo .env. Usando $DEFAULT_HOST como padrão."
        API_HOST="$DEFAULT_HOST"
    fi
    
    # Verifica e configura a porta
    if [ -z "$API_PORT" ]; then
        log_message "WARN" "API_PORT não encontrado no arquivo .env. Usando $DEFAULT_PORT como padrão."
        API_PORT="$DEFAULT_PORT"
    fi
else
    log_message "WARN" "Arquivo .env não encontrado. Usando configurações padrão."
    API_HOST="$DEFAULT_HOST"
    API_PORT="$DEFAULT_PORT"
fi

# Configura PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:${PWD}/.."

# Inicia o servidor
log_message "INFO" "Iniciando servidor em ${API_HOST}:${API_PORT}..."
log_message "INFO" "Pressione CTRL+C para encerrar."

python -m uvicorn api.main:app \
    --host "$API_HOST" \
    --port "$API_PORT" \
    --reload \
    --log-level info