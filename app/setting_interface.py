#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QApplication
from qfluentwidgets import ScrollArea
from qfluentwidgets import SettingCardGroup, ComboBoxSettingCard, PrimaryPushSettingCard
from qfluentwidgets import FluentIcon
from app.configure.config import cfg
from app.utls.const import __author__ as AUTHOR, __version__ as VERSION, __year__ as YEAR, GitHub_URL, GitHub_Release_URL, Bili_URL


class SettingInterface(ScrollArea):
    def __init__(self, parent=QWidget):
        super().__init__(parent=parent)
        self.setObjectName('settingInterface')
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")

        self.vBoxlayout = QVBoxLayout(self)
        self.scrollWidget = QWidget()
        self.personalGroup = SettingCardGroup(self.tr('Setting'), self.scrollWidget)
        self.personalGroup.setContentsMargins(25, 25, 25, 25)
        self.vBoxlayout.addWidget(self.personalGroup)
        self.aboutGroup = SettingCardGroup(self.tr('About'), self.scrollWidget)
        self.aboutGroup.setContentsMargins(25, 25, 25, 25)
        self.vBoxlayout.addWidget(self.aboutGroup)
        self.initWidget()

    def initWidget(self):
        self.languageCard = ComboBoxSettingCard(
            configItem=cfg.language,
            icon=FluentIcon.LANGUAGE,
            title=self.tr('Language'),
            content=self.tr('Choose the display language for the software'),
            texts=["简体中文", "繁體中文", "English"],
        )
        self.personalGroup.addSettingCard(self.languageCard)
        self.themeCard = ComboBoxSettingCard(
            configItem=cfg.theme,
            icon=FluentIcon.BRUSH,
            title=self.tr('Application Theme'),
            content=self.tr('Choose the theme for the software'),
            texts=[self.tr("Light"), self.tr("Dark")],
        )
        self.personalGroup.addSettingCard(self.themeCard)
        self.aboutBetterINCard = PrimaryPushSettingCard(
            text='Check update',
            icon=FluentIcon.INFO,
            title=self.tr('About BetterIN'),
            content='© ' + self.tr('Copyright') + f" {YEAR}, {AUTHOR}. " +
            self.tr('Version') + " " + VERSION,
            parent=self.aboutGroup
        )
        self.aboutBetterINCard.button.deleteLater()
        self.aboutGroup.addSettingCard(self.aboutBetterINCard)

    def retranslateUi(self):
        self.personalGroup.titleLabel.setText(QApplication.translate('SettingInterface', 'Setting'))
        self.languageCard.setTitle(QApplication.translate('SettingInterface', 'Language'))
        self.languageCard.setContent(QApplication.translate('SettingInterface', 'Choose the display language for the software'))
        self.themeCard.setTitle(QApplication.translate('SettingInterface', 'Application Theme'))
        self.themeCard.setContent(QApplication.translate('SettingInterface', 'Choose the theme for the software'))
        self.themeCard.comboBox.setItemText(0, QApplication.translate('SettingInterface', 'Light'))
        self.themeCard.comboBox.setItemText(1, QApplication.translate('SettingInterface', 'Dark'))

        self.aboutGroup.titleLabel.setText(QApplication.translate('SettingInterface', 'About'))
        self.aboutBetterINCard.setTitle(QApplication.translate('SettingInterface', 'About BetterIN'))
        self.aboutBetterINCard.setContent('© ' + QApplication.translate('SettingInterface', 'Copyright') + f" {YEAR}, {AUTHOR}. " +
            QApplication.translate('SettingInterface', 'Version') + " " + VERSION)