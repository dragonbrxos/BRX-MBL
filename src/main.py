import sys
import os
from parser import APKParser
from bridge import NativeBridge

class APKNativeBridge:
    def __init__(self, apk_path):
        self.apk_path = apk_path
        self.parser = APKParser(apk_path)
        self.env_config = None
        self.bridge = None

    def setup(self):
        print(f"[APKNativeBridge] Configurando para APK: {self.apk_path}")
        self.env_config = self.parser.prepare_runtime_env()
        self.bridge = NativeBridge(self.env_config)

    def run(self, main_activity="android.app.Activity"):
        if not self.bridge:
            print("[APKNativeBridge] Erro: Bridge não configurada. Chame setup() primeiro.")
            return
        
        print(f"[APKNativeBridge] Tentando executar a atividade principal: {main_activity}")
        process = self.bridge.run_app(main_activity)
        if process:
            print("[APKNativeBridge] Aplicação Android iniciada. Saída:")
            for line in process.stdout:
                print(f"[APP OUT] {line.strip()}")
            process.wait()
            print(f"[APKNativeBridge] Aplicação finalizada com código: {process.returncode}")
        else:
            print("[APKNativeBridge] Falha ao iniciar a aplicação.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python main.py <caminho_para_apk> [main_activity]")
        sys.exit(1)

    apk_file = sys.argv[1]
    main_activity_class = sys.argv[2] if len(sys.argv) > 2 else "android.app.Activity" # Placeholder

    if not os.path.exists(apk_file):
        print(f"Erro: Arquivo APK não encontrado: {apk_file}")
        sys.exit(1)

    app_bridge = APKNativeBridge(apk_file)
    app_bridge.setup()
    app_bridge.run(main_activity_class)
