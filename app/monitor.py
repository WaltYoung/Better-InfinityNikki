#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'Xiao'

import re
import sys
import time
import traceback

from PySide6.QtCore import QThread, Signal, QMutex, QMutexLocker
from pywinauto import Application
from pywinauto.findwindows import ElementNotFoundError, WindowNotFoundError

sys.coinit_flags = 2


class MonitorThread(QThread):
    status_update = Signal(str, str)  # 状态更新信号

    def __init__(self):
        super().__init__()
        self._active = True  # 线程活动标志
        self._connected = False  # 当前连接状态
        self.mutex = QMutex()  # 线程锁
        self.app = None  # 保持应用连接对象

    def run(self):
        """持续监控主循环"""
        while self._active:
            # 阶段1：连接尝试
            while self._active and not self._connected:
                try:
                    self._connect_app()
                except Exception as e:
                    error_msg = f"连接失败: {str(e)}，3秒后重试..."
                    print(error_msg)
                    self._safe_sleep(3)

            # 阶段2：持续监控
            while self._active and self._connected:
                try:
                    # 获取状态栏信息
                    main_window = self.app.window(title_re="(无限暖暖|Infinity Nikki)")
                    static = main_window.child_window(title="Static", control_type="Text")
                    text = static.legacy_properties().get('Value')
                    pattern = r'([^:]+):\[([^\]]+)\]'
                    matches = re.findall(pattern, text)

                    # 带退出检查的等待
                    self._safe_sleep(1)

                except (ElementNotFoundError, WindowNotFoundError):
                    print("连接丢失，尝试重新连接...")
                    self._disconnect_app()
                except Exception as e:
                    print(f"监控错误: {str(e)}")
                    traceback.print_exc()
                    self._disconnect_app()

    def _connect_app(self):
        """建立应用连接"""
        try:
            self.app = Application(backend="uia").connect(title_re="(无限暖暖|Infinity Nikki)", timeout=5)
            self._connected = True
            print("成功连接到应用")
        except (WindowNotFoundError, ElementNotFoundError):
            self._connected = False
            raise RuntimeError("目标应用未找到")
        except Exception as e:
            self._connected = False
            raise RuntimeError(f"连接异常: {str(e)}")

    def _disconnect_app(self):
        """安全断开连接"""
        if self.app:
            try:
                self.app.disconnect()
            except:
                pass
            finally:
                self.app = None
                self._connected = False

    def _safe_sleep(self, seconds):
        """带退出检查的睡眠"""
        for _ in range(int(seconds * 10)):
            if not self._active:
                break
            time.sleep(0.1)

    def stop(self):
        """安全停止监控"""
        with QMutexLocker(self.mutex):
            self._active = False
        self._disconnect_app()
        self.wait(2000)  # 最多等待2秒
        if self.isRunning():
            self.terminate()  # 强制终止最后手段
