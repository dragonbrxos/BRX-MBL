#!/bin/bash

# Script de atualização BRX-MBL: APK Native Runner
# Este script atualiza o código do repositório e reinstala os componentes necessários

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}--- Atualizador BRX-MBL: APK Native Runner ---${NC}"

# 1. Verificar se estamos em um repositório git
if [ ! -d .git ]; then
    echo -e "${RED}Erro: Este script deve ser executado na raiz do repositório BRX-MBL.${NC}"
    exit 1
fi

# 2. Puxar as últimas alterações do GitHub
echo -e "${GREEN}Buscando atualizações no GitHub...${NC}"
git pull origin main

# 3. Tornar os scripts executáveis (caso tenham mudado)
chmod +x scripts/install.sh
chmod +x scripts/update.sh

# 4. Perguntar se deseja reinstalar as dependências
read -p "Deseja rodar o instalador para aplicar as atualizações de sistema? (s/n): " choice
if [[ "$choice" == "s" || "$choice" == "S" ]]; then
    echo -e "${GREEN}Iniciando o instalador...${NC}"
    ./scripts/install.sh
else
    echo -e "${BLUE}Atualização de código concluída. Nenhuma alteração de sistema foi feita.${NC}"
fi

echo -e "${GREEN}--- BRX-MBL Atualizado com Sucesso! ---${NC}"
