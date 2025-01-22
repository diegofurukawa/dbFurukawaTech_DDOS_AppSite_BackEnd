#!/bin/bash

# Ativa o ambiente virtual se existir
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Executa o projeto
# Modifique seu script run_api.sh para:
export PYTHONPATH="${PYTHONPATH}:${PWD}/.."
#  python -m uvicorn api.main:app --host 192.168.68.111 --reload --port 8000
python -m uvicorn api.main:app