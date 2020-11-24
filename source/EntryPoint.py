import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication
from source.UI import UI
from PyQt5.QtGui import *
from PyQt5.QtCore import *


#app = QtWidgets.QApplication(sys.argv)
app = QApplication(sys.argv)
app.setApplicationName("Placeholder")
app.setStyle("Fusion")

# Fusion dark palette from https://gist.github.com/QuantumCD/6245215.
palette = QPalette()
palette.setColor(QPalette.Window, QColor(53, 53, 53))
palette.setColor(QPalette.WindowText, Qt.white)
palette.setColor(QPalette.Base, QColor(25, 25, 25))
palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
palette.setColor(QPalette.ToolTipBase, Qt.white)
palette.setColor(QPalette.ToolTipText, Qt.white)
palette.setColor(QPalette.Text, Qt.white)
palette.setColor(QPalette.Button, QColor(53, 53, 53))
palette.setColor(QPalette.ButtonText, Qt.white)
palette.setColor(QPalette.BrightText, Qt.red)
palette.setColor(QPalette.Link, QColor(42, 130, 218))
palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
palette.setColor(QPalette.HighlightedText, Qt.black)
app.setPalette(palette)
app.setStyleSheet("QToolTip { color: #ffffff; background-color: #2a82da; border: 1px solid white; }")
ui = UI()
ui.show()
app.exec_()