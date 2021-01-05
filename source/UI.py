from PyQt5 import QtWidgets, QtCore
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from source.MainWindow3 import UI_MainWindow
from source.ReportWindow import ReportWindow
import re


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
        Prepares required GUI elements, sets handlers
        :return: None
        """
        super(UI, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # Create invisible window where report will be shown
        self.report_window = ReportWindow()

        # Needed for video playback
        self.player = QMediaPlayer()
        self.player.error.connect(self.log_error)
        self.player.pause()
        self.player.setVideoOutput(self.videoWidget)

        # To accept and load video dropped into GUI
        self.setAcceptDrops(True)

        # Set listeners
        self.add_listeners()

        # Handlers will be added by Intermediary
        self.file_loaded_handler = None
        self.get_report_hanlder = None

        # Current report to display
        self.report = None

        # For list view with found plates
        self.model = QStandardItemModel()
        self.listView.setModel(self.model)

    def add_listeners(self) -> None:
        """
        Called upon initialization of GUI to bind all required listeners
        :raises NotImplementedError: When function attempts to bind GUI element's listener to nonexistent function
        :return: None
        """
        self.BLoad.clicked.connect(self.load_file)
        self.BOpen.clicked.connect(self.open_file)
        self.BReport.clicked.connect(self.show_report)
        self.report_window.save_file_action.triggered.connect(self.save_file)

        # Connect control buttons/slides for media player.
        self.playButton.pressed.connect(self.player.play)
        self.pauseButton.pressed.connect(self.player.pause)
        self.stopButton.pressed.connect(self.player.stop)
        self.volumeSlider.valueChanged.connect(self.player.setVolume)

        self.player.durationChanged.connect(self.update_duration)
        self.player.positionChanged.connect(self.update_position)
        self.timeSlider.valueChanged.connect(self.player.setPosition)

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.acceptProposedAction()

    def dropEvent(self, e):
        """Handles drop action - loads video to player and pass path to file to backend"""

        # Stop current recording
        self.player.pause()

        # Get file to new video and load it
        for url in e.mimeData().urls():
            try:
                lf = url.toLocalFile()
                if re.search(".*\.avi", lf):
                    self.player.setMedia(QMediaContent(url))
                extensions = ["mp4", "avi", "mov", "mpeg", "flv", "wmv"]
                proper_ex = False
                # Check if file has got proper extension
                for ex in extensions:
                    if re.search(".*\." + ex, lf):
                        self.file_loaded_handler(lf)
                        proper_ex = True
                # Show dialog about wrong format
                print(proper_ex)
                if not proper_ex:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Information)
                    msg.setText("Cannot load file")
                    msg.setInformativeText("Wrong file format")
                    msg.setWindowTitle("Error info")
                    msg.setStandardButtons(QMessageBox.Ok)
                    msg.exec_()
                    return
            except Exception as e:
                print(e)

        # Show new video
        self.player.pause()
        self.LInfo.setText("File loaded")

        if self.player.state() != QMediaPlayer.PlayingState:
            pass

    def load_file(self):
        """Show file choosing dialog, if user had chosen file than get path and call appropriate handler"""

        path = self.show_file_choose_dialog("Movies (*.mp4 *.avi *.mov *.mpeg *.flv *.wmv)")

        # Process choice, if one was made
        if path:
            path = path[0]
            try:
                self.file_loaded_handler(path)
                self.LInfo.setText("File loaded")
                self.clear_list_view()
            except Exception as e:
                print(e)

    def open_file(self):
        """Shows file choosing dialog and loads chosen file to player"""

        path = self.show_file_choose_dialog("Movies (*.avi)")

        if path:
            path = path[0]
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
            # Show first frame
            self.player.pause()

    def save_file(self):
        """Opens dialog to choose saved file's name and saves report to given location"""

        name = QFileDialog.getSaveFileName(self, 'Save File')
        if name is None:
            return

        with open(name[0], 'w') as f:
            f.write(self.report)

    def show_file_choose_dialog(self, filter):
        """
        Shows dialog to choose files
        :arg filter: Filter to set up, will allow only specified files
        :return: str - Path to chosen file
        """

        # Set up dialog parameters
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters([filter])
        dlg.selectNameFilter(filter)

        path = None

        # Show dialog and get path
        if dlg.exec_():
            path = dlg.selectedFiles()

        return path

    def update_duration(self, duration):
        """After loading file update displayed length info and scale slider"""

        self.timeSlider.setMaximum(duration)

        if duration >= 0:
            self.totalTimeLabel.setText(hhmmss(duration))

    def update_position(self, position):
        """Updates time displayed on slider as time passes"""

        if position >= 0:
            self.currentTimeLabel.setText(hhmmss(position))

        # Disable the events to prevent updating triggering a setPosition event (can cause stuttering).
        self.timeSlider.blockSignals(True)
        self.timeSlider.setValue(position)
        self.timeSlider.blockSignals(False)

    def log_error(self, *args):
        """Log player errors to console"""

        print("Player error: " + args)

    def signal_done(self, pth:str=None):
        """
        Display information about completed process to user [and open output file in player]
        :arg pth: Path to output video (optional), if present video will be loaded into player
        """

        if pth:
            print(pth)
            self.player.setMedia(QMediaContent(QUrl.fromLocalFile(pth)))
            # Shows first frame so that change will be noticeable
            self.player.pause()

        self.LInfo.setText("Processing finished")

    def show_report(self):
        """Open new window with report or updates text in existing one"""

        # Show window
        if not self.report_window.isVisible():
            self.report_window.show()

        # Update text if needed
        if self.get_report_hanlder():
            self.report_window.TextReport.setText(self.report)

    def add_recognized_plate(self, plate:str):
        """
        Adds recognized license plate to list view in the GUI
        :param plate: String to be added
        :type plate: str
        :return: None
        """

        item = QStandardItem(plate)
        self.model.appendRow(item)

    def clear_list_view(self):
        """Clears list view display"""

        self.model.clear()

#----------------------- Functions for setting up handlers ----------------------------
# All with the same functionality - allows Intermediary to call them in order to bind appropriate functions
# from within itself to certain events

    def set_file_loaded_hanlder(self, mthd):

        self.file_loaded_handler = mthd

    def set_get_report_handler(self, mthd):

        self.get_report_hanlder = mthd


def hhmmss(ms):
    """Convert time from ms to hours, minutes, seconds"""

    h, r = divmod(ms, 36000)
    m, r = divmod(r, 60000)
    s, _ = divmod(r, 1000)

    if h:
        return "%d:%02d:%02d" % (h, m, s)
    else:
        return "%d:%02d" % (m, s)


class ViewerWindow(QMainWindow):
    state = pyqtSignal(bool)

    def closeEvent(self, e):
        # Emit the window state, to update the viewer toggle button.
        self.state.emit(False)
