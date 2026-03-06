# BRX-MBL: APK Native Runner (Manjaro/Arch Linux)

O **BRX-MBL** é uma solução robusta para executar aplicativos Android (.apk) nativamente no Linux, sem a necessidade de emular um sistema Android completo ou usar containers pesados. Ele utiliza uma camada de tradução de baixo nível (baseada no projeto **Android Translation Layer - ATL**) para mapear as chamadas de sistema e APIs do Android diretamente para o ambiente Linux, funcionando de forma análoga ao Wine para aplicativos Windows.

## 🚀 Funcionalidades
- **Execução Nativa**: Roda APKs como processos Linux comuns, integrados ao seu desktop.
- **Tradução de APIs**: Mapeia gráficos (EGL/GLES), áudio e entrada para bibliotecas nativas do Linux.
- **Interface Gráfica (GUI)**: Aplicativo em Python (PyQt6) para gerenciar e lançar APKs com facilidade.
- **Integração com o Sistema**: Suporte a clique duplo em arquivos `.apk` e atalho no menu de aplicativos.

## 🛠️ Instalação Passo a Passo

Siga os comandos abaixo no seu terminal para clonar e instalar o BRX-MBL no seu Manjaro ou Arch Linux:

### 1. Clonar o Repositório
```bash
git clone https://github.com/dragonbrxos/BRX-MBL.git
cd BRX-MBL
```

### 2. Executar o Instalador
O instalador automatizado cuidará de todas as dependências do sistema e do AUR (como `bionic_translation` e `android_translation_layer`).
```bash
chmod +x scripts/install.sh
./scripts/install.sh
```

## 🖥️ Como Usar

Após a instalação, você tem três formas de rodar seus aplicativos APK:

1. **Clique Duplo**: No seu gerenciador de arquivos, basta clicar duas vezes em qualquer arquivo `.apk`.
2. **Menu de Aplicativos**: Procure por **"BRX-MBL APK Runner"** no seu menu de aplicativos (KDE, GNOME, XFCE, etc.).
3. **Linha de Comando**:
   ```bash
   brx-mbl /caminho/para/seu_app.apk
   ```

## 📦 Arquitetura do Projeto
- **`native_engine/`**: Contém o código-fonte do motor de tradução de baixo nível (ATL).
- **`src/gui.py`**: Interface gráfica em Python que orquestra a execução.
- **`scripts/install.sh`**: Script de automação para configuração do ambiente nativo.

## ⚠️ Observações Importantes
- **Compatibilidade**: O projeto está em desenvolvimento ativo. Aplicativos que dependem fortemente de Google Play Services podem não funcionar perfeitamente.
- **Gráficos**: O BRX-MBL força o uso de EGL para garantir que os gráficos do Android sejam renderizados corretamente via Mesa/OpenGL no Linux.

## 📄 Licença
Este projeto é distribuído sob a licença MIT.
