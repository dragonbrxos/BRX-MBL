# APK-Native-Bridge (Manjaro/Arch Linux)

Este projeto é uma camada de compatibilidade nativa escrita em Python para rodar aplicativos Android (.apk) no Linux (Manjaro/Arch) sem a necessidade de emular um sistema Android completo ou usar containers (como Waydroid). Ele funciona de forma análoga ao Wine, traduzindo as chamadas de sistema e APIs do Android para o ambiente Linux.

## 🚀 Funcionalidades
- **Extração Nativa**: Descompacta e analisa o APK para identificar bibliotecas nativas e bytecode.
- **Mapeamento de Bibliotecas**: Carrega bibliotecas `.so` do Android e tenta mapear chamadas para a `glibc` do Linux.
- **Runtime Independente**: Utiliza o `dalvikvm` ou `art` (via `art-standalone`) para executar o bytecode Dalvik nativamente.
- **Interface Gráfica (GUI)**: Gerenciador simples em PyQt6 para selecionar e rodar APKs.

## 🛠️ Arquitetura
O projeto é dividido em três componentes principais:
1. **`parser.py`**: Responsável por extrair o conteúdo do APK e preparar o ambiente de execução.
2. **`bridge.py`**: O núcleo que configura as variáveis de ambiente (`LD_LIBRARY_PATH`, `CLASSPATH`) e inicia o runtime nativo.
3. **`gui.py`**: Interface gráfica para interação amigável com o usuário.

## 📦 Instalação no Manjaro
Para instalar as dependências necessárias e configurar o ambiente, execute o script de instalação:

```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

### Dependências Principais:
- **Python 3.10+**
- **PyQt6** (Interface Gráfica)
- **art-standalone** (Runtime Android independente via AUR)
- **bionic_translation** (Camada de tradução da libc do Android via AUR)

## 🖥️ Como Usar
Após a instalação, você pode iniciar a interface gráfica:

```bash
apk-bridge
```

Ou rodar um APK diretamente via linha de comando:

```bash
python3 src/main.py /caminho/para/seu_app.apk
```

## ⚠️ Observações Importantes
- **Status do Projeto**: Este é um protótipo funcional da estrutura de tradução nativa. Nem todos os aplicativos (especialmente os que dependem de Google Play Services) funcionarão perfeitamente.
- **Tradução ARM**: O projeto foca na execução nativa. Para APKs compilados apenas para ARM em processadores x86_64, é necessário que o sistema tenha suporte a tradução binária (como `libndk` ou `libhoudini`).
- **Nativo vs Emulado**: Diferente do Waydroid, este programa não sobe um container LXC com o Android inteiro. Ele tenta rodar o app como um processo Linux comum.

## 📄 Licença
Este projeto é distribuído sob a licença MIT.
