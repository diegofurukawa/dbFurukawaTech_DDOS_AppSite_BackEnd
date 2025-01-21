#!/bin/bash

# Cores para melhor visualização
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Volta para o diretório pai
cd ..

echo -e "${GREEN}Iniciando setup do DDoS Protection API Backend...${NC}"

# Verifica se Python 3 está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Python 3 não está instalado. Por favor, instale o Python 3 primeiro.${NC}"
    exit 1
fi

# Verifica se pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}pip3 não está instalado. Por favor, instale o pip3 primeiro.${NC}"
    exit 1
fi

# Cria ambiente virtual
echo -e "${YELLOW}Criando ambiente virtual...${NC}"
python3 -m venv venv

# Ativa o ambiente virtual
echo -e "${YELLOW}Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Atualiza pip
echo -e "${YELLOW}Atualizando pip...${NC}"
pip install --upgrade pip

# Instala dependências
echo -e "${YELLOW}Instalando dependências do projeto...${NC}"
pip install -r requirements.txt

# Cria diretórios necessários
echo -e "${YELLOW}Criando estrutura de diretórios...${NC}"
mkdir -p logs
mkdir -p data/import/geoip
mkdir -p data/import/alerts
mkdir -p data/import/mitigations
mkdir -p data/import/managed_objects

# Configura permissões dos scripts
echo -e "${YELLOW}Configurando permissões...${NC}"
chmod +x scripts/*.sh

# Configura PYTHONPATH
echo -e "${YELLOW}Configurando PYTHONPATH...${NC}"
export PYTHONPATH="${PYTHONPATH}:${PWD}"

echo -e "${GREEN}Setup concluído com sucesso!${NC}"
echo -e "${YELLOW}Para iniciar o servidor, execute:${NC}"
echo -e "source venv/bin/activate"
echo -e "./scripts/run_api.sh"