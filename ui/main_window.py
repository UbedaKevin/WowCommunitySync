from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QFileDialog,
    QMessageBox,
    QFrame,
    QScrollArea,
)

from wow_saved_variables import load_saved_variables
from models.character import Character
from wow_path import find_saved_variables

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.characters = []

        self.setWindowTitle(
            "WoW Community Sync"
        )

        self.resize(
            900,
            600
        )

        self.setup_ui()
        self.apply_style()
        self.detect_saved_variables()

    # =========================================================
    # UI
    # =========================================================

    def setup_ui(self):

        central_widget = QWidget()

        self.setCentralWidget(
            central_widget
        )

        main_layout = QVBoxLayout(
            central_widget
        )

        main_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        main_layout.setSpacing(
            15
        )

        # =====================================================
        # Header
        # =====================================================

        header_layout = QHBoxLayout()

        logo = QLabel("W")
        logo.setObjectName("logo")
        header_layout.addWidget(logo)

        title = QLabel(
            "WoW Community Sync"
        )

        title.setObjectName(
            "title"
        )

        header_layout.addWidget(
            title
        )

        header_layout.addStretch()

        self.status_label = QLabel(
            "Ready"
        )

        self.status_label.setObjectName(
            "status"
        )

        header_layout.addWidget(
            self.status_label
        )

        main_layout.addLayout(
            header_layout
        )

        # =====================================================
        # File selector
        # =====================================================

        file_frame = QFrame()

        file_layout = QHBoxLayout(
            file_frame
        )

        file_layout.setContentsMargins(
            12,
            8,
            12,
            8
        )

        self.file_input = QLineEdit()

        self.file_input.setPlaceholderText(
            "Select WoWCommunityCollector.lua..."
        )

        browse_button = QPushButton(
            "Browse"
        )

        browse_button.clicked.connect(
            self.browse_file
        )

        scan_button = QPushButton(
            "Scan"
        )

        scan_button.setObjectName(
            "scanButton"
        )

        scan_button.clicked.connect(
            self.scan
        )

        file_layout.addWidget(
            self.file_input
        )

        file_layout.addWidget(
            browse_button
        )

        file_layout.addWidget(
            scan_button
        )

        main_layout.addWidget(
            file_frame
        )

        # =====================================================
        # Main content
        # =====================================================

        content_layout = QHBoxLayout()

        content_layout.setSpacing(
            15
        )

        # =====================================================
        # Character sidebar
        # =====================================================

        sidebar = QFrame()

        sidebar.setObjectName(
            "sidebar"
        )

        sidebar_layout = QVBoxLayout(
            sidebar
        )

        sidebar_layout.setContentsMargins(
            10,
            10,
            10,
            10
        )

        characters_title = QLabel(
            "Characters"
        )

        characters_title.setObjectName(
            "sectionTitle"
        )

        sidebar_layout.addWidget(
            characters_title
        )

        self.characters_list = QListWidget()

        self.characters_list.itemClicked.connect(
            self.on_character_selected
        )

        sidebar_layout.addWidget(
            self.characters_list
        )

        content_layout.addWidget(
            sidebar,
            1
        )

        # =====================================================
        # Details
        # =====================================================

        details_frame = QFrame()

        details_frame.setObjectName(
            "details"
        )

        details_layout = QVBoxLayout(
            details_frame
        )

        details_layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.details_scroll = QScrollArea()
        self.details_scroll.viewport().setStyleSheet(
            "background-color: transparent;"
        )

        self.details_scroll.setWidgetResizable(
            True
        )

        self.details_content = QWidget()
        self.details_content.setObjectName("detailsContent")
        self.details_layout = QVBoxLayout(
            self.details_content
        )

        self.details_layout.setAlignment(
            Qt.AlignTop
        )

        self.details_scroll.setWidget(
            self.details_content
        )

        details_layout.addWidget(
            self.details_scroll
        )

        content_layout.addWidget(
            details_frame,
            3
        )

        main_layout.addLayout(
            content_layout
        )

    # =========================================================
    # Style
    # =========================================================

    def apply_style(self):

        self.setStyleSheet(
            """
            QMainWindow {
                background-color: #000000;
            }

            QWidget {
                color: #E8E8E8;
                font-size: 14px;
            }
            QLabel#logo {
                color: #F0840D;
                border: 3px solid #F0840D;
                border-radius: 8px;
                padding: 5px 10px;
                font-size: 20px;
                font-weight: bold;
                background-color: transparent;
            }

            QLabel#title {
                background-color: transparent;
                font-size: 24px;
                font-weight: bold;
                border: none;
            }

            #title {
                font-size: 26px;
                font-weight: bold;
            }

            #status {
                color: #8A8F98;
            }

            #sidebar,
            #details,
            QFrame {
                background-color: #111318;
                border: 1px solid #292D35;
                border-radius: 8px;
            }

            QLineEdit {
                background-color: #111318;
                border: 1px solid #30343D;
                border-radius: 6px;
                padding: 9px;
            }

            QLineEdit:focus {
                border: 1px solid #6A7280;
            }

            QPushButton {
                background-color: #242932;
                border: 1px solid #353B46;
                border-radius: 6px;
                padding: 9px 16px;
            }

            QPushButton:hover {
                background-color: #303641;
            }

            #scanButton {
                background-color: #F0840D;
                font-weight: bold;
            }

            #scanButton:hover {
                background-color: #596579;
            }

            QListWidget {
                background-color: transparent;
                border: none;
                outline: none;
            }

            QListWidget::item {
                padding: 8px;
                margin: 3px 0;
                color: #FFF;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            QListWidget::item:hover {
                background-color: #242932;
            }

            QListWidget::item:selected {
                background-color: #343B48;
                border-left: 3px solid #F0840D;
            }

            #sectionTitle {
                font-size: 18px;
                font-weight: bold;
                padding: 3px 12px;
                background-color: transparent;
                border: none;
                border-radius: 0;
                border-left: 3px solid #F0840D;
            }

            #characterName {
                font-size: 28px;
                font-weight: bold;
                border-radius: 0px;
                border-left: 3px solid #F0840D;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
            }

            #characterInfo {
                color: #AEB4BE;
                font-size: 15px;
                padding: 10px 5px;
                background-color: #343B48;
            }

            #detailSection {
                font-size: 18px;
                font-weight: bold;
                margin-top: 12px;
                color: #FFF;
                border-radius: 0px;
                border-left: 3px solid #F0840D;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: #343B48;
            }

            #detailValue {
                color: #C7CBD2;
                padding-left: 5px;
                border-radius: 0px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: #343B48;
            }

            #recipe {
                color: #AEB4BE;
                padding-left: 10px;
                border-radius: 0px;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: #343B48;
            }

            #equipmentSlot {
                color: #8F96A2;
                border-radius: 0px;
                border-left: 3px solid #F0840D;
                border-top-right-radius: 6px;
                border-bottom-right-radius: 6px;
                background-color: #343B48;
            }

            QScrollArea {
                border: none;
                background: transparent;
            }

            QLabel#status {
                padding: 8px;
                border: 1px solid #F0840D;
                color: #FFF;
                font-size: 14px;
            }
            QScrollBar:vertical {
                background: #1A1A1A;
                width: 2px;
                margin: 0;
            }

            QScrollBar::handle:vertical {
                background: #F0840D;
                min-height: 30px;
                border-radius: 5px;
            }

            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                height: 0;
            }

            QScrollBar::add-page:vertical,
            QScrollBar::sub-page:vertical {
                background: transparent;
            }

            QScrollArea {
                background-color: transparent;
                border: none;
            }
            QWidget#detailsContent {
                background-color: #343B48;
            }
            """
        )

    # =========================================================
    # Browse
    # =========================================================

    def detect_saved_variables(self):

        file_path = find_saved_variables()

        if file_path:

            self.file_input.setText(
                str(file_path)
            )

            self.status_label.setText(
                "<span style='color:#F0840D;'>●</span>&nbsp;&nbsp;"
                "SavedVariables detected"
            )

        else:

            self.status_label.setText(
                "<span style='color:#8A8F98;'>●</span>&nbsp;&nbsp;"
                "SavedVariables not found"
            )

    def browse_file(self):

        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select SavedVariables.lua",
            "",
            "Lua files (*.lua);;All files (*)"
        )

        if file_path:

            self.file_input.setText(
                file_path
            )

    # =========================================================
    # Scan
    # =========================================================

    def scan(self):

        file_path = (
            self.file_input
            .text()
            .strip()
        )

        if not file_path:

            QMessageBox.warning(
                self,
                "Missing file",
                "Please select a SavedVariables.lua file."
            )

            return

        try:

            data = load_saved_variables(
                file_path
            )

        except Exception as e:

            QMessageBox.critical(
                self,
                "Scan error",
                str(e)
            )

            return

        characters_data = data.get(
            "characters",
            {}
        )

        self.characters = []

        for character_key, character_data in characters_data.items():

            character = Character(
                character_key,
                character_data
            )

            self.characters.append(
                character
            )

        self.display_characters()

        self.status_label.setText(
            f"<span style='color:#F0840D;'>●</span>&nbsp;&nbsp;"
            f"{len(self.characters)} character(s) detected"
        )

        if self.characters:

            self.characters_list.setCurrentRow(
                0
            )

            self.display_character_details(
                self.characters[0]
            )

    # =========================================================
    # Character list
    # =========================================================

    def display_characters(self):

        self.characters_list.clear()

        for character in self.characters:

            item = QListWidgetItem()

            item.setText(
                f"{character.name}\n"
                f"Level {character.level} • "
                f"{character.class_name}"
            )

            self.characters_list.addItem(
                item
            )

    # =========================================================
    # Character selected
    # =========================================================

    def on_character_selected(
        self,
        item
    ):

        index = self.characters_list.row(
            item
        )

        if index < 0:
            return

        if index >= len(self.characters):
            return

        character = self.characters[index]

        self.display_character_details(
            character
        )

    # =========================================================
    # Details
    # =========================================================

    def display_character_details(
        self,
        character
    ):

        self.clear_details()

        # =====================================================
        # Character header
        # =====================================================

        name = QLabel(
            character.name
        )

        name.setObjectName(
            "characterName"
        )

        self.details_layout.addWidget(
            name
        )

        info = QLabel(
            f"Level {character.level}  •  "
            f"{character.class_name}  •  "
            f"{character.race}  •  "
            f"{character.faction}"
        )

        info.setObjectName(
            "characterInfo"
        )
        self.details_layout.addWidget(info)

        realm = QLabel(f"Realm: {character.realm}")
        realm.setObjectName("characterInfo")
        self.details_layout.addWidget(realm)


        # =====================================================
        # Guild
        # =====================================================

        self.add_section_title(
            "Guild"
        )

        if character.guild:

            guild_name = character.guild.get(
                "name",
                "Unknown"
            )

            guild_rank = character.guild.get(
                "rank",
                "Unknown"
            )

            self.add_detail(
                f"{guild_name} — {guild_rank}"
            )

        else:

            self.add_detail(
                "No guild"
            )

        # =====================================================
        # Professions
        # =====================================================

        self.add_section_title(
            "Professions"
        )

        for profession in character.professions.values():

            profession_name = profession.get(
                "name",
                "Unknown"
            )

            skill_level = profession.get(
                "skillLevel",
                0
            )

            max_skill_level = profession.get(
                "maxSkillLevel",
                0
            )

            self.add_detail(
                f"{profession_name} "
                f"{skill_level} / "
                f"{max_skill_level}"
            )

            recipes = profession.get(
                "recipes",
                {}
            )

            for recipe in recipes.values():

                recipe_name = recipe.get(
                    "name",
                    "Unknown"
                )

                recipe_label = QLabel(
                    f"• {recipe_name}"
                )

                recipe_label.setObjectName(
                    "recipe"
                )

                self.details_layout.addWidget(
                    recipe_label
                )

        # =====================================================
        # Equipment
        # =====================================================

        self.add_section_title(
            "Equipment"
        )

        if not character.equipment:

            self.add_detail(
                "No equipment detected."
            )

        else:

            for slot_name, item in character.equipment.items():

                item_id = item.get(
                    "itemID"
                )

                item_link = item.get(
                    "itemLink"
                )

                item_name = self.extract_item_name(
                    item_link
                )

                label = QLabel()

                label.setText(
                    f"<span style='color:#8F96A2;'>"
                    f"{slot_name}"
                    f"</span>"
                    f"   {item_name}"
                    f"   <span style='color:#666;'>"
                    f"#{item_id}"
                    f"</span>"
                )

                label.setObjectName(
                    "detailValue"
                )

                self.details_layout.addWidget(
                    label
                )

        self.details_layout.addStretch()

    # =========================================================
    # Helpers
    # =========================================================

    def add_section_title(
        self,
        text
    ):

        label = QLabel(
            text
        )

        label.setObjectName(
            "detailSection"
        )

        self.details_layout.addWidget(
            label
        )

    def add_detail(
        self,
        text
    ):

        label = QLabel(
            text
        )

        label.setObjectName(
            "detailValue"
        )

        self.details_layout.addWidget(
            label
        )

    def clear_details(self):

        while self.details_layout.count():

            item = self.details_layout.takeAt(
                0
            )

            widget = item.widget()

            if widget:

                widget.deleteLater()

    def extract_item_name(
        self,
        item_link
    ):

        if not item_link:
            return "Unknown item"

        start = item_link.find("[")
        end = item_link.find("]")

        if start == -1 or end == -1:
            return "Unknown item"

        return item_link[
            start + 1:end
        ]