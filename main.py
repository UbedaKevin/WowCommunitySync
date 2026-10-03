import sys

from PySide6.QtWidgets import QApplication

import config

from services.api_service import ApiService
from services.sync_service import SyncService
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    api_service = ApiService(
        config.API_BASE_URL,
        config.API_ACCESS_TOKEN
    )

    sync_service = SyncService(
        api_service
    )

    window = MainWindow(
        sync_service
    )

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()