#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

from PySide6.QtCore import QTranslator, QCoreApplication
from qfluentwidgets.common.config import QConfig, OptionsConfigItem, OptionsValidator, qconfig

class Config(QConfig):
    language = OptionsConfigItem(
        "基础设置", "language", "简体中文", OptionsValidator(["简体中文", "繁體中文", "English"]), restart=False)
    def __init__(self):
        super().__init__()

    def saveToJson(self):
        qconfig.save()


cfg = Config()
qconfig.load("app/configure/config.json", cfg)
