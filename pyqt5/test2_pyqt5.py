#!/usr/bin/env python3
#! /usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = QWidget()
    button = QPushButton('button', window) # ボタンを埋め込み
    window.show()

    sys.exit(app.exec_())
