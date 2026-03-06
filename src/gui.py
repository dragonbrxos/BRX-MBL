import sys
import os
import subprocess
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QFileDialog, QLabel, QListWidget, QMessageBox, 
                             QProgressBar, QHBoxLayout)
from PyQt6.QtCore import Qt, QThread, pyqtSignal

class APKRunnerThread(QThread):
    finished_signal = pyqtSignal(int)
    output_signal = pyqtSignal(str)

    def __init__(self, apk_path):
        super().__init__()
        self.apk_path = apk_path

    def run(self):
        # Comando para rodar o motor nativo ATL
        # O ATL deve estar instalado no sistema via o script de instalação
        cmd = ["android-translation-layer", self.apk_path]
        
        # Configurações de ambiente para garantir execução nativa
        env = os.environ.copy()
        env["GDK_DEBUG"] = "gl-egl" # Forçar EGL para compatibilidade com Android
        
        try:
            process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.STDOUT, 
                text=True,
                env=env
            )
            
            if process.stdout:
                for line in process.stdout:
                    self.output_signal.emit(line.strip())
            
            process.wait()
            self.finished_signal.emit(process.returncode)
        except Exception as e:
            self.output_signal.emit(f"Erro ao iniciar: {str(e)}")
            self.finished_signal.emit(-1)

class BRX_MBL_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BRX-MBL: APK Native Runner")
        self.setGeometry(100, 100, 700, 500)
        self.setStyleSheet("""
            QMainWindow { background-color: #1e1e2e; color: #cdd6f4; }
            QPushButton { background-color: #89b4fa; color: #11111b; border-radius: 5px; padding: 10px; font-weight: bold; }
            QPushButton:hover { background-color: #b4befe; }
            QLabel { color: #cdd6f4; font-size: 14px; }
            QListWidget { background-color: #313244; color: #cdd6f4; border-radius: 5px; }
        """)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.header = QLabel("BRX-MBL - Camada de Tradução Nativa Android")
        self.header.setStyleSheet("font-size: 20px; font-weight: bold; margin-bottom: 10px;")
        self.header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.header)
        
        self.info_label = QLabel("Selecione um APK para rodar diretamente no seu Linux (estilo Wine)")
        self.info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.info_label)
        
        self.btn_select = QPushButton("Selecionar Aplicativo APK")
        self.btn_select.clicked.connect(self.select_apk)
        self.layout.addWidget(self.btn_select)
        
        self.apk_list = QListWidget()
        self.layout.addWidget(self.apk_list)
        
        self.progress = QProgressBar()
        self.progress.hide()
        self.layout.addWidget(self.progress)
        
        self.btn_run = QPushButton("Rodar Nativamente")
        self.btn_run.clicked.connect(self.run_apk)
        self.layout.addWidget(self.btn_run)
        
        self.selected_apk = None

    def select_apk(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Abrir APK", "", "Android Packages (*.apk)")
        if file_path:
            self.selected_apk = file_path
            self.apk_list.clear()
            self.apk_list.addItem(f"Pronto para rodar: {os.path.basename(file_path)}")
            self.info_label.setText(f"Arquivo: {os.path.basename(file_path)}")

    def run_apk(self):
        if not self.selected_apk:
            QMessageBox.warning(self, "Aviso", "Por favor, selecione um arquivo APK primeiro.")
            return
        
        self.btn_run.setEnabled(False)
        self.progress.show()
        self.progress.setRange(0, 0) # Modo indeterminado
        
        self.runner_thread = APKRunnerThread(self.selected_apk)
        self.runner_thread.output_signal.connect(self.handle_output)
        self.runner_thread.finished_signal.connect(self.handle_finished)
        self.runner_thread.start()

    def handle_output(self, text):
        print(f"[ATL LOG] {text}")

    def handle_finished(self, exit_code):
        self.btn_run.setEnabled(True)
        self.progress.hide()
        if exit_code == 0:
            print("Aplicação finalizada com sucesso.")
        else:
            QMessageBox.critical(self, "Erro", f"O aplicativo fechou com erro (Código: {exit_code}). Verifique se as dependências do ATL estão instaladas.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BRX_MBL_GUI()
    window.show()
    sys.exit(app.exec())
