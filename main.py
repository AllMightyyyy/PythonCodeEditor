import sys
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QMessageBox,
    QSplitter, QFontDialog
)
from PySide6.QtGui import QAction, QIcon
from PySide6.QtCore import Qt
from editor import CodeEditor
from preview import LivePreview
from find_replace_dialog import FindReplaceDialog 

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Professional Code Editor")

        self.editor = CodeEditor()
        self.preview = LivePreview()
        
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.editor)
        splitter.addWidget(self.preview)
        splitter.setSizes([800, 400])

        self.setCentralWidget(splitter)

        # Create Menus and Actions
        self.create_actions()
        self.create_menus()

        # Connect Editor's signal to update_preview
        self.editor.text_changed_for_preview.connect(self.update_preview)

        # Initial preview update
        self.update_preview()

    def create_actions(self):
        # File actions
        self.open_action = QAction("&Open", self)
        self.open_action.setShortcut("Ctrl+O")
        self.open_action.triggered.connect(self.open_file)

        self.save_action = QAction("&Save", self)
        self.save_action.setShortcut("Ctrl+S")
        self.save_action.triggered.connect(self.save_file)

        self.save_as_action = QAction("Save &As", self)
        self.save_as_action.triggered.connect(self.save_file_as)

        self.exit_action = QAction("E&xit", self)
        self.exit_action.setShortcut("Ctrl+Q")
        self.exit_action.triggered.connect(self.close)

        # Edit actions
        self.find_action = QAction("&Find", self)
        self.find_action.setShortcut("Ctrl+F")
        self.find_action.triggered.connect(self.find_text)

        self.replace_action = QAction("&Replace", self)
        self.replace_action.setShortcut("Ctrl+H")
        self.replace_action.triggered.connect(self.replace_text)

        # View actions
        self.light_theme_action = QAction("&Light Theme", self)
        self.light_theme_action.triggered.connect(self.set_light_theme)

        self.dark_theme_action = QAction("&Dark Theme", self)
        self.dark_theme_action.triggered.connect(self.set_dark_theme)

        self.change_font_action = QAction("&Change Font", self)
        self.change_font_action.triggered.connect(self.change_font)

    def create_menus(self):
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("&File")
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.save_action)
        file_menu.addAction(self.save_as_action)
        file_menu.addSeparator()
        file_menu.addAction(self.exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("&Edit")
        edit_menu.addAction(self.find_action)
        edit_menu.addAction(self.replace_action)

        # View menu
        view_menu = menubar.addMenu("&View")
        view_menu.addAction(self.light_theme_action)
        view_menu.addAction(self.dark_theme_action)
        view_menu.addAction(self.change_font_action)

    def open_file(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Open File", "", "HTML Files (*.html *.htm);;XML Files (*.xml);;All Files (*)"
        )
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.editor.setPlainText(content)
                    self.current_file = path
                    self.setWindowTitle(f"Professional Code Editor - {path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not open file: {e}")

    def save_file(self):
        if hasattr(self, 'current_file'):
            try:
                with open(self.current_file, 'w', encoding='utf-8') as file:
                    content = self.editor.toPlainText()
                    file.write(content)
                    QMessageBox.information(self, "Saved", "File saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save file: {e}")
        else:
            self.save_file_as()

    def save_file_as(self):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File As", "", "HTML Files (*.html *.htm);;XML Files (*.xml);;All Files (*)"
        )
        if path:
            try:
                with open(path, 'w', encoding='utf-8') as file:
                    content = self.editor.toPlainText()
                    file.write(content)
                    self.current_file = path
                    self.setWindowTitle(f"Professional Code Editor - {path}")
                    QMessageBox.information(self, "Saved", "File saved successfully.")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Could not save file: {e}")

    def find_text(self):
        dialog = FindReplaceDialog(self.editor, replace=False)
        dialog.exec()

    def replace_text(self):
        dialog = FindReplaceDialog(self.editor, replace=True)
        dialog.exec()

    def set_light_theme(self):
        light_style = """
        QPlainTextEdit {
            background-color: #FFFFFF;
            color: #000000;
            font-family: Consolas;
            font-size: 14px;
        }

        QMenuBar {
            background-color: #E0E0E0;
            color: #000000;
        }

        QMenuBar::item:selected {
            background-color: #A0A0A0;
        }

        QMenu {
            background-color: #F0F0F0;
            color: #000000;
        }

        QMenu::item:selected {
            background-color: #C0C0C0;
        }
        """
        self.setStyleSheet(light_style)
        self.editor.set_theme('light')

    def set_dark_theme(self):
        dark_style = """
        QPlainTextEdit {
            background-color: #2B2B2B;
            color: #D4D4D4; /* Light Gray */
            font-family: Consolas;
            font-size: 14px;
        }

        QMenuBar {
            background-color: #333333;
            color: #FFFFFF;
        }

        QMenuBar::item:selected {
            background-color: #555555;
        }

        QMenu {
            background-color: #444444;
            color: #FFFFFF;
        }

        QMenu::item:selected {
            background-color: #666666;
        }
        """
        self.setStyleSheet(dark_style)
        self.editor.set_theme('dark')

    def change_font(self):
        font, ok = QFontDialog.getFont(self.editor.font(), self, "Select Font")
        if ok:
            self.editor.setFont(font)

    def update_preview(self):
        html_content = self.editor.toPlainText()
        self.preview.update_preview(html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set initial theme to dark
    app.setStyleSheet(open("resources/styles.qss").read())
    window = MainWindow()
    window.resize(1200, 800)
    window.show()
    sys.exit(app.exec())
