from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import pyqtSlot
from source.UI import UI
from source.SignalWrapper import *
from source.plates import process_video
from threading import Thread
import re
from os import getcwd


class Intermediary:
    """
    Provides interface with functions handling GUI events. Manages communication between UI and Backend.
    When it's necessary synchronizes actions. Controls program execution
    Saves log (to allow parallel processing Backend sends data back here to be stored until end of given file processing
    and then sorted, prepared and saved)
    """

    def __init__(self, gui: UI):
        """
        Prepares required resources
        :arg gui: Reference to UI class that allows to send updates, interact with UI
        """

        Intermediary.gui = gui
        Intermediary.pth = None

        gui.set_file_loaded_hanlder(Intermediary.handle_file_loaded)
        gui.set_get_report_handler(Intermediary.handle_get_report)

        Intermediary.report = "Not ready"
        Intermediary.started = False

    #________________________ Handlers ________________________
    # Section of handlers for GUI events
    # Name format handle_<event>

    @staticmethod
    def handle_file_loaded(pth:str):
        """
        Handle called after path to analyzed file has been choosen in GUI
        :param pth: Path to movie file
        :type pth: str
        :return: None
        """
        Intermediary.pth = pth
        Intermediary.found = set()
        Intermediary.processor = CallbackThread(Intermediary.signal_done, target=process_video,
                                                args=(pth, Intermediary.found, Intermediary.handle_progress))
        Intermediary.processor.start()
        Intermediary.started = True

    @staticmethod
    def handle_get_report():
        """
        Provides report to UI
        :return: True if report has been updated, False otherwise
        """

        if Intermediary.started:
            if Intermediary.processor.is_alive():
                return False
            Intermediary.started = False
            with open("output/report.txt", "r") as f:
                Intermediary.report = f.read()
            Intermediary.gui.report = Intermediary.report
            return True
        return False

    @staticmethod
    def signal_done():
        """Finishes file processing, displays necessary info, forwards signal to load output file"""
        # Get filename by regex
        pattern = re.compile("/\w*\..*$") # Filename
        res = pattern.search(Intermediary.pth).group(0)
        # Forward signal to GUI with created output path
        Intermediary.gui.signal_done(getcwd() + "/output" + re.sub("\..*$", ".avi", res))
        # Add recognized plates to GUI
        for plate in Intermediary.found:
            Intermediary.gui.add_recognized_plate(plate)

    @staticmethod
    def handle_progress(frame):
        """Display number of frame that is being processed"""

        Intermediary.gui.LInfo.setText("Processing frame #" + str(frame))



class CallbackThread(Thread):

    def __init__(self, callback, **kwargs):
        Thread.__init__(self, **kwargs)
        self.callback = callback

    def run(self):
        super().run()
        self.callback()
