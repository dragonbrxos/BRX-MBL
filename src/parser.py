import zipfile
import os
import shutil
import json

class APKParser:
    def __init__(self, apk_path, work_dir="/tmp/apk_bridge"):
        self.apk_path = apk_path
        self.work_dir = work_dir
        self.extract_path = os.path.join(self.work_dir, "extracted")
        
    def extract_apk(self):
        """Extrai o conteúdo do APK para o diretório de trabalho."""
        if not os.path.exists(self.work_dir):
            os.makedirs(self.work_dir)
        if os.path.exists(self.extract_path):
            shutil.rmtree(self.extract_path)
        os.makedirs(self.extract_path)
        
        with zipfile.ZipFile(self.apk_path, 'r') as zip_ref:
            zip_ref.extractall(self.extract_path)
        return self.extract_path

    def get_native_libs(self):
        """Identifica as bibliotecas nativas (.so) no APK."""
        libs = {}
        lib_dir = os.path.join(self.extract_path, "lib")
        if os.path.exists(lib_dir):
            for arch in os.listdir(lib_dir):
                arch_path = os.path.join(lib_dir, arch)
                if os.path.isdir(arch_path):
                    libs[arch] = [f for f in os.listdir(arch_path) if f.endswith('.so')]
        return libs

    def prepare_runtime_env(self):
        """Prepara o ambiente para execução nativa."""
        self.extract_apk()
        libs = self.get_native_libs()
        # Priorizar x86_64 se disponível, senão usar tradução ARM
        target_arch = "x86_64" if "x86_64" in libs else "armeabi-v7a"
        
        env_config = {
            "extract_path": self.extract_path,
            "libs": libs.get(target_arch, []),
            "lib_path": os.path.join(self.extract_path, "lib", target_arch) if target_arch in libs else None,
            "dex_files": [f for f in os.listdir(self.extract_path) if f.endswith('.dex')]
        }
        return env_config
