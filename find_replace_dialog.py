from PySide6.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QCheckBox
from PySide6.QtCore import Qt
from PySide6.QtGui import QTextDocument

class FindReplaceDialog(QDialog):
    def __init__(self, editor, replace=False):
        super().__init__()
        self.editor = editor
        self.replace = replace
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Find and Replace" if self.replace else "Find")
        self.layout = QVBoxLayout()

        # Find
        self.find_label = QLabel("Find:")
        self.find_input = QLineEdit()
        self.layout.addWidget(self.find_label)
        self.layout.addWidget(self.find_input)

        if self.replace:
            # Replace
            self.replace_label = QLabel("Replace:")
            self.replace_input = QLineEdit()
            self.layout.addWidget(self.replace_label)
            self.layout.addWidget(self.replace_input)

        # Options
        self.case_checkbox = QCheckBox("Case Sensitive")
        self.whole_checkbox = QCheckBox("Whole Words")
        self.layout.addWidget(self.case_checkbox)
        self.layout.addWidget(self.whole_checkbox)

        # Buttons
        self.buttons_layout = QHBoxLayout()
        self.find_button = QPushButton("Find")
        self.find_button.clicked.connect(self.find)
        self.buttons_layout.addWidget(self.find_button)

        if self.replace:
            self.replace_button = QPushButton("Replace")
            self.replace_button.clicked.connect(self.replace_text)
            self.buttons_layout.addWidget(self.replace_button)

            self.replace_all_button = QPushButton("Replace All")
            self.replace_all_button.clicked.connect(self.replace_all)
            self.buttons_layout.addWidget(self.replace_all_button)

        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        self.buttons_layout.addWidget(self.close_button)

        self.layout.addLayout(self.buttons_layout)
        self.setLayout(self.layout)

    def find(self):
        flags = QTextDocument.FindFlags()
        if self.case_checkbox.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_checkbox.isChecked():
            flags |= QTextDocument.FindWholeWords
        text = self.find_input.text()
        if not self.editor.find(text, flags):
            # Not found, reset cursor
            cursor = self.editor.textCursor()
            cursor.setPosition(0)
            self.editor.setTextCursor(cursor)
            if not self.editor.find(text, flags):
                # Still not found
                pass

    def replace_text(self):
        cursor = self.editor.textCursor()
        if cursor.hasSelection():
            cursor.insertText(self.replace_input.text())
        self.find()

    def replace_all(self):
        text = self.find_input.text()
        replace_text = self.replace_input.text()
        flags = QTextDocument.FindFlags()
        if self.case_checkbox.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        if self.whole_checkbox.isChecked():
            flags |= QTextDocument.FindWholeWords

        cursor = self.editor.textCursor()
        cursor.beginEditBlock()

        self.editor.moveCursor(cursor.Start)
        while self.editor.find(text, flags):
            tc = self.editor.textCursor()
            tc.insertText(replace_text)

        cursor.endEditBlock()
