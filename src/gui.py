import sys
import os
from PyQt6.QtWidgets import (QApplication, QMainWindow, QPushButton, QVBoxLayout, 
                             QWidget, QFileDialog, QLabel, QListWidget, QMessageBox)
from PyQt6.QtCore import Qt
from main import APKNativeBridge

class APKBridgeGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("APK Native Bridge - Manjaro")
        self.setGeometry(100, 100, 600, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)
        
        self.label = QLabel("Selecione um APK para rodar nativamente no Linux")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)
        
        self.btn_select = QPushButton("Selecionar APK")
        self.btn_select.clicked.connect(self.select_apk)
        self.layout.addWidget(self.btn_select)
        
        self.apk_list = QListWidget()
        self.layout.addWidget(self.apk_list)
        
        self.btn_run = QPushButton("Rodar APK Selecionado")
        self.btn_run.clicked.connect(self.run_selected_apk)
        self.layout.addWidget(self.btn_run)
        
        self.selected_apk_path = None

    def select_apk(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self, "Selecionar APK", "", "Android Packages (*.apk)")
        if file_path:
            self.selected_apk_path = file_path
            self.apk_list.clear()
            self.apk_list.addItem(os.path.basename(file_path))
            self.label.setText(f"Selecionado: {os.path.basename(file_path)}")

    def run_selected_apk(self):
        if not self.selected_apk_path:
            QMessageBox.warning(self, "Erro", "Por favor, selecione um APK primeiro.")
            return
        
        try:
            # Em um app real, isso rodaria em uma thread para não congelar a GUI
            QMessageBox.information(self, "Iniciando", f"Tentando rodar {os.path.basename(self.selected_apk_path)}...\nIsso é um protótipo e a execução ocorrerá no terminal.")
            # A execução real é complexa e requer um ambiente configurado.
            # Este protótipo foca na estrutura do projeto.
            print(f"GUI: Iniciando bridge para {self.selected_apk_path}")
            # A chamada real seria algo como:
            # bridge = APKNativeBridge(self.selected_apk_path)
            # bridge.setup()
            # bridge.run()
        except Exception as e:
            QMessageBox.critical(self, "Erro de Execução", f"Falha ao rodar o APK: {str(e)}")

if __name__ == "__main__":
    # Dependências: pip install PyQt6
    app = QApplication(sys.argv)
    window = APKBridgeGUI()
    window.show()
    sys.exit(app.exec())
