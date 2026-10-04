from PySide6.QtCore import Qt, QUrl
from PySide6.QtWidgets import (
    QCheckBox,
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from PySide6.QtGui import QDesktopServices

import json
from pathlib import Path

class LoginWindow(QDialog):

    def __init__(
        self,
        auth_service,
        parent=None,
    ):
        super().__init__(parent)

        self.auth_service = auth_service
        self.preferences_file = (
            Path.home() / ".wowcommunity_preferences.json"
        )
        self.setWindowTitle(
            "WoW Community Sync"
        )

        self.setFixedSize(
            500,
            650
        )

        self.setup_ui()
        self.load_preferences()
        self.apply_style()

    def load_preferences(self):
        if not self.preferences_file.exists():
            return

        try:
            with self.preferences_file.open(
                "r",
                encoding="utf-8"
            ) as file:
                data = json.load(file)

            self.remember_checkbox.setChecked(
                data.get("rememberMe", False)
            )

        except (OSError, json.JSONDecodeError):
            self.remember_checkbox.setChecked(False)


    def save_preferences(self):
        data = {
            "rememberMe": self.remember_checkbox.isChecked()
        }

        try:
            with self.preferences_file.open(
                "w",
                encoding="utf-8"
            ) as file:
                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False,
                )

        except OSError:
            pass
    # =========================================================
    # UI
    # =========================================================

    def setup_ui(self):

        main_layout = QVBoxLayout()

        main_layout.setContentsMargins(
            60,
            40,
            60,
            40
        )

        main_layout.setSpacing(
            0
        )

        main_layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # =====================================================
        # Logo
        # =====================================================

        logo = QLabel("W")

        logo.setObjectName(
            "logo"
        )

        logo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        logo.setFixedSize(
            70,
            70
        )

        main_layout.addWidget(
            logo,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addSpacing(
            25
        )

        # =====================================================
        # Welcome
        # =====================================================

        welcome_label = QLabel(
            "Welcome To"
        )

        welcome_label.setObjectName(
            "welcome"
        )

        welcome_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(
            welcome_label
        )

        title_label = QLabel(
            "WoW Community Sync"
        )

        title_label.setObjectName(
            "title"
        )

        title_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        main_layout.addWidget(
            title_label
        )

        main_layout.addSpacing(
            35
        )

        # =====================================================
        # Login card
        # =====================================================

        login_frame = QFrame()

        login_frame.setObjectName(
            "loginFrame"
        )

        login_layout = QVBoxLayout(
            login_frame
        )

        login_layout.setContentsMargins(
            30,
            30,
            30,
            30
        )

        login_layout.setSpacing(
            15
        )

        # =====================================================
        # Email
        # =====================================================

        self.email_input = QLineEdit()

        self.email_input.setPlaceholderText(
            "Email"
        )

        login_layout.addWidget(
            self.email_input
        )

        # =====================================================
        # Password
        # =====================================================

        self.password_input = QLineEdit()

        self.password_input.setPlaceholderText(
            "Password"
        )

        self.password_input.setEchoMode(
            QLineEdit.EchoMode.Password
        )

        login_layout.addWidget(
            self.password_input
        )

        # =====================================================
        # Remember / Forgot
        # =====================================================

        options_layout = QHBoxLayout()

        self.remember_checkbox = QCheckBox(
            "Remember me"
        )

        options_layout.addWidget(
            self.remember_checkbox
        )

        options_layout.addStretch()

        forgot_button = QPushButton(
            "Forgot password?"
        )

        forgot_button.setObjectName(
            "forgotButton"
        )

        forgot_button.setFlat(
            True
        )
        forgot_button.clicked.connect(
            lambda: QDesktopServices.openUrl(
                QUrl("http://localhost:3000")
            )
        )
        options_layout.addWidget(
            forgot_button
        )

        login_layout.addLayout(
            options_layout
        )

        login_layout.addSpacing(
            10
        )

        # =====================================================
        # Login button
        # =====================================================

        self.login_button = QPushButton(
            "Log in  →"
        )

        self.login_button.setObjectName(
            "loginButton"
        )

        self.login_button.clicked.connect(
            self.handle_login
        )

        login_layout.addWidget(
            self.login_button
        )

        # =====================================================
        # Status
        # =====================================================

        self.status_label = QLabel()

        self.status_label.setObjectName(
            "status"
        )

        self.status_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.status_label.setWordWrap(
            True
        )

        login_layout.addWidget(
            self.status_label
        )

        main_layout.addWidget(
            login_frame
        )

        self.setLayout(
            main_layout
        )

    # =========================================================
    # Style
    # =========================================================

    def apply_style(self):

        self.setStyleSheet(
            """
            QDialog {
                background-color: #000000;
            }

            QLabel {
                color: #FFFFFF;
            }

            QLabel#logo {
                color: #F0840D;
                border: 3px solid #F0840D;
                border-radius: 12px;
                font-size: 30px;
                font-weight: bold;
                background-color: transparent;
            }

            QLabel#welcome {
                color: #AEB4BE;
                font-size: 18px;
                background-color: transparent;
            }

            QLabel#title {
                color: #FFFFFF;
                font-size: 28px;
                font-weight: bold;
                background-color: transparent;
            }

            QFrame#loginFrame {
                background-color: #111318;
                border: 1px solid #292D35;
                border-radius: 10px;
            }

            QLineEdit {
                background-color: #000000;
                color: #FFFFFF;
                border: 1px solid #353B46;
                border-radius: 6px;
                padding: 13px;
                font-size: 14px;
            }

            QLineEdit:focus {
                border: 1px solid #F0840D;
            }

            QLineEdit::placeholder {
                color: #666B75;
            }

            QCheckBox {
                color: #AEB4BE;
                font-size: 13px;
                spacing: 7px;
            }

            QCheckBox::indicator {
                width: 15px;
                height: 15px;
                border: 1px solid #353B46;
                border-radius: 4px;
                background-color: #000000;
            }

            QCheckBox::indicator:hover {
                border: 1px solid #F0840D;
            }

            QCheckBox::indicator:checked {
                background-color: #F0840D;
                border: 1px solid #F0840D;
            }

            QPushButton#forgotButton {
                color: #F0840D;
                background-color: transparent;
                border: none;
                padding: 0;
            }

            QPushButton#forgotButton:hover {
                color: #FFFFFF;
            }

            QPushButton#loginButton {
                background-color: #F0840D;
                color: #FFFFFF;
                border: none;
                border-radius: 6px;
                padding: 13px;
                font-size: 15px;
                font-weight: bold;
            }

            QPushButton#loginButton:hover {
                background-color: #FF982D;
            }

            QPushButton#loginButton:pressed {
                background-color: #D66F00;
            }

            QLabel#status {
                color: #F0840D;
                font-size: 13px;
                background-color: transparent;
                border: none;
            }
            """
        )

    # =========================================================
    # Login
    # =========================================================

    def handle_login(self):

        email = self.email_input.text().strip()
        password = self.password_input.text()

        if not email or not password:

            self.status_label.setText(
                "Please enter your email and password."
            )

            return

        self.login_button.setEnabled(
            False
        )

        self.status_label.setText(
            "Signing in..."
        )

        try:
            self.auth_service.login(
                email,
                password,
                remember_me=self.remember_checkbox.isChecked(),
            )
            
            self.save_preferences()

        except Exception as error:

            self.status_label.setText(
                str(error)
            )

            self.login_button.setEnabled(
                True
            )

            return

        self.accept()

    def closeEvent(self, event):
        if not self.auth_service.is_authenticated():
            event.accept()
            return

        event.accept()