#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

from PySide6.QtCore import Qt, QUrl, SignalInstance
from PySide6.QtGui import QDesktopServices, QColor
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QApplication
from app.utls.const import Xhs_URL, Bili_URL, Tutorial_URL, Feedback_URL
from qfluentwidgets import ScrollArea, ElevatedCardWidget, CaptionLabel, AvatarWidget, TitleLabel, TextWrap, \
    StrongBodyLabel, SubtitleLabel, CardWidget, BodyLabel, PushButton, FluentIcon
from qfluentwidgets.components.widgets.flyout import IconWidget


class HomeInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName('homeInterface')
        self.setStyleSheet("QScrollArea{background: transparent; border: none}")
        self.banner = TitleLabel(self.tr('Chinese Name - Better Infinity Nikki'), self)
        self.banner.move(40, 40)
        self.tip = SubtitleLabel(self.tr('QuickEnter'), self)
        self.tip.move(40, 375)

        self.initWidget()

    def initWidget(self):
        self.XhsCard = AuthorCard(':app/assets/avatar/每日更新暖暖.jpg', '每日更新暖暖', Xhs_URL, self.tr('Click to go to the author\'s Xiaohongshu homepage'), self)
        self.XhsCard.move(40, 120)
        self.BiliCard = AuthorCard(':app/assets/avatar/布洛妮娅de重装小兔19c.jpg', '布洛妮娅de重装小兔19c', Bili_URL, self.tr('Click to go to the author\'s Bilibili homepage'), self)
        self.BiliCard.move(260, 120)
        self.TutorialCard = AuthorCard(':app/assets/icons/tutorial.ico', self.tr('Tutorial'), Tutorial_URL, self.tr('Click to view tutorial'), self)
        self.TutorialCard.move(480, 120)
        self.FeedbackCard = AuthorCard(':app/assets/icons/feedback.ico', self.tr('Feedback'), Feedback_URL, self.tr('Click to submit feedback'), self)
        self.FeedbackCard.move(700, 120)
        self.AutoPlayCard = SWitchToSubInterface(FluentIcon.MUSIC, self.tr('Auto playing'), self.tr('Automatic playing'), self)
        self.AutoPlayCard.move(40, 420)

    def retranslateUi(self):
        self.banner.setText(QApplication.translate('HomeInterface', 'Chinese Name - Better Infinity Nikki'))
        self.tip.setText(QApplication.translate('HomeInterface', 'QuickEnter'))

        self.XhsCard.contentLabel.setText(QApplication.translate('HomeInterface', 'Click to go to the author\'s Xiaohongshu homepage'))
        self.BiliCard.contentLabel.setText(QApplication.translate('HomeInterface', 'Click to go to the author\'s Bilibili homepage'))
        self.TutorialCard.label.setText(QApplication.translate('HomeInterface', 'Tutorial'))
        self.TutorialCard.contentLabel.setText(QApplication.translate('HomeInterface', 'Click to view tutorial'))
        self.FeedbackCard.label.setText(QApplication.translate('HomeInterface', 'Feedback'))
        self.FeedbackCard.contentLabel.setText(QApplication.translate('HomeInterface', 'Click to submit feedback'))

        self.AutoPlayCard.titleLabel.setText(QApplication.translate('HomeInterface', 'Auto playing'))
        self.AutoPlayCard.contentLabel.setText(QApplication.translate('HomeInterface', 'Automatic playing'))
        self.AutoPlayCard.openButton.setText(QApplication.translate('HomeInterface', 'Open'))


class AuthorCard(ElevatedCardWidget):
    def __init__(self, avatarPath: str, name: str, url: str, content: str, parent=None):
        super().__init__(parent)
        self.avatarWidget = AvatarWidget(avatarPath, self)
        self.avatarWidget.setRadius(48)
        self.label = StrongBodyLabel(name, self)
        self.url = QUrl(url)
        self.contentLabel = CaptionLabel(TextWrap.wrap(content, 28, False)[0], self)
        self.contentLabel.setTextColor(QColor(128, 128, 128))

        self.vBoxLayout = QVBoxLayout(self)
        self.vBoxLayout.setAlignment(Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.avatarWidget, 0, Qt.AlignCenter)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.label, 0, Qt.AlignHCenter | Qt.AlignBottom)
        self.vBoxLayout.addStretch(1)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft | Qt.AlignTop)

        self.setFixedSize(200, 220)

    def mouseReleaseEvent(self, e):
        # super().mouseReleaseEvent(e)
        QDesktopServices.openUrl(self.url)


class SWitchToSubInterface(CardWidget):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent)
        self.iconWidget = IconWidget(icon)
        self.titleLabel = BodyLabel(title, self)
        self.contentLabel = CaptionLabel(content, self)
        self.openButton = PushButton(self.tr('Open'), self)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.setFixedHeight(73)
        self.iconWidget.setFixedSize(48, 48)
        self.contentLabel.setTextColor("#606060", "#d2d2d2")
        self.openButton.setFixedWidth(150)

        self.hBoxLayout.setContentsMargins(20, 11, 11, 11)
        self.hBoxLayout.setSpacing(15)
        self.hBoxLayout.addWidget(self.iconWidget)

        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.setSpacing(0)
        self.vBoxLayout.addWidget(self.titleLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.addWidget(self.contentLabel, 0, Qt.AlignVCenter)
        self.vBoxLayout.setAlignment(Qt.AlignVCenter)
        self.hBoxLayout.addLayout(self.vBoxLayout)

        self.hBoxLayout.addStretch(1)
        self.hBoxLayout.addWidget(self.openButton, 0, Qt.AlignRight)