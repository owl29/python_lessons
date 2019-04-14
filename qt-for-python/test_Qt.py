import sys
from PySide2 import QtWidgets


def show_message():
    messagebox = QtWidgets.QMessageBox(QtWidgets.QMessageBox.Information,
                                       'Title - Hello',
                                       'Hello, Qt for Python!',
                                       QtWidgets.QMessageBox.Close
                                       )
    messagebox.exec_()


def main():
    # アプリケーション作成、Qt初期化のために最初にインスタンス化すること
    app = QtWidgets.QApplication(sys.argv)

    # ボタン作成
    button = QtWidgets.QPushButton('click me!')
    button.resize(100, 40)
    button.show()

    # ボタンクリック時のシグナルに、メッセージ表示のスロット(関数)を結びつける
    button.clicked.connect(show_message)

    # アプリケーションを起動する
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
