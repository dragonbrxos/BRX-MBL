import os
import subprocess
import ctypes
import sys

class NativeBridge:
    def __init__(self, env_config):
        self.env_config = env_config
        self.lib_path = env_config.get("lib_path")
        self.dex_files = env_config.get("dex_files")
        self.extract_path = env_config.get("extract_path")

    def setup_environment(self):
        """Configura as variáveis de ambiente para o runtime nativo."""
        # Adicionar o caminho das bibliotecas do APK ao LD_LIBRARY_PATH
        if self.lib_path:
            os.environ["LD_LIBRARY_PATH"] = f"{self.lib_path}:{os.environ.get('LD_LIBRARY_PATH', '')}"
        
        # Configurar o classpath para o Dalvik/ART
        classpath = ":".join([os.path.join(self.extract_path, dex) for dex in self.dex_files])
        os.environ["CLASSPATH"] = classpath
        
        # Definir o diretório de dados do Android (simulado)
        os.environ["ANDROID_DATA"] = "/tmp/apk_bridge/android_data"
        if not os.path.exists("/tmp/apk_bridge/android_data"):
            os.makedirs("/tmp/apk_bridge/android_data")

    def run_app(self, main_class):
        """Inicia a execução do app usando o runtime nativo (dalvikvm/art)."""
        self.setup_environment()
        
        # Comando para rodar o bytecode Dalvik nativamente no Linux
        # Requer que o pacote 'art-standalone' ou similar esteja instalado
        cmd = [
            "dalvikvm",
            "-Xbootclasspath:/usr/share/art/core-oj.jar:/usr/share/art/core-libart.jar",
            "-cp", os.environ["CLASSPATH"],
            main_class
        ]
        
        print(f"Executando: {' '.join(cmd)}")
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return process
        except FileNotFoundError:
            print("Erro: Runtime 'dalvikvm' não encontrado. Certifique-se de instalar as dependências.")
            return None

    def load_native_library(self, lib_name):
        """Tenta carregar uma biblioteca nativa do APK via ctypes."""
        if not self.lib_path:
            return None
        
        lib_full_path = os.path.join(self.lib_path, lib_name)
        try:
            # Carregar a biblioteca nativa do Android no processo Python
            # Nota: Isso pode falhar se a biblioteca depender de símbolos da Bionic libc
            lib = ctypes.CDLL(lib_full_path)
            return lib
        except Exception as e:
            print(f"Falha ao carregar biblioteca nativa {lib_name}: {e}")
            return None
