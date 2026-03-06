#!/bin/bash

# Script de instalação para o APK-Native-Bridge no Manjaro/Arch Linux
# Este script instala as dependências necessárias para a camada de compatibilidade nativa

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}--- Instalador APK-Native-Bridge para Manjaro ---${NC}"

# 1. Instalar dependências do sistema (Pacman)
echo -e "${GREEN}Instalando dependências do sistema...${NC}"
sudo pacman -S --noconfirm python-pip python-pyqt6 base-devel git jre-openjdk-headless alsa-lib cairo ffmpeg gdk-pixbuf2 glib2 glibc graphene gtk4 harfbuzz

# 2. Instalar dependências do AUR (Essenciais para o runtime nativo)
# Nota: Usando pamac (padrão no Manjaro)
echo -e "${GREEN}Instalando componentes de runtime nativo via AUR...${NC}"
if command -v pamac >/dev/null 2>&1; then
    pamac build --no-confirm bionic_translation art_standalone
else
    echo -e "${RED}Aviso: Pamac não encontrado. Por favor, instale 'bionic_translation' e 'art_standalone' manualmente via AUR.${NC}"
fi

# 3. Configurar ambiente Python
echo -e "${GREEN}Configurando ambiente Python...${NC}"
# No Manjaro/Arch, é recomendado usar venv ou pacman para pacotes python
# Para este projeto, usaremos as bibliotecas do sistema instaladas via pacman

# 4. Configurar caminhos de biblioteca
echo -e "${GREEN}Configurando caminhos de biblioteca para o ART...${NC}"
if [ ! -f /etc/ld.so.conf.d/art.conf ]; then
    echo "/usr/lib/art" | sudo tee /etc/ld.so.conf.d/art.conf
    sudo ldconfig
fi

# 5. Criar atalho de execução
echo -e "${GREEN}Criando atalho 'apk-bridge'...${NC}"
cat << EOF | sudo tee /usr/local/bin/apk-bridge > /dev/null
#!/bin/bash
python3 /home/ubuntu/apk-native-bridge/src/gui.py "\$@"
EOF
sudo chmod +x /usr/local/bin/apk-bridge

echo -e "${BLUE}--- Instalação Concluída! ---${NC}"
echo -e "Você pode iniciar o programa digitando: ${GREEN}apk-bridge${NC}"
echo -e "Ou rodar via terminal: ${GREEN}python3 src/main.py seu_app.apk${NC}"
