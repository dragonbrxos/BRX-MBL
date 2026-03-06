#!/bin/bash

# Script de atualização BRX-MBL: APK Native Runner
# Este script permite atualizações incrementais ou uma atualização limpa (remover e clonar novamente)

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

REPO_URL="https://github.com/dragonbrxos/BRX-MBL.git"
REPO_NAME="BRX-MBL"

echo -e "${BLUE}--- Atualizador BRX-MBL: APK Native Runner ---${NC}"

echo -e "Escolha o tipo de atualização:"
echo -e "1) ${GREEN}Atualização Rápida${NC} (git pull - mantém seus arquivos locais)"
echo -e "2) ${YELLOW}Atualização Limpa${NC} (Remove a pasta atual, clona de novo e reinstala - RECOMENDADO)"
echo -e "3) Sair"
read -p "Opção: " update_choice

case $update_choice in
    1)
        echo -e "${GREEN}Buscando atualizações incrementais...${NC}"
        if [ -d .git ]; then
            git pull origin main
            chmod +x scripts/*.sh
            ./scripts/install.sh
        else
            echo -e "${RED}Erro: Pasta .git não encontrada. Use a opção 2 (Atualização Limpa).${NC}"
            exit 1
        fi
        ;;
    2)
        echo -e "${YELLOW}Iniciando Atualização Limpa...${NC}"
        cd ..
        echo -e "${RED}Removendo versão antiga...${NC}"
        rm -rf "$REPO_NAME"
        echo -e "${GREEN}Clonando versão mais recente do GitHub...${NC}"
        git clone "$REPO_URL"
        cd "$REPO_NAME"
        chmod +x scripts/*.sh
        echo -e "${GREEN}Iniciando instalação completa...${NC}"
        ./scripts/install.sh
        ;;
    3)
        echo -e "Saindo..."
        exit 0
        ;;
    *)
        echo -e "${RED}Opção inválida.${NC}"
        exit 1
        ;;
esac

echo -e "${GREEN}--- BRX-MBL Atualizado com Sucesso! ---${NC}"
