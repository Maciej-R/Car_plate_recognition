from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QMainWindow, QWidget, QPushButton, QApplication,
                             QLabel, QFileDialog, QStyle, QVBoxLayout)
import sys


class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Video Player")

        self.mediaPlayer = QMediaPlayer()
        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.openButton = QPushButton("Open Video")
        self.openButton.clicked.connect(self.openFile)

        widget = QWidget(self)
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addWidget(self.openButton)
        layout.addWidget(self.playButton)

        widget.setLayout(layout)
        self.mediaPlayer.setVideoOutput(videoWidget)
        print("Done")

    def openFile(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "Open Movie")
        print(fileName)
        if fileName != '':
            print("Set")
            self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(fileName)))

    def play(self):
        print("Play")
        self.mediaPlayer.play()
        return
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            print("Do")
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()


app = QApplication(sys.argv)
videoplayer = VideoPlayer()
videoplayer.resize(640, 480)
videoplayer.show()
sys.exit(app.exec_())