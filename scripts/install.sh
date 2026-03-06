#!/bin/bash

# Script de instalação BRX-MBL: APK Native Runner para Manjaro/Arch
# Este script configura o motor de tradução nativa e cria atalhos de sistema

set -e

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}--- Instalador BRX-MBL: APK Native Runner ---${NC}"

# 1. Instalar dependências básicas do sistema
echo -e "${GREEN}Instalando dependências do sistema...${NC}"
sudo pacman -S --noconfirm python-pip python-pyqt6 base-devel git jre-openjdk-headless alsa-lib cairo ffmpeg gdk-pixbuf2 glib2 glibc graphene gtk4 harfbuzz meson ninja

# 2. Instalar o motor de tradução nativa (ATL) via AUR
# O ATL é o componente de baixo nível que faz a tradução estilo Wine
echo -e "${GREEN}Instalando motor de tradução nativa (ATL) via AUR...${NC}"
if command -v pamac >/dev/null 2>&1; then
    pamac build --no-confirm bionic_translation art_standalone android_translation_layer
elif command -v yay >/dev/null 2>&1; then
    yay -S --noconfirm bionic_translation art_standalone android_translation_layer
else
    echo -e "${RED}Erro: Nenhum helper de AUR (pamac ou yay) encontrado. Instale as dependências do ATL manualmente.${NC}"
    exit 1
fi

# 3. Configurar caminhos de biblioteca para o runtime Android
echo -e "${GREEN}Configurando caminhos de biblioteca...${NC}"
if [ ! -f /etc/ld.so.conf.d/art.conf ]; then
    echo "/usr/lib/art" | sudo tee /etc/ld.so.conf.d/art.conf
    sudo ldconfig
fi

# 4. Configurar o comando global do BRX-MBL
echo -e "${GREEN}Configurando comando global 'brx-mbl'...${NC}"
INSTALL_DIR=$(pwd)
cat << EOF | sudo tee /usr/local/bin/brx-mbl > /dev/null
#!/bin/bash
export GDK_DEBUG=gl-egl
python3 $INSTALL_DIR/src/gui.py "\$@"
EOF
sudo chmod +x /usr/local/bin/brx-mbl

# 5. Criar atalho .desktop para o menu de aplicativos
echo -e "${GREEN}Criando atalho no menu de aplicativos...${NC}"
mkdir -p ~/.local/share/applications
cat << EOF > ~/.local/share/applications/brx-mbl.desktop
[Desktop Entry]
Name=BRX-MBL APK Runner
Comment=Executa aplicativos APK nativamente no Linux
Exec=brx-mbl
Icon=android-sdk
Terminal=false
Type=Application
Categories=System;Utility;
EOF

# 6. Associar arquivos .apk para abertura com um clique
echo -e "${GREEN}Associando arquivos .apk ao BRX-MBL...${NC}"
xdg-mime default brx-mbl.desktop application/vnd.android.package-archive

echo -e "${BLUE}--- Instalação Concluída com Sucesso! ---${NC}"
echo -e "${GREEN}O BRX-MBL agora está integrado ao seu sistema.${NC}"
echo -e "Você pode abrir APKs diretamente pelo menu ou clicando duas vezes neles.${NC}"
