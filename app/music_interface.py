#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

from PySide6.QtWidgets import QApplication
from qfluentwidgets import ScrollArea


class MusicInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('musicInterface')
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")

        self.initWidget()

    def initWidget(self):
        pass

    def retranslateUI(self):
        pass