# Copyright (C) 2024 Travis Abendshien (CyanVoxel).
# Licensed under the GPL-3.0 License.
# Created for TagStudio: https://github.com/CyanVoxel/TagStudio


import structlog
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QScrollArea,
    QFrame,
    QTextEdit,
    QComboBox,
)

from src.core.library import Tag, Library
from src.core.library.alchemy.enums import TagColor
from src.core.palette import ColorType, get_tag_color

from src.qt.widgets.panel import PanelWidget, PanelModal
from src.qt.widgets.tag import TagWidget
from src.qt.modals.tag_search import TagSearchPanel

logger = structlog.get_logger(__name__)


class BuildTagPanel(PanelWidget):
    on_edit = Signal(object)

    def __init__(self, library: Library, tag_id: int = -1):
        super().__init__()
        self.lib = library
        # self.callback = callback
        # self.tag_id = tag_id
        self.tag: Tag | None = None
        self.setMinimumSize(300, 400)
        self.root_layout = QVBoxLayout(self)
        self.root_layout.setContentsMargins(6, 0, 6, 0)
        self.root_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # Name -----------------------------------------------------------------
        self.name_widget = QWidget()
        self.name_layout = QVBoxLayout(self.name_widget)
        self.name_layout.setStretch(1, 1)
        self.name_layout.setContentsMargins(0, 0, 0, 0)
        self.name_layout.setSpacing(0)
        self.name_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.name_title = QLabel()
        self.name_title.setText("Name")
        self.name_layout.addWidget(self.name_title)
        self.name_field = QLineEdit()
        self.name_layout.addWidget(self.name_field)

        # Shorthand ------------------------------------------------------------
        self.shorthand_widget = QWidget()
        self.shorthand_layout = QVBoxLayout(self.shorthand_widget)
        self.shorthand_layout.setStretch(1, 1)
        self.shorthand_layout.setContentsMargins(0, 0, 0, 0)
        self.shorthand_layout.setSpacing(0)
        self.shorthand_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.shorthand_title = QLabel()
        self.shorthand_title.setText("Shorthand")
        self.shorthand_layout.addWidget(self.shorthand_title)
        self.shorthand_field = QLineEdit()
        self.shorthand_layout.addWidget(self.shorthand_field)

        # Aliases --------------------------------------------------------------
        self.aliases_widget = QWidget()
        self.aliases_layout = QVBoxLayout(self.aliases_widget)
        self.aliases_layout.setStretch(1, 1)
        self.aliases_layout.setContentsMargins(0, 0, 0, 0)
        self.aliases_layout.setSpacing(0)
        self.aliases_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.aliases_title = QLabel()
        self.aliases_title.setText("Aliases")
        self.aliases_layout.addWidget(self.aliases_title)
        self.aliases_field = QTextEdit()
        self.aliases_field.setAcceptRichText(False)
        self.aliases_field.setMinimumHeight(40)
        self.aliases_layout.addWidget(self.aliases_field)

        # Subtags ------------------------------------------------------------
        self.subtags_widget = QWidget()
        self.subtags_layout = QVBoxLayout(self.subtags_widget)
        self.subtags_layout.setStretch(1, 1)
        self.subtags_layout.setContentsMargins(0, 0, 0, 0)
        self.subtags_layout.setSpacing(0)
        self.subtags_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.subtags_title = QLabel()
        self.subtags_title.setText("Parent Tags")
        self.subtags_layout.addWidget(self.subtags_title)

        self.scroll_contents = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_contents)
        self.scroll_layout.setContentsMargins(6, 0, 6, 0)
        self.scroll_layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.scroll_area = QScrollArea()
        # self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setFrameShadow(QFrame.Shadow.Plain)
        self.scroll_area.setFrameShape(QFrame.Shape.NoFrame)
        self.scroll_area.setWidget(self.scroll_contents)
        # self.scroll_area.setMinimumHeight(60)

        self.subtags_layout.addWidget(self.scroll_area)

        self.subtags_add_button = QPushButton()
        self.subtags_add_button.setText("+")
        tsp = TagSearchPanel(self.lib)
        tsp.tag_chosen.connect(lambda x: self.add_subtag_callback(x))
        self.add_tag_modal = PanelModal(tsp, "Add Parent Tags", "Add Parent Tags")
        self.subtags_add_button.clicked.connect(self.add_tag_modal.show)
        self.subtags_layout.addWidget(self.subtags_add_button)

        # self.subtags_field = TagBoxWidget()
        # self.subtags_field.setMinimumHeight(60)
        # self.subtags_layout.addWidget(self.subtags_field)

        # Shorthand ------------------------------------------------------------
        self.color_widget = QWidget()
        self.color_layout = QVBoxLayout(self.color_widget)
        self.color_layout.setStretch(1, 1)
        self.color_layout.setContentsMargins(0, 0, 0, 0)
        self.color_layout.setSpacing(0)
        self.color_layout.setAlignment(Qt.AlignmentFlag.AlignLeft)
        self.color_title = QLabel()
        self.color_title.setText("Color")
        self.color_layout.addWidget(self.color_title)
        self.color_field = QComboBox()
        self.color_field.setEditable(False)
        self.color_field.setMaxVisibleItems(10)
        self.color_field.setStyleSheet("combobox-popup:0;")
        for color in TagColor:
            self.color_field.addItem(color.name, userData=color.value)
        # self.color_field.setProperty("appearance", "flat")
        self.color_field.currentIndexChanged.connect(
            lambda c: (
                # TODO - index and userData might get out of sync, use userData
                self.color_field.setStyleSheet(
                    "combobox-popup:0;"
                    "font-weight:600;"
                    f"color:{get_tag_color(ColorType.TEXT, self.color_field.currentData())};"
                    f"background-color:{get_tag_color(ColorType.PRIMARY, self.color_field.currentData())};"
                )
            )
        )
        self.color_layout.addWidget(self.color_field)

        # Add Widgets to Layout ================================================
        self.root_layout.addWidget(self.name_widget)
        self.root_layout.addWidget(self.shorthand_widget)
        self.root_layout.addWidget(self.aliases_widget)
        self.root_layout.addWidget(self.subtags_widget)
        self.root_layout.addWidget(self.color_widget)
        # self.parent().done.connect(self.update_tag)

        if tag_id >= 0:
            self.tag = self.lib.get_tag(tag_id)
        else:
            self.tag = Tag(
                name="New Tag",
            )

        self.set_tag(self.tag)

    def add_subtag_callback(self, tag_id: int):
        logger.info("add_subtag_callback", tag_id=tag_id)
        # TODO
        self.tag.add_subtag(tag_id)
        self.set_subtags()

    def remove_subtag_callback(self, tag_id: int):
        logger.info(f"removing {tag_id}")
        # tag = self.lib.get_tag(self.tag_id)
        # TODO: Create a single way to update tags and refresh library data
        # new = self.build_tag()
        # TODO
        self.tag.remove_subtag(tag_id)
        # self.tag = new
        # self.lib.update_tag(new)
        self.set_subtags()
        # self.on_edit.emit(self.build_tag())

    def set_subtags(self):
        while self.scroll_layout.itemAt(0):
            self.scroll_layout.takeAt(0).widget().deleteLater()
        # TODO
        logger.info("setting subtags", tag=self.tag, subtags=self.tag.subtag_ids)

        c = QWidget()
        l = QVBoxLayout(c)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(3)
        for tag_id in self.tag.subtag_ids:
            tag = self.lib.get_tag(tag_id)
            tw = TagWidget(tag, False, True)
            tw.on_remove.connect(lambda t=tag_id: self.remove_subtag_callback(t))
            l.addWidget(tw)
        self.scroll_layout.addWidget(c)

    def set_tag(self, tag: Tag):
        logger.info("setting tag", tag=tag)

        self.name_field.setText(tag.name)
        self.shorthand_field.setText(tag.shorthand or "")
        # TODO: Implement aliases
        # self.aliases_field.setText("\n".join(tag.aliases))
        self.set_subtags()
        self.color_field.setCurrentIndex(tag.color.value)

    def build_tag(self) -> Tag:
        color = self.color_field.currentData() or TagColor.DEFAULT

        new_tag = Tag(
            name=self.name_field.text(),
            shorthand=self.shorthand_field.text(),
            # aliases=set(self.aliases_field.toPlainText().split("\n")),
            # subtags_ids=self.tag.subtag_ids,
            color=color,
        )
        logger.info("built tag", tag=new_tag, self_tag=self.tag)
        return new_tag

        # NOTE: The callback and signal do the same thing, I'm currently
        # transitioning from using callbacks to the Qt method of using signals.
        # self.tag_updated.emit(new_tag)
        # self.callback(new_tag)

    # def on_return(self, callback, text:str):
    # 	if text and self.first_tag_id >= 0:
    # 		callback(self.first_tag_id)
    # 		self.search_field.setText('')
    # 		self.update_tags('')
    # 	else:
    # 		self.search_field.setFocus()
    # 		self.parentWidget().hide()
