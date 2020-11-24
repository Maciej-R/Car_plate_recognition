from PyQt5.QtWidgets import QFileDialog


class Intermediary:
    """
    Provides interface with functions handling GUI events. Manages communication between UI and Backend.
    When it's necessary synchronizes actions. Controls program execution
    Saves log (to allow parallel processing Backend sends data back here to be stored until end of given file processing
    and then sorted, prepared and saved)
    """

    def __init__(self): #, gui: UI):
        """
        Prepares required resources
        :arg gui: Reference to UI class that allows to send updates, interact with UI
        """
        pass

    def get_log_data(self, data):
        """
        Receives log data, stores it
        :param data:
        :return:
        """

    def log(self, data):
        """
        After end of file processing prepares and saves log file
        :param data:
        :return:
        """
        pass

    #________________________ Handlers ________________________
    # Section of handlers for GUI events
    # Name format handle_<event>

    def handle_xxx(self):
        """

        :return:
        """

    def handle_open_file_dialog(self):

        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)
        dlg.setNameFilters(["Movies (*.mp4)"])
        dlg.selectNameFilter("Movies (*.mp4)")
        
        filenames = str()

        if dlg.exec_():
            filenames = dlg.selectedFiles()

