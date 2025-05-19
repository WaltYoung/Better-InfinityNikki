#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

import sys

import app.assets.resources
from PySide6.QtCore import Qt, QSize, QEventLoop, QTimer, QTranslator, QCoreApplication, QSharedMemory
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QFrame, QApplication, QHBoxLayout, QMessageBox
from app.configure.config import cfg
from app.home_interface import HomeInterface
from app.music_interface import MusicInterface
from app.setting_interface import SettingInterface
from app.utls.const import WindowTitle
from qfluentwidgets import FluentIcon as FIF, setTheme, Theme
from qfluentwidgets import NavigationItemPosition, FluentWindow, SubtitleLabel, setFont, SplashScreen


class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)


class Window(FluentWindow):
    def __init__(self):
        super().__init__()
        # 确保应用程序的运行实例唯一
        self.shared_memory = QSharedMemory("UniqueAppKey")
        if self.shared_memory.attach():  # 如果未调用create申请共享内存空间，则无法调用attach进行绑定，返回false
            QMessageBox.critical(None, "Instance Error", "An instance of the application is already running.")
            sys.exit(1)
        if not self.shared_memory.create(1):  # 申请1字节的共享内存空间
            QMessageBox.critical(None, "Shared Memory Error", "Unable to create shared memory block.")
            sys.exit(1)
        # 启动页面
        self.resize(500, 500)
        self.center()
        self.setWindowTitle(WindowTitle)
        self.setWindowIcon(QIcon(':app/assets/avatar/每日更新暖暖.png'))
        self.splashScreen = SplashScreen(self.windowIcon(), self)
        self.splashScreen.setIconSize(QSize(102, 102))
        self.show()
        self.createSubInterface()
        self.splashScreen.finish()
        # 正式页面
        self.homeInterface = HomeInterface(self)  # 括号内的self将当前Window实例作为父对象传递
        self.musicInterface = MusicInterface(self)
        # self.videoInterface = Widget('Video Interface', self)
        self.settingInterface = SettingInterface(self)

        self.initNavigation()
        self.initWindow()

        self.translator = QTranslator()
        self.languageChanged(cfg.language.value)
        cfg.language.valueChanged.connect(self.languageChanged)

        self.themeChanged(cfg.theme.value)
        cfg.theme.valueChanged.connect(self.themeChanged)

        self.homeInterface.AutoPlayCard.openButton.clicked.connect(lambda: self.switchInterface(1))

    def initNavigation(self):
        self.homeInterfaceItem = self.addSubInterface(self.homeInterface, FIF.HOME, self.tr('Home'))
        self.navigationInterface.addSeparator()
        self.musicInterfaceItem = self.addSubInterface(self.musicInterface, FIF.MUSIC, self.tr('Automatic playing'))
        # self.addSubInterface(self.videoInterface, FIF.VIDEO, 'Video library')
        self.settingInterfaceItem = self.addSubInterface(self.settingInterface, FIF.SETTING, self.tr('Setting'), NavigationItemPosition.BOTTOM)

    def initWindow(self):
        self.resize(1000, 750)
        self.adjust_window_size()
        self.center()
        self.setWindowIcon(QIcon(':app/assets/icons/Nikki_256x256.ico'))
        self.setWindowTitle(WindowTitle)

    def createSubInterface(self):
        loop = QEventLoop(self)
        QTimer.singleShot(1000, loop.quit)
        loop.exec()

    def center(self):
        screen = QApplication.primaryScreen().geometry()# 获取屏幕的几何信息
        size = self.geometry()# 获取窗口的几何信息
        self.move((screen.width() - size.width()) // 2, (screen.height() - size.height()) // 2)# 计算居中的位置

    def adjust_window_size(self):
        screen = QApplication.primaryScreen().geometry()
        if self.height() > screen.height(): # 如果窗口高度大于屏幕高度，调整窗口高度为 650
            self.resize(1000, 650)

    def languageChanged(self, language: str):
        cfg.saveToJson()
        if language == "简体中文":
            self.translator.load(":app/assets/language/translation_zh_CN.qm")
            QCoreApplication.instance().installTranslator(self.translator)
        elif language == "繁體中文":
            # self.translator.load(":app/assets/language/translation_zh_TW.qm")
            # QCoreApplication.instance().installTranslator(self.translator)
            pass
        else:
            QApplication.instance().removeTranslator(self.translator)
        self.retranslateUi()

    def retranslateUi(self):
        self.homeInterfaceItem.setText(QApplication.translate('Window', 'Home'))
        self.musicInterfaceItem.setText(QApplication.translate('Window', 'Automatic playing'))
        self.settingInterfaceItem.setText(QApplication.translate('Window', 'Setting'))
        self.homeInterface.retranslateUi()
        self.musicInterface.retranslateUi()
        self.settingInterface.retranslateUi()
        # self.videoInterface.retranslateUi()

    def themeChanged(self, theme: str):
        cfg.saveToJson()
        if theme == "Light":
            setTheme(Theme.LIGHT, lazy=True)
        else:
            setTheme(Theme.DARK, lazy=True)

    def switchInterface(self, index: int = 0):
        self.stackedWidget.setCurrentIndex(index)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()