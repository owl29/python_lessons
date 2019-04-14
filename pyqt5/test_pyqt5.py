import sys
import PyQt5.QtWidgets

def main():
  app = PyQt5.QtWidgets.QApplication([])
  w = PyQt5.QtWidgets.QWidget()
  w.resize(300, 200)
  w.setWindowTitle('foo')

  w.show()
  sys.exit(app.exec())

if __name__ == '__main__':
    main()
