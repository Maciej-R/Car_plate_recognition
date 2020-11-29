from PyQt5 import QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from source.MainWindow2 import UI_MainWindow


class UI(QtWidgets.QMainWindow, UI_MainWindow):
    """
     Class initialized and prepares user's interface so that it's fully operational before forwarding processing to
     other parts of program.
     Provides functions to interact with user (displaying information, updating GUI, etc.)
     Program operates serving manually made user's requests so there's no need for and kind of pre-processing or
     initialization so UI is entry point to whole program and it starts first.
    """

    def __init__(self, *args, **kwargs) -> None:
        """
        Loads required data and configuration for GUI, binds appropriate listeners from Intermediary class to GUI
        elements, initializes it to be displayed.
        :arg pth: Path to GUI definition file -- Removed for now
        :type pth: String -- Removed for now
        :raises RuntimeError: When configuration file has wrong format
        :raises FileNotFoundError: When provided file points to file that does not exists
        :return: None
        :return: None
        """
        super(UI, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.player = QMediaPlayer()

        self.player.error.connect(self.erroralert)
        self.player.play()

        # Setup the playlist.
        self.playlist = QMediaPlaylist()
        self.player.setPlaylist(self.playlist)

        # Add viewer for video playback, separate floating window.
        self.viewer = ViewerWindow(self)
        self.viewer.setWindowFlags(self.viewer.windowFlags() | Qt.WindowStaysOnTopHint)
        self.viewer.setMinimumSize(QSize(480,360))

        self.player.setVideoOutput(self.videoWidget)

        # Connect control buttons/slides for media player.
        self.playButton.pressed.connect(self.player.play)
        self.pauseButton.pressed.connect(self.player.pause)
        self.stopButton.pressed.connect(self.player.stop)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)

        # self.viewButton.toggled.connect(self.toggle_viewer)
        # self.viewer.state.connect(self.viewButton.setChecked)

        self.previousButton.pressed.connect(self.playlist.previous)
        self.nextButton.pressed.connect(self.playlist.next)

        # self.model = PlaylistModel(self.playlist)
        # self.playlistView.setModel(self.model)
        # self.playlist.currentIndexChanged.connect(self.playlist_position_changed)
        # selection_model = self.playlistView.selectionModel()
        # selection_model.selectionChanged.connect(self.playlist_selection_changed)

        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.timeSlider.valueChanged.connect(self.player.setPosition)

        self.open_file_action.triggered.connect(self.open_file)

        self.setAcceptDrops(True)

        self.add_listeners()

        self.file_loaded_handler = None

    def add_listeners(self) -> None:
        """
        Called upon initialization of GUI to bind all required listeners
        :raises NotImplementedError: When function attempts to bind GUI element's listener to nonexistent function
        :return: None
        """
        self.pushButton_4.clicked.connect(self.open_file)

    def results_ready_notify(self):
        """
        Display information about completed process to user and allow him to open output file in player
        :return:
        """

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        for url in e.mimeData().urls():
            self.playlist.addMedia(
                QMediaContent(url)
            )

        self.model.layoutChanged.emit()

        # If not playing, seeking to first of newly added + play.
        if self.player.state() != QMediaPlayer.PlayingState:
            i = self.playlist.mediaCount() - len(e.mimeData().urls())
            self.playlist.setCurrentIndex(i)
            self.player.play()

    def open_file(self):

        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["Movies (*.avi)"])
        dlg.selectNameFilter("Movies (*.avi)")

        path = None

        if dlg.exec_():
            path = dlg.selectedFiles()

        print(path)

        if path:
            path = path[0]
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(path)))
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            print(self.file_loaded_handler)
            try:
                self.file_loaded_handler(path)
            except Exception as e:
                print(e)

        # self.model.layoutChanged.emit()

    def update_duration(self, duration):
        print("!", duration)
        print("?", self.player.duration())

        self.timeSlider.setMaximum(duration)

        if duration >= 0:
            self.totalTimeLabel.setText(hhmmss(duration))

    def update_position(self, position):
        if position >= 0:
            self.currentTimeLabel.setText(hhmmss(position))

        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.timeSlider.blockSignals(True)
        self.timeSlider.setValue(position)
        self.timeSlider.blockSignals(False)

    def playlist_selection_changed(self, ix):
        # We receive a QItemSelection from selectionChanged.
        i = ix.indexes()[0].row()
        self.playlist.setCurrentIndex(i)

    def playlist_position_changed(self, i):
        if i > -1:
            ix = self.model.index(i)
            self.playlistView.setCurrentIndex(ix)

    def toggle_viewer(self, state):
        if state:
            self.viewer.show()
        else:
            self.viewer.hide()

    def erroralert(self, *args):
        print("Error")
        print(args)

    def set_file_loaded_hanlder(self, mthd):

        self.file_loaded_handler = mthd


def hhmmss(ms):
    # s = 1000
    # m = 60000
    # h = 360000
    h, r = divmod(ms, 36000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)
    return ("%d:%02d:%02d" % (h,m,s)) if h else ("%d:%02d" % (m,s))


class ViewerWindow(QMainWindow):
    state = pyqtSignal(bool)

    def closeEvent(self, e):
        # Emit the window state, to update the viewer toggle button.
        self.state.emit(False)


class PlaylistModel(QAbstractListModel):

    def __init__(self, playlist, *args, **kwargs):
        super(PlaylistModel, self).__init__(*args, **kwargs)
        self.playlist = playlist

    def data(self, index, role):
        if role == Qt.DisplayRole:
            media = self.playlist.media(index.row())
            return media.canonicalUrl().fileName()

    def rowCount(self, index):
        return self.playlist.mediaCount()