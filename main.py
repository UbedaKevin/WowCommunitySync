import sys

from PySide6.QtWidgets import QApplication

import config
from services.api_service import ApiService
from services.auth_service import AuthService
from services.sync_service import SyncService
from ui.login_window import LoginWindow
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    api_service = ApiService(
        config.API_BASE_URL,
        config.API_ACCESS_TOKEN,
    )

    auth_service = AuthService(api_service)

    def show_login(initial=False):
        login_window = LoginWindow(auth_service)

        result = login_window.exec()

        if result != LoginWindow.DialogCode.Accepted:
            if initial:
                return False

            app.quit()
            return False

        show_main_window()
        return True

    def show_main_window():
        sync_service = SyncService(api_service)

        app.main_window = MainWindow(
            sync_service,
            auth_service,
            on_logout=lambda: show_login(initial=False),
        )

        app.main_window.show()

    if not auth_service.load_session():
        if not show_login(initial=True):
            sys.exit(0)
    else:
        show_main_window()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()

